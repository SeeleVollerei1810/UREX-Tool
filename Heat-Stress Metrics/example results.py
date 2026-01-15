import xarray as xr
import numpy as np
import netCDF4 as nc
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import warnings

file_path = '/content/drive/MyDrive/Group Project 2025/results/calculated_heatstress.nc'
plot_existing_tw_analysis(file_path)

print(fh.file_format)
print(fh.dimensions.keys())
print(fh.dimensions['time'])
print(fh.variables.keys())
print(fh.Conventions)
for attr in fh.ncattrs():
    print(attr, '=', getattr(fh,attr))

warnings.filterwarnings("ignore", message="All-NaN slice encountered")

def plot_existing_tw_analysis(file_path: str):
    ds = xr.open_dataset(file_path)

    if 'Tw' not in ds.variables:
        print("Error: 'Tw' variable not found in the file. Please check the variable name.")
        return

    lon = ds.lon.values
    lat = ds.lat.values
    years = ds.time.dt.year.values

    tw_data = ds['Tw']
    risk_level = xr.where(tw_data < 18, 1,
                 xr.where(tw_data < 21, 2,
                 xr.where(tw_data < 24, 3, 4)))

    risk_level = risk_level.where(~np.isnan(tw_data))

    fig = plt.figure(figsize=(15, 8))

    # --- SUBPLOT 1: HEAT RISK MAP (White background for ocean) ---
    ax1 = fig.add_subplot(1, 2, 1)

    risk_map_data = risk_level.mean(dim='time')

    colors = ['#28a745', '#ffc107', '#fd7e14', '#dc3545']
    cmap = mcolors.ListedColormap(colors)
    cmap.set_bad(color='white')

    bounds = [0.5, 1.5, 2.5, 3.5, 4.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    risk_masked = np.ma.masked_invalid(risk_map_data.values)
    plot = ax1.pcolormesh(lon, lat, risk_masked, cmap=cmap, norm=norm, shading='auto')

    cbar = fig.colorbar(plot, ax=ax1, ticks=[1, 2, 3, 4], shrink=0.7)
    cbar.ax.set_yticklabels(['Low (<18)', 'Moderate (18-21)', 'High (21-24)', 'Extreme (>24)'])
    cbar.set_label('Heat Stress Classification (Tw)')

    ax1.set_title('(a) Spatial Distribution of Tw Risk Levels', fontsize=14)
    ax1.set_xlabel('Longitude (°E)')
    ax1.set_ylabel('Latitude (°N)')
    ax1.set_aspect('equal')
    ax1.set_xlim(102, 109.5)
    ax1.set_ylim(8, 23.5)

    # --- SUBPLOT 2: Tw FREQUENCY DISTRIBUTION (HISTOGRAM) ---
    ax2 = fig.add_subplot(1, 2, 2)

    unique_years = np.unique(years)
    years_to_show = [unique_years[0], unique_years[len(unique_years)//2], unique_years[-1]]
    plot_colors = ['#1f77b4', '#2ca02c', '#d62728']

    for year, color in zip(years_to_show, plot_colors):
        data_year = ds['Tw'].sel(time=str(year)).values.flatten()
        data_clean = data_year[~np.isnan(data_year)]

        if len(data_clean) > 0:
            ax2.hist(data_clean, bins=50, alpha=0.4, label=f'Year {year}', color=color, density=True)
            ax2.axvline(np.mean(data_clean), color=color, linestyle='--', linewidth=1.5)

    ax2.axvline(18, color='gray', linestyle=':', label='Threshold (18°C)')
    ax2.axvline(24, color='darkred', linestyle='-', label='Extreme Threshold (24°C)')

    ax2.set_title('(b) Tw Frequency Distribution over Selected Years', fontsize=14)
    ax2.set_xlabel('Tw Temperature (°C)')
    ax2.set_ylabel('Probability Density (PDF)')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.show()
    ds.close()
