# Free Tax Paperwork Organizer Kit

Six free print-and-file sheets that hold tax season by the hand. No signups, no
accounts, no email gates: the finished PDFs sit in `printables/`, ready to print.

**An organizer, never tax advice.** These sheets are places to *put* paperwork,
not places to learn what the law wants from you. Every sheet says so on its face,
and every sheet is unbranded, so your folders look like yours, not ours.

## What is in the kit

| Sheet | File | What it does |
| --- | --- | --- |
| 1 | `printables/01-folder-labels.pdf` | Big cut-out labels for the three folders that hold a tax year (income / expenses / deductions) plus nine small labels for sub-folders and envelopes. |
| 2 | `printables/02-intake-checklist.pdf` | The W-2-and-1099 unpacking list: every form that might arrive, in plain English, with have-it / waiting / not-applying boxes. |
| 3 | `printables/03-mileage-log.pdf` | A mileage log continuation page: twenty rows per page, a spare-rows page, and a month roll-up strip. Print as many as the year needs. |
| 4 | `printables/04-quarterly-dates.pdf` | The four-dates-a-year rhythm on one page, with blanks for your own looked-up dates and a confirmation box per quarter. |
| 5 | `printables/05-give-away-pile.pdf` | The rules card for letting paperwork go: two identical cards per page, one for the file cabinet and one for the desk. |
| 6 | `printables/06-calendar-strip.pdf` | February-to-April on one landscape strip: thirteen weeks, your dates along the top, milestones marked where they usually land. |

Every sheet carries a **Warm tip** box — one small, kind habit that makes the
sheet easier to live with — and the same footer promise: *this is a paper
organizer, never tax, legal, or financial advice.*

## Printing notes

- Paper size is US Letter, portrait except Sheet 6 (landscape).
- Sheet 1 works best on cardstock if you have it; plain paper plus tape works fine.
- Sheet 5 prints two cards per page on purpose: cut along the dashed line.
- The tinted colors print fine in grayscale, too — nothing in the kit needs color ink.

## Build it yourself

The PDFs are generated from HTML/CSS sources in `src/` by one script:

```bash
pip install weasyprint     # the only build dependency
python3 build.py           # builds every sheet into printables/
python3 build.py --clean   # wipes printables/ first
python3 build.py --only 03-mileage-log   # rebuild one sheet
```

## Tests

The test suite builds the whole kit and then verifies that every sheet produced
a valid, non-blank, unbranded PDF (correct header/trailer, at least one page,
extractable text, the disclaimer present, and no brand words anywhere):

```bash
python3 -m unittest discover -s tests -v
```

pytest runs the same suite if you prefer it: `python3 -m pytest tests -q`.
Tests also use `pypdf` when it is installed (`pip install pypdf`) for deeper
page-count and text checks; without it they fall back to structural checks.

## Who this is for

Anyone whose tax paperwork pile feels bigger than they are right now —
especially folks who like low-energy, ADHD-friendly, one-small-step systems.
Print the sheets, tape the labels, and let the folders do the remembering.

## Credits and license

Made by [Asdale Dynamics, LLC](https://dylanasdale.github.io) — beginner-friendly
AI education and practical, tested tools. Released under the MIT License
(see `LICENSE`). No personal data, secrets, or tracking anywhere in this kit:
everything runs locally, and the PDFs you build are yours alone.

*One more time, because it matters: this kit organizes paper. It does not give
tax, legal, or financial advice, and official government sources are the final
word on dates, rules, and requirements.*
