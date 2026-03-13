# Contributing

Thanks for contributing to A359012.

## Scope

Contributions are welcome in the following areas:

- sequence generation and correctness
- mathematical analysis of the sequence
- tests and reproducibility
- documentation
- website improvements and visualizations
- release and automation workflows

## Development Setup

This project currently uses Python and a static website.

### Requirements

- Python 3.13 or a close modern Python 3 version
- `pytest` for the test suite

### Common Commands

Generate the canonical CSV dataset:

```bash
python main.py
```

Generate the analysis summary:

```bash
python analyze_sequence.py
```

Run the tests:

```bash
pytest -q
```

Preview the website locally:

```bash
python -m http.server
```

Then open `http://localhost:8000`.

## Guidelines

- Keep [`A359012.csv`](./A359012.csv) as the single source dataset in the repository.
- Prefer small, reviewable pull requests.
- Update documentation when behavior, data shape, or workflows change.
- Add or update tests when changing generation logic or file formats.
- Keep the website data-driven from the canonical CSV whenever practical.
- Preserve existing licenses and attribution.

## Pull Requests

When opening a pull request, please include:

- a short summary of the change
- the reason for the change
- any data or documentation files that were regenerated
- confirmation that `pytest -q` passes locally

## Release Expectations

For release-related changes:

- update [`CHANGELOG.md`](./CHANGELOG.md)
- update [`RELEASE.md`](./RELEASE.md) when preparing a versioned release
- make sure GitHub Actions workflows still reflect the current repository structure

## Code of Collaboration

Please be respectful, constructive, and clear in both code and discussion. The project benefits most from contributions that improve correctness, reproducibility, and understandability.
