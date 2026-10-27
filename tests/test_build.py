"""Verify every sheet in the kit builds a valid, content-bearing, unbranded PDF."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT_ROOT))

import build  # noqa: E402

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None


EXPECTED_SHEETS = [
    "01-folder-labels",
    "02-intake-checklist",
    "03-mileage-log",
    "04-quarterly-dates",
    "05-give-away-pile",
    "06-calendar-strip",
]

DISCLAIMER_PHRASE = "never tax, legal, or financial advice"
UNBRANDED_WORDS = ["asdale", "dylan", "asdale dynamics"]


def pdf_pages(path: Path) -> int:
    if PdfReader is not None:
        return len(PdfReader(str(path)).pages)
    raw = path.read_bytes()
    import re

    counts = [int(m) for m in re.findall(rb"/Count\s+(\d+)", raw)]
    return max(counts) if counts else 0


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        proc = subprocess.run(
            [sys.executable, str(KIT_ROOT / "build.py"), "--clean"],
            cwd=str(KIT_ROOT),
            check=True,
            capture_output=True,
            text=True,
        )
        cls.build_stdout = proc.stdout
        cls.pdfs: dict[str, Path] = {
            stem: KIT_ROOT / "printables" / f"{stem}.pdf" for stem in EXPECTED_SHEETS
        }

    def test_every_sheet_has_a_pdf(self) -> None:
        for stem in EXPECTED_SHEETS:
            path = KIT_ROOT / "printables" / f"{stem}.pdf"
            self.assertTrue(path.is_file(), f"missing {path}")

    def test_no_stray_pdfs_in_printables(self) -> None:
        built = {p.stem for p in (KIT_ROOT / "printables").glob("*.pdf")}
        self.assertEqual(built, set(EXPECTED_SHEETS))

    def test_pdfs_have_correct_header_and_trailer(self) -> None:
        for stem in EXPECTED_SHEETS:
            path = KIT_ROOT / "printables" / f"{stem}.pdf"
            raw = path.read_bytes()
            self.assertTrue(raw.startswith(b"%PDF-"), f"{stem} lacks %PDF header")
            self.assertIn(b"%%EOF", raw[-64:], f"{stem} lacks %%EOF trailer")

    def test_pdfs_have_at_least_one_page(self) -> None:
        for stem in EXPECTED_SHEETS:
            path = KIT_ROOT / "printables" / f"{stem}.pdf"
            pages = pdf_pages(path)
            self.assertGreaterEqual(pages, 1, f"{stem} has {pages} pages")

    def test_pdfs_are_not_blank(self) -> None:
        if PdfReader is None:
            self.skipTest("pypdf not installed")
        for stem in EXPECTED_SHEETS:
            path = KIT_ROOT / "printables" / f"{stem}.pdf"
            reader = PdfReader(str(path))
            text = " ".join((page.extract_text() or "") for page in reader.pages)
            self.assertGreater(len(text.strip()), 200, f"{stem} extracts almost no text")

    def _pdf_text(self, stem: str) -> str:
        path = KIT_ROOT / "printables" / f"{stem}.pdf"
        reader = PdfReader(str(path))
        raw = " ".join((page.extract_text() or "") for page in reader.pages)
        return " ".join(raw.split()).lower()

    def test_pdfs_carry_the_disclaimer(self) -> None:
        if PdfReader is None:
            self.skipTest("pypdf not installed")
        for stem in EXPECTED_SHEETS:
            text = self._pdf_text(stem)
            self.assertIn(DISCLAIMER_PHRASE, text, f"{stem} missing disclaimer")

    def test_pdfs_are_unbranded(self) -> None:
        if PdfReader is None:
            self.skipTest("pypdf not installed")
        for stem in EXPECTED_SHEETS:
            text = self._pdf_text(stem)
            for word in UNBRANDED_WORDS:
                self.assertNotIn(word, text, f"{stem} contains brand word '{word}'")

    def test_src_sheets_exist_for_every_pdf(self) -> None:
        sources = sorted(p.stem for p in (KIT_ROOT / "src" / "sheets").glob("*.html"))
        self.assertEqual(sources, EXPECTED_SHEETS)

    def test_every_html_links_the_shared_stylesheet(self) -> None:
        for stem in EXPECTED_SHEETS:
            html = (KIT_ROOT / "src" / "sheets" / f"{stem}.html").read_text()
            self.assertIn('href="../css/kit.css"', html, f"{stem} missing shared css")

    def test_calendar_strip_prints_landscape(self) -> None:
        path = KIT_ROOT / "printables" / "06-calendar-strip.pdf"
        if PdfReader is not None:
            reader = PdfReader(str(path))
            box = reader.pages[0].mediabox
            self.assertGreater(float(box.width), float(box.height), "strip page not landscape")
        else:
            raw = path.read_bytes()
            self.assertIn(b"792", raw, "strip page width not landscape letter")

    def test_build_reports_expected_sheet_count(self) -> None:
        self.assertIn("6 sheet(s) built", self.build_stdout)


if __name__ == "__main__":
    unittest.main()
