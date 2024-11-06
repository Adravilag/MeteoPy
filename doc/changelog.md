
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.4] - 2024-11-06
### Added
- Added support for configurable visualization parameters in `config.json`.
- Implemented `ci.yml` GitHub Actions workflow for continuous integration.
- New `bin` batch files for running `geoPy.py` and `metPy.py` scripts with localization options.

### Changed
- Refactored `core.py` and `metPy.py` to use modular functions from `utils.py`.
- Moved `geoPy.py` and `metPy.py` to `src` directory for a clearer project structure.

### Fixed
- Corrected issues with Excel file handling in `metPy.py` to avoid file locks.

## [1.1.3] - 2024-11-05
### Added
- Integrated `.env` configuration file support for sensitive information like `GITHUB_TOKEN`.
- Added error handling for API rate limits and network issues in `data_acquisition` module.

### Changed
- Updated `architecture.md` to reflect new modules and functions.

### Fixed
- Fixed `data_processing` module to handle missing or outlier values in API data.

## [1.1.2] - 2024-11-05
### Added
- Included initial CI/CD setup for GitHub Actions.
- Introduced locale support for English and Spanish (`locales/en.json` and `locales/es.json`).

### Changed
- Refined project structure with modular directories for core, data processing, and visualization.
- Updated `config.json` to include `comunidades` list and API settings.

### Fixed
- Resolved issues with data formatting in Excel templates.

## [1.1.1] - 2024-11-05
### Added
- Implemented data visualization with dynamic map interaction in `visualization/geoPy.py`.

### Changed
- Reorganized `config` directory to include `templates` for Excel files.

## [1.1.0] - 2024-11-01
### Added
- Initial release of **MeteoWave** with modules for data acquisition, processing, and visualization.
- Basic batch files for executing Python scripts.
- Added `config.json` for centralized project configuration.
