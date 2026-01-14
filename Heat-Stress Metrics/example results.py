import numpy as np
import netCDF4 as nc
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

file_path = '/content/drive/MyDrive/Group Project 2025/results/calculated_heatstress.nc'
fh = Dataset(file_path, 'r')

print(fh.file_format)
print(fh.dimensions.keys())
print(fh.dimensions['time'])
print(fh.variables.keys())
print(fh.Conventions)
for attr in fh.ncattrs():
    print(attr, '=', getattr(fh,attr))

lat = fh.variables['lat'][:]
lon = fh.variables['lon'][:]
time_var = fh.variables['time']
heat_data = fh.variables['WBGT'][:]

d_times = nc.num2date(time_var[:], time_var.units)
years = np.array([d.year for d in d_times])

heat_mean = np.nanmean(heat_data, axis=0)

fig = plt.figure(figsize=(16, 10))

# --- SUBPLOT 1: SPATIAL DISTRIBUTION MAP ---
ax1 = fig.add_subplot(1, 2, 1)

plot = ax1.pcolormesh(lon, lat, heat_mean, cmap='RdYlBu_r', shading='auto', vmin=20, vmax=35)

cbar = fig.colorbar(plot, ax=ax1, label='WBGT Index (°C)', extend='both', shrink=0.7)

ax1.set_title('(a) Spatial Distribution of WBGT Mean (1961-2023)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Longitude (°E)')
ax1.set_ylabel('Latitude (°N)')
ax1.set_aspect('equal')
ax1.set_xlim(102, 109.5)
ax1.set_ylim(8, 23.5)

# --- SUBPLOT 2: MULTI-YEAR FREQUENCY DISTRIBUTION (HISTOGRAM) ---
ax2 = fig.add_subplot(1, 2, 2)

unique_years = np.unique(years)
years_to_plot = [unique_years[0], unique_years[len(unique_years)//2], unique_years[-1]]
colors = ['#1f77b4', '#2ca02c', '#d62728'] # Blue, Green, Red

for year, color in zip(years_to_plot, colors):
    year_idx = np.where(years == year)[0]
    year_data = heat_data[year_idx, :, :].flatten()
    clean_data = year_data[~np.isnan(year_data)]

    if len(clean_data) > 0:
        ax2.hist(clean_data, bins=40, alpha=0.4, label=f'Year {year}', color=color, density=True)
        ax2.axvline(np.mean(clean_data), color=color, linestyle='--', linewidth=1.5)

ax2.set_title('(b) WBGT Frequency Distribution Comparison', fontsize=14, fontweight='bold')
ax2.set_xlabel('Temperature (°C)')
ax2.set_ylabel('Probability Density (PDF)')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Overall Minimum WBGT: {np.nanmin(heat_mean):.2f}°C")
print(f"Overall Maximum WBGT: {np.nanmax(heat_mean):.2f}°C")

fh.close()
