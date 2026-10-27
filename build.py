#!/usr/bin/env python3
"""Build every sheet in src/sheets into a print-ready PDF in printables/."""
from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from weasyprint import HTML

KIT_ROOT = Path(__file__).resolve().parent
SHEETS_DIR = KIT_ROOT / "src" / "sheets"
OUTPUT_DIR = KIT_ROOT / "printables"


@dataclass(frozen=True)
class Sheet:
    source: Path
    output: Path


@dataclass(frozen=True)
class BuildResult:
    sheet: Sheet
    pages: int
    size_bytes: int


def discover_sheets() -> list[Sheet]:
    if not SHEETS_DIR.is_dir():
        raise SystemExit(f"missing folder: {SHEETS_DIR}")
    sheets = [
        Sheet(path, OUTPUT_DIR / (path.stem + ".pdf"))
        for path in sorted(SHEETS_DIR.glob("*.html"))
    ]
    if not sheets:
        raise SystemExit(f"no .html sheets found in {SHEETS_DIR}")
    return sheets


def render_sheet(sheet: Sheet) -> BuildResult:
    document = HTML(filename=str(sheet.source)).render()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    document.write_pdf(str(sheet.output))
    size_bytes = sheet.output.stat().st_size
    return BuildResult(sheet=sheet, pages=len(document.pages), size_bytes=size_bytes)


def build_all(only: list[str] | None = None, clean: bool = False) -> list[BuildResult]:
    sheets = discover_sheets()
    if only:
        needles = {item.removeprefix("printables/").removesuffix(".pdf") for item in only}
        sheets = [s for s in sheets if s.source.stem in needles]
        found = {s.source.stem for s in sheets}
        missing = sorted(needles - found - {"."})
        if missing:
            raise SystemExit(f"unknown sheet(s): {', '.join(missing)}")
    if clean and OUTPUT_DIR.is_dir():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for sheet in sheets:
        result = render_sheet(sheet)
        relative = sheet.output.relative_to(KIT_ROOT)
        kib = result.size_bytes / 1024
        print(f"built {sheet.source.name} -> {relative} ({result.pages} page(s), {kib:.0f} KiB)")
        results.append(result)
    if not results:
        raise SystemExit("nothing matched --only")
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="build.py",
        description="Render the Tax Paperwork Organizer Kit sheets to PDF.",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="STEM",
        help="build specific sheets by file stem, e.g. --only 03-mileage-log",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="delete printables/ before building",
    )
    args = parser.parse_args(argv)
    results = build_all(only=args.only, clean=args.clean)
    total_pages = sum(result.pages for result in results)
    print(f"{len(results)} sheet(s) built into printables/ ({total_pages} pages total)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
