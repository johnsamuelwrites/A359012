# Release Notes

## 0.2.0 - 2026-03-13

This release expands the project from a generator-focused repository into a documented, testable, and deployable sequence atlas.

### Highlights

- Brute-force Python generator for the integer sequence A359012.
- Canonical CSV dataset in [`A359012.csv`](./A359012.csv) with sequence terms, split metadata, witness lengths, positions, and expansion ratios.
- Generated analytical summary in [`ANALYSIS.md`](./ANALYSIS.md).
- Interactive D3-based website in [`index.html`](./index.html) for exploring the sequence visually.
- Custom logo and favicon for the project website.
- Automated test workflow with GitHub Actions.
- Automated GitHub Pages deployment workflow for the website.
- Release, changelog, and contribution documentation for ongoing maintenance.

### Notes

- The project currently targets the search window `10 <= k < 10^6`.
- The canonical dataset currently contains 712 terms in that range.
- Version `0.1` already existed as an earlier project release; this document describes the next documented release, `0.2.0`.
