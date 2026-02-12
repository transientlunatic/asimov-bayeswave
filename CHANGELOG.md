# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of asimov-bayeswave plugin
- BayesWave pipeline integration for Asimov 0.7+
- Automatic PSD generation and collection
- XML format PSD conversion
- HTCondor DAG generation and submission
- Post-processing and result collection
- PSD suppression capabilities
- Megaplot output collection
- Comprehensive test suite
- Sphinx documentation with kentigern theme
- GitHub Actions CI/CD workflows
- `[asimov]` optional dependency group for explicit asimov integration

### Changed
- Extracted BayesWave integration from Asimov core into standalone plugin
- Removed deprecation warning from Asimov 0.6
- Updated version constraint to require asimov>=0.7
- Added installation instructions for asimov[gw]

### Fixed
- Updated dependency constraint to support asimov 0.7 (changed from `asimov>=0.6.0` to `asimov>=0.7`)

## [0.1.0] - TBD

### Added
- First public release

[Unreleased]: https://github.com/transientlunatic/asimov-bayeswave/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/transientlunatic/asimov-bayeswave/releases/tag/v0.1.0
