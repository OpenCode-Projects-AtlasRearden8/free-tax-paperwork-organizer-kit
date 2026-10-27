# STATUS — Free Tax Paperwork Organizer Kit

Last updated: 2026-10-27

## What was built

Six free, unbranded, print-and-file organizer sheets for tax season, rendered
from HTML/CSS sources to US Letter PDFs by a single build script. The kit is an
organizer only — every sheet carries the footer promise "this is a paper
organizer, never tax, legal, or financial advice."

Sheets (sources in `src/sheets/`, shared design system in `src/css/kit.css`):

1. **Folder labels** (`01-folder-labels.html`) — three large cut-out labels for
   income / expenses / deductions folders plus nine small labels for
   sub-folders and envelopes.
2. **W-2 & 1099 intake checklist** (`02-intake-checklist.html`) — grouped
   checklist of forms that arrive in January–spring, in plain English, with
   have-it / waiting / not-applying checkboxes; header row repeats on page 2.
3. **Mileage log continuation sheet** (`03-mileage-log.html`) — 20 log rows +
   page total on page 1; spare rows, month roll-up, and warm tip on page 2.
4. **Quarterly due-date one-pager** (`04-quarterly-dates.html`) — the
   four-times-a-year rhythm with blanks for the user's own looked-up dates,
   per-quarter done/confirmation boxes, and an explicit "official calendar is
   the source of truth" note.
5. **Give-away pile rules card** (`05-give-away-pile.html`) — four rules for
   letting paperwork go, printed twice per page to cut apart, plus a
   let-go / folder / long-keep reference table.
6. **February-to-April calendar strip** (`06-calendar-strip.html`) — landscape
   13-week strip (Feb→Apr) with a fill-in date row, milestone tracks for the
   W-2/1099 watch, intake, numbers time, filing, and the quarterly payment.

Each sheet includes a "Warm tip" box (usage habit, ADHD-friendly, low-energy)
and no branding anywhere in the PDF output (no names, no URLs, no logos).

## How to run it

```bash
pip install weasyprint        # only build dependency
python3 build.py              # builds all sheets -> printables/
python3 build.py --clean      # wipe printables/ first
python3 build.py --only 03-mileage-log      # build one sheet

python3 -m unittest discover -s tests -v    # test suite (pytest also works)
```

## Verification results (2026-10-27, this machine)

- `python3 build.py --clean` — 6 sheets built, 8 pages total, exit 0:
  - `01-folder-labels.pdf` — 1 page, ~19 KiB
  - `02-intake-checklist.pdf` — 2 pages, ~30 KiB
  - `03-mileage-log.pdf` — 2 pages, ~18 KiB
  - `04-quarterly-dates.pdf` — 1 page, ~20 KiB
  - `05-give-away-pile.pdf` — 1 page, ~21 KiB
  - `06-calendar-strip.pdf` — 1 page (landscape), ~38 KiB
- `python3 -m unittest discover -s tests -v` — **11 tests, all OK**:
  every sheet builds a PDF; no stray PDFs; valid `%PDF-` header + `%%EOF`
  trailer; ≥1 page per PDF; extractable text (>200 chars); disclaimer present
  in every PDF; zero brand words in any PDF ("unbranded" is enforced by test);
  source HTML matches the sheet list exactly; every sheet links the shared
  stylesheet; calendar strip verified landscape; build summary reports 6 sheets.
- `python3 -m pytest tests -q` — 11 passed.
- Extra manual checks: `pdfinfo` page sizes correct (612x792 portrait, 792x612
  landscape); `pdffonts` shows Atkinson Hyperlegible / Cabin / Inconsolata
  embedded; rasterized pages at 40 dpi show tinted backgrounds and text ink on
  every page (nothing renders blank); `pdftotext` spot-checks confirm sheet
  content, tips, and footers.
- `python3 -m py_compile build.py tests/test_build.py` — clean.
- Reproducible output: `build.py` sets `SOURCE_DATE_EPOCH` when unset, so
  rebuilding produces byte-identical PDFs (verified with md5sum across two
  consecutive runs); committed `printables/` artifacts no longer churn.

## Known gaps

- **Dates are deliberately generic.** The quarterly one-pager and calendar
  strip use the typical mid-April / mid-June / mid-September / mid-January
  rhythm but no hard-coded year; exact dates shift by weekend/holiday and by
  situation, so the sheets ask the user to write in their own looked-up dates.
- **US Letter only** — no A4 variant yet (would be a small `@page` addition).
- **No screen-friendly index page** — the kit is print-only by design; a
  browser-viewable catalog page could be added later.
- **WeasyPrint is required to rebuild.** Prebuilt PDFs are committed in
  `printables/`, so users only need the build step to make changes.
- **Fonts** fall back to DejaVu if Atkinson Hyperlegible / Cabin / Inconsolata
  are not installed; layout tolerates the fallback but looks best with them.
- Mileage log, quarterly page, and rules card reflect common organizing habits,
  not legal retention requirements; the sheets say so themselves.

## Repo notes

- MIT License, `Copyright (c) 2026 Asdale Dynamics, LLC` (see `LICENSE`).
- README credits Asdale Dynamics, LLC.
- No secrets, API keys, or personal data anywhere in the repo; nothing phones
  home; the build is fully local.
