
# Architecture

## Overview

**MeteoWave** is a Python-based application designed to fetch, process, and visualize meteorological data, focusing on specific regions in Spain. The main objectives of the application are:
- To fetch weather data from external sources.
- To process and organize the data for visualization.
- To display the data on interactive maps with configurable visualization parameters.

This document provides an architectural overview of the project, including the main components, directory structure, and data flow across modules.

## Project Structure

The MeteoWave project follows a modular architecture, with each module dedicated to specific functionalities. Below is an overview of the directory structure and the responsibilities of each module.

```plaintext
MeteoWave/
├── bin/                     # Batch files for running scripts and setting up releases
├── config/                  # Configuration files, including settings and templates
│   ├── shp/                 # Shapefiles for geographic regions
│   └── templates/           # Excel templates for data storage
├── data/                    # Directory for storing acquired data and results
│   ├── YYYY/MM/             # Subdirectories for data organized by year and month
├── doc/                     # Documentation files
├── locales/                 # Language files for localization (e.g., en.json, es.json)
├── src/                     # Main source code directory
│   ├── core/                # Core logic and main entry point
│   ├── data_acquisition/    # Modules for fetching data from APIs
│   ├── data_processing/     # Modules for processing and cleaning data
│   ├── utils/               # Utility functions used across modules
│   └── visualization/       # Modules for data visualization
├── tests/                   # Testing directory with unit, integration, and E2E tests
│   ├── e2e_tests/           # End-to-End tests
│   ├── integration_tests/   # Integration tests
│   └── unit_tests/          # Unit tests for individual functions and modules
└── .github/                 # CI/CD workflows for GitHub Actions
```

### Module Breakdown

#### 1. `core/`
This module contains the core logic and main entry point of **MeteoWave**. It coordinates the flow of data from acquisition through to visualization.

- **Key Functions**: `menu_principal`, `procesar_datos`
- **Main Responsibilities**:
  - Orchestrating data acquisition, processing, and visualization steps.
  - Handling user interactions, such as selecting regions and dates.

#### 2. `data_acquisition/`
This module is responsible for fetching weather data from external APIs (e.g., Open Meteo).

- **Key Functions**: `obtener_fechas_disponibles_api`, `obtener_datos_meteo`
- **Main Responsibilities**:
  - Handling API requests for weather data based on location and date.
  - Managing retries and error handling for network issues.

#### 3. `data_processing/`
This module processes raw weather data, cleaning, formatting, and organizing it for storage or visualization.

- **Key Functions**: `copiar_plantilla_si_no_existe`, `cargar_excel`
- **Main Responsibilities**:
  - Data cleaning and transformation.
  - Organizing data into a structured format compatible with visualization.

#### 4. `visualization/`
The visualization module generates interactive maps to display meteorological data. It utilizes geographic data from shapefiles to render maps.

- **Key Functions**: `update_scatter`, `set_selected_data`
- **Main Responsibilities**:
  - Displaying weather data on maps with visual indicators (e.g., color and size based on metrics).
  - Allowing user interactions, such as hovering to view data values.

#### 5. `utils/`
This module contains utility functions used across various parts of the project. These functions include file handling, configuration loading, and auxiliary processes.

- **Key Functions**: `cargar_configuracion`, `cargar_traducciones`, `inicializar_directorios`
- **Main Responsibilities**:
  - Supporting data processing, file operations, and configuration management.
  - Simplifying repeated tasks across modules.

## Data Flow

The data flow in **MeteoWave** follows a logical sequence, beginning with data acquisition, moving through processing, and finally reaching visualization.

1. **Data Acquisition** (`data_acquisition/`):
   - The application fetches data from the API based on specified parameters (e.g., location, date).
   - `obtener_fechas_disponibles_api` and `obtener_datos_meteo` manage the request and retrieval of raw weather data.

2. **Data Processing** (`data_processing/`):
   - The raw data is cleaned and structured in `data_processing` before being stored or visualized.
   - Excel templates are used to organize data for historical reference and reporting.

3. **Data Storage** (`data/`):
   - The processed data is saved in the `data/` directory, organized by date and region for easy access.
   - Historical data is stored in Excel files for use in future analysis or visualization.

4. **Visualization** (`visualization/`):
   - The data is loaded into the `visualization` module to generate interactive maps.
   - Users can interact with the map to view detailed data points, and the visualization is customized based on user-selected metrics and regions.

## CI/CD Integration

The **MeteoWave** project uses GitHub Actions for continuous integration (CI) and deployment processes. The `ci.yml` workflow file in `.github/workflows/` defines automated testing triggered on each commit or pull request.

- **Steps in CI/CD Pipeline**:
  1. **Setup**: Clone the repository, set up Python, and install dependencies.
  2. **Testing**: Execute unit, integration, and E2E tests to ensure code reliability.
  3. **Deployment** (if applicable): Deploy changes if all tests pass.

## Future Improvements

1. **Expand Data Sources**: Integrate additional weather APIs for broader data coverage and redundancy.
2. **Error Handling Enhancements**: Improve error handling for API requests, especially for rate limits and timeouts.
3. **Scalability**: Adapt the architecture to handle larger datasets and multiple regions simultaneously.
4. **Advanced Visualization**: Add dynamic features, such as time-based animations and additional weather metrics for a richer user experience.

## Conclusion

The **MeteoWave** architecture is modular and scalable, enabling straightforward maintenance, testing, and future expansion. Each module is dedicated to a specific responsibility, promoting a clear data flow from acquisition through processing to visualization. CI/CD integration via GitHub Actions ensures code reliability and project quality, making **MeteoWave** a robust solution for meteorological data analysis and visualization.
