# An Integrated Toolbox for Assessing and Enhancing Urban Resilience to Climate Extremes

## Introduction
This project aims to develop an integrated computational toolbox to explore climate-biosphere feedback processes and assess urban resilience to climate extremes.

In the context of rapid urbanization and global warming, this toolbox provides a workflow to process climate data, compute extreme indicators, and visualize risks associated with heat stress and extreme rainfall.

## How to Run
Follow these steps to set up the environment, configure your data, and obtain the results.
### 1. Installation
First, clone the repository to your local machine or Google Colab environment:
- git clone https://github.com/SeeleVollerei1810/Group_Project_2025.git
- cd Group_Project_2025

Ensure you have the required libraries installed:
- pip install numpy pandas xarray netCDF4 matplotlib

If you want to calculate Climate Indices or Heat Stress Metrics, navigate to the corresponding directory:
- cd Climate Extreme Indicators
- cd Heat-Stress Metrics
### 2. Configuration
Before running, you must update the file paths and study area parameters to match your dataset.
- **Step 1: Set Data Path**
    - Open `input.py` and locate the `get_drive_data_path` function.
    - Change the default_path to the folder containing your .nc files:
```
def get_drive_data_path() -> str:
    # CHANGE THIS to YOUR actual data folder path
    default_path = '/content/drive/MyDrive/Group Project 2025/data/'
    return default_path
```
- **Step 2: Set Study Area**
    - Open `main.py`, find the `main()` function and update the following coordinates:
```
def main():
    OUTPUT_DIR = '/content/drive/MyDrive/Group Project 2025/results'
    # Define YOUR study area boundaries
    LAT_RANGE = (8.0, 24.0)
    LON_RANGE = (102.0, 110.0)
    NAN_METHOD: Literal['keep'] = 'keep'
```
### 3. Visualization
Use the provided `example_results.py` script to generate spatial maps and frequency distributions for any calculated index.
- **Step 1: Update Input File**
    - Open `example results.py` and modify the `file_path` to point to your result NetCDF file (e.g., `calculated_indices.nc` or `calculated_heatstress.nc`).
```
# CHANGE THIS to YOUR result file path
file_path = '/content/drive/MyDrive/Group Project 2025/results/calculated_indices.nc'
```
- **Step 2: Select Variable**
    - Update the variable key to the specific index you want to plot (e.g., `'TNn'`, `'TXx'`, `'WBGT'`, `'Tw'`).
```
# Change 'WBGT' or 'TNn' to your desired variable name found in the file
tnn_data = fh.variables['TNn'][:]
tw_data = ds['Tw']
```

    - Also, update the variable key in other line to match the specific index

## Key Features
The toolbox focuses on the following primary objectives:
- **Climate Extreme Indicators (ETCCDI):** Computing indices such as `TXx`, `TNn`, `R95p`, and `PRCPTOT` to assess long-term temperature and rainfall trends.
- **Heat-Stress Metrics:** Calculating human heat exposure metrics like Wet-Bulb Temperature (`Tw`) and Wet-Bulb Globe Temperature (`WBGT`).

## Technology Stack
The project is implemented using the **Python** ecosystem with the following key libraries:
### Core Dependencies
- **Xarray:** The backbone of the toolbox. Used for N-dimensional data manipulation, labeling, and climate index calculation.
- **NumPy:** Efficient numerical computation and array operations.
- **Pandas:** Handles datetime indexing, time resampling ('YE'), and time-series logic underlying Xarray.
- **NetCDF4:** The essential backend engine for reading and writing `.nc` climate data files.
### Standard Libraries & Utilities
- **Typing:** Extensive use of Type Hints (`List`, `Dict`, `Tuple`, `Literal`) ensures code reliability and clarity.
- **Pathlib / Glob:** Robust cross-platform file path handling and batch processing.
- **Argparse:** Command-line argument parsing for flexible execution.

## Indices
The toolbox computes a comprehensive set of **24 ETCCDI climate indices** and **2 Heat stress metrics** covering temperature extremes, heatwaves, heavy rainfall, drought durations and human heat stress.
### 1. Temperature Indices (11 Indices)
| Index | Unit | Description | Threshold / Logic |
| :--- | :--- | :--- | :--- |
| **`TXx`** | **°C** | Annual maximum of daily maximum temperature | Absolute Max |
| **`TXn`** | **°C** | Annual minimum of daily maximum temperature | Min of Max |
| **`TNx`** | **°C** | Annual maximum of daily minimum temperature | Max of Min |
| **`TNn`** | **°C** | Annual minimum of daily minimum temperature | Absolute Min |
| **`Tmean`**| **°C** | Annual Mean surface air temperature | Mean Value |
| **`DTR`** | **°C** | Mean daily temperature range | Tmax - Tmin |
| **`SU25`** | **Days** | Number of Summer Days | Tmax > 25°C |
| **`TR20`** | **Days** | Number of Tropical Nights | Tmin > 20°C |
| **`FDD`** | **Days** | Frost days (Cold stress) | Tmin ≤ 0°C |
| **`WSDI`** | **Days** | Warm Spell Duration Index | Heatwave Duration |
| **`CSDI`** | **Days** | Cold Spell Duration Index | Cold Spell Duration |
### 2. Precipitation Indices (13 Indices)
| Index | Unit | Description | Threshold / Logic |
| :--- | :--- | :--- | :--- |
| **`Rx1day`** | **mm** | Annual maximum 1-day precipitation | Max 1-day rain |
| **`Rx5day`** | **mm** | Annual maximum consecutive 5-day precipitation | Max 5-day rain |
| **`SDII`** | **mm/day**| Simple Daily Intensity Index | Rain rate / Wet days |
| **`PRCPTOT`**| **mm** | Annual total wet-day precipitation | Total Rain (>1mm) |
| **`RRR`** | **mm** | Annual total precipitation in the wettest period | Wettest Period |
| **`R95p`** | **mm** | Precipitation above 95th percentile | Very Wet Days |
| **`R99p`** | **mm** | Precipitation above 99th percentile | Extremely Wet Days |
| **`CWD`** | **Days** | Consecutive Wet Days | Duration (Wet) |
| **`CDD`** | **Days** | Consecutive Dry Days | Duration (Dry) |
| **`R1mm`** | **Days** | Number of wet days (Rain ≥ 1mm) | P ≥ 1mm |
| **`R10mm`** | **Days** | Number of heavy precipitation days | P ≥ 10mm |
| **`R20mm`** | **Days** | Number of very heavy precipitation days | P ≥ 20mm |
| **`R50mm`** | **Days** | Number of violent precipitation days | P ≥ 50mm |
### 3. Heat-Stress Metrics (2 Indices)
| Index | Unit | Description | Threshold / Logic |
| :--- | :--- | :--- | :--- |
| **`Tw`** | **°C** | Wet-bulb Temperature | f(Temp, Humidity, Pressure) |
| **`WBGT`** | **°C** | Wet-Bulb Globe Temperature | ISO Heat Stress Standard |

## Author
**University of Science and Technology of Hanoi (USTH)** *Department of Space and Earth Sciences*
| Name | Student ID |
| :--- | :--- |
| **Pham Minh Thu** | BA12-170 |
| **Nguyen Ngoc Quan** | 22TA13002 |
| **Le Van Ben** | 22BA12046 |
| **Nguyen Quang Nam** | 2410682 |

**Supervisor:** Dr. Nguyen Xuan Thanh
