"""Command-line interface for igprompts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .core import get_prompt, list_prompts, render_pipeline, render_prompt
from .renderer import generate_carousel_from_workflow
from .workflow import DryRunProvider, WorkflowRunner, WorkflowState


def parse_var_arguments(var_args: list[str] | None) -> dict[str, str]:
    """Parse list of `key=value` strings into a dictionary."""
    result: dict[str, str] = {}
    if not var_args:
        return result
    for item in var_args:
        if "=" not in item:
            raise ValueError(f"Invalid variable specification '{item}'. Format must be key=value.")
        k, v = item.split("=", 1)
        result[k.strip()] = v.strip()
    return result


def load_config_file(file_path: str | None) -> dict[str, Any]:
    """Load json config file if path is supplied."""
    if not file_path:
        return {}
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Configuration JSON root must be an object/dict.")
    return data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="igprompts",
        description="CLI tool for Instagram Growth & Faceless Content Prompt Management.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: list
    subparsers.add_parser("list", help="List all available prompts and required variables.")

    # Subcommand: show
    show_parser = subparsers.add_parser("show", help="Display the raw template of a specific prompt.")
    show_parser.add_argument("id", type=int, help="Prompt ID (1-5)")

    # Subcommand: render
    render_parser = subparsers.add_parser("render", help="Render a prompt with supplied variables.")
    render_parser.add_argument("id", type=int, help="Prompt ID (1-5)")
    render_parser.add_argument("--json-file", "-f", type=str, help="Path to JSON file with variables.")
    render_parser.add_argument("--var", "-v", action="append", help="Set variable as key=value.")
    render_parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Allow missing variables and keep <placeholder> tokens.",
    )

    # Subcommand: pipeline
    pipe_parser = subparsers.add_parser(
        "pipeline", help="Render all 5 prompts into an end-to-end SOP markdown document."
    )
    pipe_parser.add_argument("--json-file", "-f", type=str, help="Path to JSON file with variables.")
    pipe_parser.add_argument("--var", "-v", action="append", help="Set variable as key=value.")
    pipe_parser.add_argument("--output", "-o", type=str, help="Optional output markdown file path.")

    # Subcommand: run-pipeline (Phase 1 Automated Runner)
    run_parser = subparsers.add_parser(
        "run-pipeline", help="Execute the 5-step workflow runner with state tracking."
    )
    run_parser.add_argument("--json-file", "-f", type=str, help="Path to JSON file with variables.")
    run_parser.add_argument("--var", "-v", action="append", help="Set variable as key=value.")
    run_parser.add_argument("--resume", "-r", type=str, help="Resume from an existing checkpoint JSON.")
    run_parser.add_argument(
        "--output-dir", "-o", type=str, default="output_pipeline", help="Directory to save artifacts."
    )
    run_parser.add_argument(
        "--render-slides", action="store_true", help="Automatically generate 4:5 SVG carousel slides."
    )

    # Subcommand: render-slides (Phase 2 SVG Generator)
    slides_parser = subparsers.add_parser(
        "render-slides", help="Render 1080x1350 SVG carousel cards from state or config."
    )
    slides_parser.add_argument("--state-file", "-s", type=str, help="Path to existing workflow_state.json.")
    slides_parser.add_argument("--json-file", "-f", type=str, help="Path to variables JSON file.")
    slides_parser.add_argument(
        "--output-dir", "-o", type=str, default="slides_output", help="Directory for SVG files."
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "list":
            print(f"{'ID':<4} {'Key':<24} {'Title':<30} {'Required Variables'}")
            print("-" * 90)
            for p in list_prompts():
                vars_str = ", ".join(p.variables)
                print(f"{p.id:<4} {p.key:<24} {p.title:<30} {vars_str}")
            return 0

        if args.command == "show":
            p = get_prompt(args.id)
            print(f"# PROMPT {p.id}: {p.title}\n")
            print(p.template)
            return 0

        if args.command == "render":
            vars_dict = load_config_file(args.json_file)
            vars_dict.update(parse_var_arguments(args.var))
            output = render_prompt(
                args.id,
                vars_dict,
                fallback_placeholder=args.allow_missing,
            )
            print(output)
            return 0

        if args.command == "pipeline":
            vars_dict = load_config_file(args.json_file)
            vars_dict.update(parse_var_arguments(args.var))
            doc = render_pipeline(vars_dict)
            if args.output:
                out_path = Path(args.output)
                out_path.write_text(doc, encoding="utf-8")
                print(f"Pipeline successfully written to: {out_path}")
            else:
                print(doc)
            return 0

        if args.command == "run-pipeline":
            state = None
            if args.resume:
                state = WorkflowState.load_checkpoint(args.resume)
                config = state.config
            else:
                config = load_config_file(args.json_file)
                config.update(parse_var_arguments(args.var))

            runner = WorkflowRunner(config=config, provider=DryRunProvider(), state=state)
            out_dir = Path(args.output_dir)
            checkpoint_file = out_dir / "workflow_state.json"
            runner.run_all(checkpoint_path=checkpoint_file)
            artifacts = runner.export_manifest(out_dir)

            print(f"Workflow completed successfully.")
            print(f" - State:    {artifacts['state']}")
            print(f" - Manifest: {artifacts['manifest']}")

            if args.render_slides:
                slides_dir = out_dir / "slides"
                files = generate_carousel_from_workflow(runner.state, slides_dir)
                print(f" - Slides:   {len(files)} SVG cards generated in {slides_dir}")
            return 0

        if args.command == "render-slides":
            if args.state_file:
                state = WorkflowState.load_checkpoint(args.state_file)
            else:
                cfg = load_config_file(args.json_file)
                state = WorkflowState(config=cfg)

            out_dir = Path(args.output_dir)
            files = generate_carousel_from_workflow(state, out_dir)
            print(f"Successfully generated {len(files)} SVG carousel slides in: {out_dir}")
            return 0

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
