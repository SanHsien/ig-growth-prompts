"""Command-line interface for igprompts."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

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
    if args.provider == "manual":
        return ManualProvider(out_dir / "handoff")
    if args.provider == "command":
        command = args.cmd or os.environ.get(CMD_ENV, "")
        if not command.strip():
            raise ValueError(f"--provider command needs --cmd or the {CMD_ENV} environment variable.")
        return CommandProvider(command, timeout=args.timeout, encoding=args.encoding)
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

    p_list = sub.add_parser("list", help="List prompts and their variables.")
    p_list.add_argument("--series", "-s", choices=SERIES_CHOICES)

    p_show = sub.add_parser("show", help="Show a raw template.")
    p_show.add_argument("id", help="Prompt ID (01-12) or key.")

    p_render = sub.add_parser("render", help="Fill one prompt with variables.")
    p_render.add_argument("id", help="Prompt ID (01-12) or key.")
    _add_vars(p_render)
    p_render.add_argument("--allow-missing", action="store_true", help="Keep <placeholder> for missing variables.")

    p_pipe = sub.add_parser("pipeline", help="Write every prompt of a series into one Markdown file.")
    p_pipe.add_argument("--series", "-s", choices=SERIES_CHOICES, default=SERIES_FACELESS)
    _add_vars(p_pipe)
    p_pipe.add_argument("--output", "-o", type=str)

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

    p_slides = sub.add_parser("render-slides", help="Render SVG cards from a slide spec file.")
    p_slides.add_argument("--from", dest="spec", required=True,
                          help="Markdown slide spec, or any file containing a ```slides block.")
    p_slides.add_argument("--output-dir", "-o", type=str, default="slides_output")

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
    except Exception as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
