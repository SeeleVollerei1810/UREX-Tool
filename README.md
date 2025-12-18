# An Integrated Toolbox for Assessing and Enhancing Urban Resilience to Climate Extremes

## Introduction
This project aims to develop an integrated computational toolbox to explore climate-biosphere feedback processes and assess urban resilience to climate extremes.

In the context of rapid urbanization and global warming, this toolbox provides a workflow to process climate data, compute extreme indicators, and visualize risks associated with heat stress and extreme rainfall.

## Key Features
The toolbox focuses on the following primary objectives:
* **Climate Extreme Indicators (ETCCDI):** Computing indices such as `TXx`, `TNn`, `R95p`, and `PRCPTOT` to assess long-term temperature and rainfall trends.
* **Heat-Stress Metrics:** Calculating human heat exposure metrics like Wet-Bulb Temperature (`Tw`) and Wet-Bulb Globe Temperature (`WBGT`).

## Technology Stack
The project is implemented using the **Python** ecosystem with the following key libraries:
### Core Dependencies
* **Xarray** The backbone of the toolbox. Used for N-dimensional data manipulation, labeling, and climate index calculation.
* **NumPy** efficient numerical computation and array operations.
* **Pandas** Handles datetime indexing, time resampling ('YE'), and time-series logic underlying Xarray.
* **NetCDF4** The essential backend engine for reading and writing `.nc` climate data files.
### Standard Libraries & Utilities
* **Typing:** Extensive use of Type Hints (`List`, `Dict`, `Tuple`, `Literal`) ensures code reliability and clarity.
* **Pathlib / Glob:** Robust cross-platform file path handling and batch processing.
* **Argparse:** Command-line argument parsing for flexible execution.

## Climate Indices
The toolbox computes a comprehensive set of **24 ETCCDI climate indices** covering temperature extremes, heatwaves, heavy rainfall, and drought durations.
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

## Author
**University of Science and Technology of Hanoi (USTH)** *Department of Space and Earth Sciences*
| Name | Student ID |
| :--- | :--- |
| **Pham Minh Thu** | BA12-170 |
| **Nguyen Ngoc Quan** | 22TA13002 |
| **Le Van Ben** | 22BA12046 |
| **Nguyen Quang Nam** | 2410682 |

**Supervisor:** Dr. Nguyen Xuan Thanh
