
# Installation Guide

Welcome to **MeteoWave**! This guide will walk you through the installation and initial setup of the application, including configuring important files and setting up dependencies.

## Requirements

Before starting, make sure you have:

- **Python** 3.9 or higher installed.
- Access to **Git** for cloning the repository.
- **Virtual environment** support (recommended for dependency isolation).

## Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/MeteoWave.git
cd MeteoWave
```

## Step 2: Set Up a Virtual Environment

To keep dependencies isolated and prevent conflicts, set up a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

- **On Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **On macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

## Step 3: Install Dependencies

Install the required dependencies specified in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If you need to generate the `requirements.txt` file manually, you can do so by running:

```bash
pip freeze > requirements.txt
```

## Step 4: Configure the Application

### 1. Configuration File: `config.json`

The application uses a `config.json` file located in the `config` folder to define various parameters. Here is a template of the file with explanations of each field:

```json
{
    "base_size": 10,
    "max_point_size": 500,
    "min_point_size": 5,
    "label_threshold": 400,
    "default_selected_data": "temperature_mean",
    "map_xlim": [-7.6, -1.5],
    "map_ylim": [35.8, 39],
    "shapefile_path": "config/shp/gadm41_ESP_4.shp",
    "language": "en",
    "data_directory": "data",
    "template_path": "config/templates/MeteoData.xlsx",
    "version": "1.1.4",
    "comunidades": [
        "ANDALUCIA",
        "VALENCIA",
        "CATALUÑA",
        "MADRID",
        "GALICIA"
    ],
    "api_settings": {
        "base_url": "https://api.open-meteo.com/v1/forecast",
        "daily_params": [
            "temperature_2m_max",
            "temperature_2m_min",
            "windspeed_10m_max",
            "windgusts_10m_max",
            "winddirection_10m_dominant",
            "precipitation_sum"
        ],
        "timezone": "Europe/Madrid"
    }
}
```

### 2. `.env` File

If not already created, set up a `.env` file to store sensitive information (e.g., API tokens):

```bash
GITHUB_TOKEN=your_token_here
```

> **Note:** Make sure to add your `.env` file to `.gitignore` to prevent it from being uploaded to the repository.

## Step 5: Initial Setup Script

To streamline the setup, run the `setup.bat` script (on Windows) or the equivalent shell script on macOS/Linux to create the environment, activate it, and install dependencies automatically.

```bash
setup.bat
```

This script performs the following tasks:

- Creates and activates the virtual environment.
- Installs dependencies.
- Checks for a `.env` file and prompts for manual updates if necessary.

## Step 6: Run the Application

After setup is complete, you can run the application:

```bash
python src/metPy.py
```

## Step 7: Testing the Application (Optional)

Run unit tests to verify that the application is set up correctly. If you have configured CI/CD, these tests should run automatically on each commit.

```bash
python -m unittest discover -s tests -p "*.py"
```

---

### Additional Notes

- **Language Support**: Set `"language": "en"` in `config.json` for English, or `"es"` for Spanish.
- **Git Branches**: Development should occur in the `develop` branch, while releases are merged into `main`.

---

This should cover the installation and initial configuration of **MeteoWave**. For any questions, consult the documentation or reach out to the development team.
