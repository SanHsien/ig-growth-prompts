"""Command-line interface for igprompts."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path
from typing import Any

from .batch import load_topic_queue, run_batch_queue
from .calendar import (
    export_airtable_csv,
    export_buffer_csv,
    export_markdown_calendar,
    export_notion_csv,
    generate_calendar_from_batch_dir,
    generate_calendar_from_ledger,
    generate_calendar_from_workflow_state,
)
from .core import SERIES_FACELESS, SERIES_REELS, get_prompt, list_prompts, render_pipeline, render_prompt
from .experiments import build_report, load_ledger, write_plan
from .providers import CommandProvider, DryRunProvider, ManualProvider, WorkflowProvider
from .renderer import (
    SLIDES_FORMAT_ADDENDUM,
    SlideSpecError,
    render_slides_from_answer,
    render_slides_from_spec_file,
)
from .workflow import STATE_FILE, WorkflowRunner, WorkflowState

CMD_ENV = "IGPROMPTS_LLM_CMD"
FACELESS_FORMATS_PROMPT_ID = 3
REVIVAL_PROMPT_ID = 10
SERIES_CHOICES = [SERIES_FACELESS, SERIES_REELS, "faceless", "reels"]


def parse_var_arguments(var_args: list[str] | None) -> dict[str, str]:
    """Parse ``key=value`` strings."""
    result: dict[str, str] = {}
    for item in var_args or []:
        if "=" not in item:
            raise ValueError(f"Invalid variable specification '{item}'. Format must be key=value.")
        k, v = item.split("=", 1)
        result[k.strip()] = v.strip()
    return result


def load_config_file(file_path: str | None) -> dict[str, Any]:
    if not file_path:
        return {}
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Configuration JSON root must be an object.")
    return data


def _config_from_args(args: argparse.Namespace) -> dict[str, Any]:
    cfg = load_config_file(getattr(args, "json_file", None))
    cfg.update(parse_var_arguments(getattr(args, "var", None)))
    return cfg


def _build_provider(args: argparse.Namespace, out_dir: Path) -> WorkflowProvider:
    provider_type = getattr(args, "provider", "dry-run")
    if provider_type == "manual":
        return ManualProvider(out_dir / "handoff")
    if provider_type == "command":
        command = getattr(args, "cmd", None) or os.environ.get(CMD_ENV, "")
        if not command.strip():
            raise ValueError(f"--provider command needs --cmd or the {CMD_ENV} environment variable.")
        return CommandProvider(command, timeout=getattr(args, "timeout", 600.0), encoding=getattr(args, "encoding", "utf-8"))
    return DryRunProvider()


def _add_vars(p: argparse.ArgumentParser) -> None:
    p.add_argument("--json-file", "-f", type=str, help="JSON file with variables.")
    p.add_argument("--var", "-v", action="append", help="Set a variable as key=value (repeatable).")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="igprompts",
        description="Tool-agnostic Instagram content prompts: works with any AI chat, CLI, API, or agent.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="List prompts and their variables.")
    p_list.add_argument("--series", "-s", choices=SERIES_CHOICES)

    # show
    p_show = sub.add_parser("show", help="Show a raw template.")
    p_show.add_argument("id", help="Prompt ID (01-12) or key.")

    # render
    p_render = sub.add_parser("render", help="Fill one prompt with variables.")
    p_render.add_argument("id", help="Prompt ID (01-12) or key.")
    _add_vars(p_render)
    p_render.add_argument("--allow-missing", action="store_true", help="Keep <placeholder> for missing variables.")

    # pipeline
    p_pipe = sub.add_parser("pipeline", help="Write every prompt of a series into one Markdown file.")
    p_pipe.add_argument("--series", "-s", choices=SERIES_CHOICES, default=SERIES_FACELESS)
    _add_vars(p_pipe)
    p_pipe.add_argument("--output", "-o", type=str)

    # run-pipeline
    p_run = sub.add_parser("run-pipeline", help="Run a series step by step with any AI tool.")
    p_run.add_argument("--series", "-s", choices=SERIES_CHOICES, default=SERIES_FACELESS)
    _add_vars(p_run)
    p_run.add_argument("--provider", "-p", choices=["dry-run", "manual", "command"], default="dry-run",
                       help="dry-run: no AI call; manual: file handoff for any chat UI; command: pipe to any CLI.")
    p_run.add_argument("--cmd", type=str, help=f"Command for --provider command (or set {CMD_ENV}).")
    p_run.add_argument("--timeout", type=float, default=600.0, help="Per-step timeout in seconds for --provider command.")
    p_run.add_argument("--encoding", type=str, default="utf-8", help="Text encoding of the command's stdin/stdout.")
    p_run.add_argument("--output-dir", "-o", type=str, default="output_pipeline")
    p_run.add_argument("--resume", "-r", action="store_true", help=f"Continue from <output-dir>/{STATE_FILE}.")
    p_run.add_argument("--render-slides", action="store_true",
                       help="Ask Prompt 03 for a ```slides block and render it to SVG (faceless series).")

    # render-slides
    p_slides = sub.add_parser("render-slides", help="Render SVG cards from a slide spec file.")
    p_slides.add_argument("--from", dest="spec", required=True,
                          help="Markdown slide spec, or any file containing a ```slides block.")
    p_slides.add_argument("--output-dir", "-o", type=str, default="slides_output")

    # experiment
    p_exp = sub.add_parser("experiment", help="7-day test ledger (pairs with Prompts 12 and 10).")
    exp_sub = p_exp.add_subparsers(dest="exp_command", required=True)
    p_plan = exp_sub.add_parser("plan", help="Create an empty CSV ledger.")
    p_plan.add_argument("--csv", required=True)
    p_plan.add_argument("--days", type=int, default=7)
    p_plan.add_argument("--overwrite", action="store_true")
    p_rep = exp_sub.add_parser("report", help="Analyze a filled ledger.")
    p_rep.add_argument("--csv", required=True)
    p_rep.add_argument("--output", "-o", type=str, help="Write the Markdown report here.")
    p_rep.add_argument("--prompt-out", type=str, help="Also write Prompt 10 filled with this report.")

    # calendar (Phase 4)
    p_cal = sub.add_parser("calendar", help="Phase 4: Content calendar generation and multi-channel export.")
    cal_sub = p_cal.add_subparsers(dest="cal_command", required=True)
    p_cal_gen = cal_sub.add_parser("generate", help="Generate content calendar from ledger or workflow state.")
    p_cal_gen.add_argument("--from-ledger", type=str, help="Path to 7-day test ledger CSV.")
    p_cal_gen.add_argument("--from-state", type=str, help="Path to workflow_state.json.")
    p_cal_gen.add_argument("--from-batch", type=str, help="Path to batch output directory containing workflow_state.json files.")
    p_cal_gen.add_argument("--interval", type=int, default=1, help="Interval days between posts for batch calendar (default: 1).")
    p_cal_gen.add_argument("--start-date", type=str, default=date.today().isoformat(), help="Start date (YYYY-MM-DD).")
    p_cal_gen.add_argument("--format", choices=["notion", "airtable", "buffer", "markdown", "all"], default="all")
    p_cal_gen.add_argument("--output", "-o", dest="output_target", type=str, default="calendar_export",
                           help="Output directory or target file path.")

    # batch (Phase 4)
    p_batch = sub.add_parser("batch", help="Phase 4: Batch queue execution for multiple topics.")
    batch_sub = p_batch.add_subparsers(dest="batch_command", required=True)
    p_batch_run = batch_sub.add_parser("run", help="Run batch topic queue.")
    p_batch_run.add_argument("-f", "--queue", required=True, help="Path to topics_queue.json or topics_queue.csv.")
    p_batch_run.add_argument("--output-dir", "-o", type=str, default="batch_output")
    p_batch_run.add_argument("--provider", "-p", choices=["dry-run", "manual", "command"], default="dry-run")
    p_batch_run.add_argument("--cmd", type=str, help="Command for --provider command.")

    return parser


def _cmd_run(args: argparse.Namespace) -> int:
    out_dir = Path(args.output_dir)
    state_path = out_dir / STATE_FILE
    if args.resume:
        state = WorkflowState.load_checkpoint(state_path)
        config = state.config
    else:
        if state_path.exists():
            raise FileExistsError(f"{state_path} exists. Use --resume, or pick another --output-dir.")
        state = None
        config = _config_from_args(args)

    addenda = {FACELESS_FORMATS_PROMPT_ID: SLIDES_FORMAT_ADDENDUM} if args.render_slides else {}
    provider = _build_provider(args, out_dir)
    runner = WorkflowRunner(config=config, series=args.series, provider=provider, state=state,
                            prompt_addenda=addenda)
    try:
        runner.run_all(checkpoint_path=state_path)
    finally:
        artifacts = runner.export_manifest(out_dir)

    print(f"Series:   {runner.series}  Provider: {provider.name}")
    print(f"State:    {artifacts['state']}")
    print(f"Manifest: {artifacts['manifest']}")

    waiting = [s for s in runner.pending_steps() if s.status == "awaiting_response"]
    if waiting and isinstance(provider, ManualProvider):
        step = waiting[0]
        prompt_path, response_path = provider.paths(get_prompt(step.step_id))
        print(f"\nWAITING:  Prompt {step.step_id:02d} ({step.title})")
        print(f"  1. Paste {prompt_path} into any AI tool.")
        print(f"  2. Save the answer as {response_path}")
        print(f"  3. Run again with --resume --provider manual -o {out_dir}")
        return 0

    if args.render_slides and runner.is_complete():
        if FACELESS_FORMATS_PROMPT_ID not in runner.state.steps:
            sys.stderr.write("WARNING: --render-slides only applies to the faceless_carousel series.\n")
            return 0
        answer = runner.state.step_output(FACELESS_FORMATS_PROMPT_ID)
        try:
            files = render_slides_from_answer(answer, out_dir / "slides")
            print(f"Slides:   {len(files)} SVG cards in {out_dir / 'slides'}")
        except SlideSpecError as exc:
            sys.stderr.write(
                f"WARNING: slides not rendered: {exc}\n"
                f"  Prompt 03's answer needs a ```slides block. Fix the answer, or run:\n"
                f"  python -m igprompts render-slides --from <your-spec.md>\n"
            )
    return 0


def _cmd_experiment(args: argparse.Namespace) -> int:
    if args.exp_command == "plan":
        path = write_plan(args.csv, days=args.days, overwrite=args.overwrite)
        print(f"Ledger created: {path}")
        print("Fill hypothesis/topic/hook/format/cta/primary_metric from Prompt 12, then the numbers after posting.")
        return 0

    report = build_report(load_ledger(args.csv))
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report written: {args.output}")
    else:
        print(report)
    if args.prompt_out:
        filled = render_prompt(REVIVAL_PROMPT_ID, {"content_and_metrics": report})
        Path(args.prompt_out).write_text(filled, encoding="utf-8")
        print(f"Prompt 10 input written: {args.prompt_out}")
    return 0


def _cmd_calendar(args: argparse.Namespace) -> int:
    if args.cal_command == "generate":
        entries = []
        if args.from_ledger:
            rows = load_ledger(args.from_ledger)
            entries = generate_calendar_from_ledger(rows, start_date=args.start_date)
        elif args.from_state:
            state = WorkflowState.load_checkpoint(args.from_state)
            entries = generate_calendar_from_workflow_state(state, start_date=args.start_date)
        elif args.from_batch:
            entries = generate_calendar_from_batch_dir(
                args.from_batch,
                start_date=args.start_date,
                interval_days=args.interval,
            )
        else:
            raise ValueError("Specify either --from-ledger, --from-state, or --from-batch.")

        target = Path(args.output_target)
        is_file = target.suffix.lower() in (".csv", ".md")
        out_dir = target.parent if is_file else target
        out_dir.mkdir(parents=True, exist_ok=True)
        fmt = args.format

        if fmt == "notion" and is_file:
            p = export_notion_csv(entries, target)
            print(f"Notion CSV:   {p}")
            return 0
        if fmt == "airtable" and is_file:
            p = export_airtable_csv(entries, target)
            print(f"Airtable CSV: {p}")
            return 0
        if fmt == "buffer" and is_file:
            p = export_buffer_csv(entries, target)
            print(f"Buffer CSV:   {p}")
            return 0
        if fmt == "markdown" and is_file:
            export_markdown_calendar(entries, target)
            print(f"Markdown:     {target}")
            return 0

        if fmt in ("notion", "all"):
            p = export_notion_csv(entries, out_dir / "notion_database.csv")
            print(f"Notion CSV:   {p}")
        if fmt in ("airtable", "all"):
            p = export_airtable_csv(entries, out_dir / "airtable_calendar.csv")
            print(f"Airtable CSV: {p}")
        if fmt in ("buffer", "all"):
            p = export_buffer_csv(entries, out_dir / "buffer_schedule.csv")
            print(f"Buffer CSV:   {p}")
        if fmt in ("markdown", "all"):
            p = out_dir / "content_calendar.md"
            export_markdown_calendar(entries, p)
            print(f"Markdown:     {p}")

        return 0
    return 0


def _cmd_batch(args: argparse.Namespace) -> int:
    if args.batch_command == "run":
        items = load_topic_queue(args.queue)
        out_dir = Path(args.output_dir)
        provider = _build_provider(args, out_dir)
        results = run_batch_queue(items, out_dir, provider=provider)
        print(f"Batch completed: processed {len(results)} topics in {out_dir}")
        for r in results:
            print(f" - [{r['id']}] {r['topic']} ({r['series']}) -> {r['manifest']}")
        return 0
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "list":
            print(f"{'ID':<4} {'Key':<24} {'Title':<30} Variables")
            print("-" * 90)
            for p in list_prompts(args.series):
                print(f"{p.id:02d}   {p.key:<24} {p.title:<30} {', '.join(p.variables)}")
            return 0
        if args.command == "show":
            p = get_prompt(args.id)
            print(f"# PROMPT {p.id:02d}: {p.title}\n")
            print(p.template)
            return 0
        if args.command == "render":
            print(render_prompt(args.id, _config_from_args(args), fallback_placeholder=args.allow_missing))
            return 0
        if args.command == "pipeline":
            doc = render_pipeline(_config_from_args(args), series=args.series)
            if args.output:
                Path(args.output).write_text(doc, encoding="utf-8")
                print(f"Pipeline written: {args.output}")
            else:
                print(doc)
            return 0
        if args.command == "run-pipeline":
            return _cmd_run(args)
        if args.command == "render-slides":
            files = render_slides_from_spec_file(args.spec, args.output_dir)
            print(f"{len(files)} SVG slides written to {args.output_dir}")
            return 0
        if args.command == "experiment":
            return _cmd_experiment(args)
        if args.command == "calendar":
            return _cmd_calendar(args)
        if args.command == "batch":
            return _cmd_batch(args)
    except Exception as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
