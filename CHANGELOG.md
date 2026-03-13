# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog, and this project uses semantic versioning.

## [0.1.0] - 2026-03-13

### Added

- Python generator for sequence A359012 in [`A359012.py`](./A359012.py).
- CSV export pipeline in [`main.py`](./main.py).
- Canonical dataset in [`A359012.csv`](./A359012.csv).
- Analysis generator in [`analyze_sequence.py`](./analyze_sequence.py) and generated summary in [`ANALYSIS.md`](./ANALYSIS.md).
- Regression and file-output tests in [`tests/test_a359012.py`](./tests/test_a359012.py).
- Interactive website with D3 visualizations in [`index.html`](./index.html) and [`assets/`](./assets).
- Project branding with a logo and favicon.
- GitHub Actions workflow for tests in [`.github/workflows/tests.yml`](./.github/workflows/tests.yml).
- GitHub Actions workflow for GitHub Pages deployment in [`.github/workflows/deploy-site.yml`](./.github/workflows/deploy-site.yml).
- Project documentation for release notes, changelog, and contributing.

### Changed

- Consolidated the repository around a single canonical CSV source instead of maintaining duplicate CSV exports.
- Enriched the canonical CSV with derived fields such as length annotations, witness position, relative depth, and expansion ratio.
- Simplified `ANALYSIS.md` so it summarizes the dataset instead of repeating the full dataset inline.
