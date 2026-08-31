from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .errors import GXKBError
from .normalizer import normalize


def _print_progress(event: dict[str, object]) -> None:
    stage = event["stage"]
    elapsed = event.get("elapsed", 0)
    counts = ""
    if "percent" in event:
        counts = f" {event['percent']}% ({event.get('current', 0)}/{event.get('total', 0)})"
    detail = event.get("object")
    if detail:
        counts += f" {detail}"
    processed = event.get("processed")
    skipped = event.get("skipped")
    if processed is not None or skipped is not None:
        counts += f" processed={processed or 0} skipped={skipped or 0}"
    print(f"[{elapsed:>7.1f}s] {stage}: {event['message']}{counts}", flush=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Normalize GeneXus XML/XPZ exports into a readable knowledge base")
    parser.add_argument("input", type=Path, help=".xml or .xpz file")
    parser.add_argument("-o", "--output", type=Path, default=Path("normalized-kb"), help="Output directory")
    parser.add_argument("--xml-member", help="XML member inside an XPZ; avoids automatic selection")
    parser.add_argument("--gxl", type=Path, help="Optional GeneXus 9 .gxl object-selection file; never used as primary content")
    parser.add_argument("--without-raw", action="store_true", help="Do not copy the input into raw/ (useful for shareable examples)")
    parser.add_argument("--redact-source", action="store_true", help="Redact user/path source attributes in generated metadata")
    parser.add_argument("--share-safe", action="store_true", help="Create a share-safe export: omit raw input and redact provenance")
    parser.add_argument("--reprocess-all", action="store_true", help="Reprocess every object in this input")
    parser.add_argument("--snapshot", action="store_true", help="Treat this input as a complete snapshot and retire absent objects for its KB version")
    parser.add_argument("--new-kb", action="store_true", help="Explicitly document initialization of a new KB output (never mixes existing KBs)")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress reporting")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        output = normalize(args.input, args.output, args.xml_member, preserve_raw=not args.without_raw, redact_source=args.redact_source, reprocess_all=args.reprocess_all, new_kb=args.new_kb, share_safe=args.share_safe, snapshot=args.snapshot, gxl_selection=args.gxl, progress=None if args.quiet else _print_progress)
        print(f"Normalization completed: {output}")
        return 0
    except GXKBError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(
            f"Error accessing input or output: {exc}. "
            "Check that the input exists and the output directory is writable.",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
