# DevFlux Scraper Notes

## Source

GitHub public repository search.

## Fixed population

GitHub repositories satisfying:
topic:machine-learning stars:>50

## Sort

Recently updated / descending.

## Target URL

https://github.com/search?q=topic%3Amachine-learning+stars%3A%3E50&type=repositories&s=updated&o=desc

## Meaning of the population

DevFlux monitors publicly available GitHub repositories related to machine learning that have more than 50 stars, prioritizing the repositories that have been updated most recently.

## Fields to extract

- `repo_name` (String): Full repository identifier (`owner/repo`)
- `owner` (String): Organization or user name
- `repo_url` (URL): Canonical link to the repository
- `description` (String): Project overview text
- `language` (String): Primary programming language
- `topics` (Array): Technology tags
- `stars` (Integer/String): Star count
- `updated_at` (String/ISO): Last recorded GitHub update timestamp


# DevFlux Scraper Notes & Engineering Log

## 🎯 Target Parameters
- **Source:** GitHub public repository search
- **Query Filter:** `topic:machine-learning stars:>50`
- **Sort Order:** Recently updated / descending (`s=updated&o=desc`)
- **Target URL:** `https://github.com/search?q=topic%3Amachine-learning+stars%3A%3E50&type=repositories&s=updated&o=desc`
- **Pagination Strategy:** Automated recursive pagination via `rerun_stage()` parameterized by `max_pages` (15 pages $\approx$ 150 repositories).



## 🛠️ Technical Decisions & Troubleshooting Log
- **Single-Stage Flat Schema:** Replaced nested two-stage crawl to eliminate empty wrapper objects (`[]`) and output clean, row-level repository records.
- **Selector Precision:**
  - Excluded non-repository link prefixes (`/topics/`, `/search`, `/orgs/`, `/users/`) to prevent tag links from masquerading as repo titles.
  - Scoped description extraction strictly outside title header blocks.
  - Added K/M string parsing to star metrics.
  - **Polymorphic File Format Ingestion:**
  - Built a single-pass fallback parser in src/validator.py capable of
  - seamlessly handling standard CSV, JSON arrays, and NDJSON line-by-line
  - dumps without pipeline crashes.
- **Defensive Ingestion:**
  - Dynamic snapshot timestamps derived from filename patterns (`raw_YYYY_MM_DD.csv`) to prevent OS-level timestamp (`st_mtime`) drift across machines.
  - Non-fatal handling for null `description` and `updated_at` fields.


## 📈 Progress Tracker

| Date       | Phase / Milestone              | Status    | Key Output / Notes                                                                                    |
|------------|--------------------------------|-----------|-------------------------------------------------------------------------------------------------------|
| 2026-08-17 | Initial Scraper Conception     | Completed | Defined target population and schema requirements.                                                    |
| 2026-08-18 | Architecture Refactor          | Completed | Migrated from 2-stage nested scraper to flat card scraper.                                            |
| 2026-08-19 | Ingestion & Baseline Data      | Completed | Scraped 15 pages (150 valid ML repos).                                                                |
| 2026-08-19 | Validation & Classification    | Completed | Verified `validator.py` and categorized records using `classifier.py`.                                |
| 2026-08-19 | Change Detection Setup         | Completed | Built `change_detector.py` for star delta tracking.                                                   |
| 2026-08-20 | Day-2 Snapshot & Analytics     | Completed | Ingest 24-hr snapshot, calculate growth velocity, and generate dashboard.                             |
| 2026-08-20 | Quality Audit & UI Dashboard   | Completed | Added `data_quality.py`, unified `run_pipeline.py`, and launched Streamlit `dashboard.py`.            |
| 2026-08-21 |Snapshot 03 & Resilient Parsing	| Completed	| Ingested Day-3 snapshot; upgraded validator.py with multi-format (CSV/NDJSON) polymorphic ingestion.  |
| 2026-08-22 |Snapshot 04 & Cloud Deployment	| Completed	| Captured 4-day longitudinal history, added theme engine, and deployed public radar on Streamlit Cloud.|