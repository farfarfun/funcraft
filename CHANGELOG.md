# Changelog

## [Unreleased]

### Changed

- **Breaking:** renamed the import name and PyPI package name from `notecraft` to `funcraft`
  to match the repository name. Anyone doing `import notecraft` or `pip install notecraft`
  must switch to `import funcraft` / `pip install funcraft`.
- The old `notecraft` PyPI package will receive one final release forwarding to `funcraft`
  (manual follow-up by the repo owner). Note: as of this change, neither `notecraft` nor
  `funcraft` has actually been published to PyPI yet — source install only.
