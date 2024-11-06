
# Contributing to MeteoWave

Thank you for your interest in contributing to MeteoWave! This guide provides information on the workflow and best practices for collaborating on the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Report Issues](#how-to-report-issues)
- [Contribution Process](#contribution-process)
- [Project Structure](#project-structure)
- [Testing and CI/CD](#testing-and-cicd)
- [Code Standards](#code-standards)

## Code of Conduct

We want MeteoWave to be an inclusive and collaborative project. We ask that you are respectful and professional in all interactions with the community. Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## How to Report Issues

If you find a bug or would like to propose a new feature:
1. Check [Issues](https://github.com/username/MeteoWave/issues) to ensure that a similar issue has not already been reported.
2. Open a new issue with a detailed description of the problem or suggestion.
3. Include steps to reproduce the problem (if applicable) and relevant screenshots or error logs.

## Contribution Process

### 1. Fork the Repository

Fork the repository to your GitHub account and clone it to your machine:

```bash
git clone https://github.com/your_username/MeteoWave.git
cd MeteoWave
```

### 2. Create a Branch for Your Contribution

Use the `develop` branch for development. Create a new branch from `develop` with a descriptive name, for example:

```bash
git checkout -b feature/new-feature develop
```

**Note:** All development should be done in the `develop` branch. The `main` branch is reserved for deployment and release purposes.

### 3. Make Changes and Add Tests

Make the necessary changes in the code and ensure that:
- The code is documented and follows the [Code Standards](#code-standards).
- You add or update tests in `tests/` and `integration_tests/` as appropriate.

### 4. Run the Tests

Run all tests locally before submitting your contribution:

```bash
python -m unittest discover -s tests
python -m unittest discover -s integration_tests
```

### 5. Create a Pull Request (PR)

1. Push your changes to your forked repository.
2. Open a *Pull Request* to the `develop` branch in the main repository.
3. In the PR, provide a clear description of the changes made and their purpose.

The maintenance team will review the PR and may suggest changes before approval.

## Project Structure

- `bin/`: Batch scripts to facilitate running project scripts.
- `config/`: Configuration files and data templates.
- `data/`: Test data and generated data storage.
- `locales/`: Translation files for project localization.
- `src/`: Main source code.
  - `core/`: Core project logic.
  - `data_acquisition/`: Functions to retrieve data from the Open Meteo API.
  - `data_processing/`: Data processing functions.
  - `utils/`: Utility or helper functions.
  - `visualization/`: Code for visualizations and graphics.
- `tests/`: Unit, integration, and end-to-end tests.

## Testing and CI/CD

The project has a CI/CD workflow set up in GitHub Actions that:
- Runs unit and integration tests automatically when pushing or opening a PR to `develop` or `main`.
- Verifies that all dependencies and configurations are up-to-date.

Please check the CI/CD logs in your PR to ensure that your changes pass all tests.

## Code Standards

To maintain clean and maintainable code:
- **PEP 8**: Follow Python's style guide.
- **Documentation**: Document all key functions and classes.
- **Commit Messages**: Use descriptive commit messages, e.g., `fix: correct error in community selection`.
- **Type Hinting**: Use type hints where possible to improve readability and maintainability.

## Questions

If you have any questions, feel free to open an issue or contact the maintenance team. Thank you for contributing to MeteoWave!
