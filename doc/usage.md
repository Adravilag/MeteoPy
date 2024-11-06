
# Usage

This guide provides instructions on how to use **MeteoWave** for retrieving, processing, and visualizing weather data.

## Basic Workflow

1. **Fetch Weather Data**: Run the application and choose the region and date for which you want weather data.
2. **Process Data**: The application will process the raw data, converting it into a structured format for analysis.
3. **Visualize Data**: Use the map interface to interact with the weather data, viewing metrics such as temperature, wind speed, and precipitation.

## Running the Application

After completing the installation, you can run the application using the following options:

### Option 1: Run with Python Command

```bash
python src/metPy.py
```

### Option 2: Run with .bat Files

To streamline execution, use the provided `.bat` files in the `bin` directory:

- **`run_metPy.bat`**: Runs the `metPy.py` script for data processing.
- **`run_geoPy.bat`**: Runs the `geoPy.py` script for data visualization.
- **`run_tests.bat`**: Runs all tests.

> **Note**: Double-clicking the `.bat` file will automatically activate the virtual environment and execute the corresponding Python script.

## User Interface

- **Map Interaction**: Hover over regions to see specific data points.
- **Data Selection**: Use buttons to switch between metrics (e.g., temperature, wind speed).
- **Language Setting**: Change language settings in `config.json` to switch between English and Spanish.

## Additional Commands

- **Run Tests**: To verify the setup and functionality of the application:

  ```bash
  python -m unittest discover -s tests -p "*.py"
  ```

Alternatively, you can run tests using the `.bat` file:

```bash
bin\run_tests.bat
```

This file will activate the environment and execute all tests, providing a streamlined testing process.
