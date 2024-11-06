# Changelog - 2024-11-06

## Version 1.4.0 - Project Architecture Updates

### Summary of Changes

This update introduces significant modifications to the project structure, dependency management, and automated changelog generation. Below are detailed changes for each relevant file.

### Detailed Changes by File

#### `.gitignore`
- Added `temp` to exclude temporary files from version control.
- Adjusted the `__pycache__` entry to improve handling of Python cache files.

#### `bin/scripts/generate_changelog.py`
- **New file**: Created `generate_changelog.py` in the `bin/scripts/` directory to automate changelog generation.
- **Key functionalities**:
  - Extraction of recent commits from the repository using `git log`.
  - Retrieval of differences in each commit using `git diff`.
  - Generation and storage of a detailed Markdown file documenting changes.

#### `README.md`
- Updated documentation to reflect changes in the project structure and new automation scripts.
- Added details on environment configuration and the use of the changelog generation script.

#### `src/core.py`
- Refactored to improve modularity and facilitate interaction between modules.
- **New functions**:
  - `menu_principal()` to organize user navigation through various application options.
  - `seleccionar_comunidad()` added to allow dynamic selection of the autonomous community.

#### `config/config.json`
- Updated default configurations.
- **New parameters added**:
  - `language`: Defines the interface language.
  - `api_settings`: Contains configurations for interaction with the Open-Meteo API, such as `base_url` and `daily_params`.

#### `.github/workflows/ci.yml`
- Modified CI/CD workflow steps to integrate unit and integration tests.
- **Key changes**:
  - Removed redundant steps.
  - Updated Python version used in tests.
  - Improved setup steps for dependency installation and test execution.

#### `MeteoWave_License.txt`
- Updated license to reflect the current project version.
- Resolved version conflicts within the license file.

### Error Handling Improvements
- Added exception handling in multiple parts of the code to manage common errors, such as missing configuration files or HTTP request failures.

### General Refactoring
- Restructured directories for better project organization.
- Modularized code in `core.py`, `data_acquisition.py`, and `data_processing.py` to enhance maintainability and scalability.

---

**Note:** This update marks a significant milestone in the evolution of **MeteoWave**, focusing on automation and continuous improvement of integration and deployment processes, as well as better project organization to facilitate future expansions and collaborations.