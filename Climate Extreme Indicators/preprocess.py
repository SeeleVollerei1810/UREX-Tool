import xarray as xr
import numpy as np
from typing import Tuple, Literal


def normalize_temperature(ds: xr.Dataset) -> xr.Dataset:
    for var in ds.data_vars:
        if 'tas' in var.lower():
            data = ds[var]
            data = data.where((data < 1e10) & (data > -1e10))
            units = data.attrs.get('units', '').lower()
            if units.startswith('k'):
                data = data - 273.15
                data.attrs['units'] = '°C'
            ds[var] = data
    print("Temperatures normalized (to °C) and spike errors removed.")
    return ds

def spatial_subset(ds: xr.Dataset, lat_range: Tuple[float, float], lon_range: Tuple[float, float], verbose: bool = True) -> xr.Dataset:
    lat_min, lat_max = lat_range
    lon_min, lon_max = lon_range
    ds_sel = ds.sel(lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max))
    if verbose:
        print(f"Cut area: lat={lat_min}–{lat_max}, lon={lon_min}–{lon_max}")
    return ds_sel

def time_subset(ds: xr.Dataset, verbose: bool = True) -> xr.Dataset:
    years = np.unique(ds["time"].dt.year.values)
    start_year = int(years.min())
    end_year   = int(years.max())
    ds_sel = ds.sel(time=slice(f"{start_year}-01-01", f"{end_year}-12-31"))
    if verbose:
        print(f"Filtered time data automatically: {start_year} → {end_year}")
    return ds_sel

def handle_nan(ds: xr.Dataset, method: Literal['keep'] = 'keep') -> xr.Dataset:
    if method == 'keep':
        for var in ds.data_vars:
            arr = ds[var]
            arr = arr.where(~np.isnan(arr), np.nan)
            if 'time' in arr.dims:
                mask_static_zero = (arr.mean(dim='time', skipna=True) == 0)
                arr = arr.where(~mask_static_zero)
            ds[var] = arr
    return ds

def combine_preprocess(ds: xr.Dataset, lat_range: Tuple[float, float], lon_range: Tuple[float, float], nan_method: Literal['keep'] = 'keep') -> xr.Dataset:
    ds = normalize_temperature(ds)
    ds = spatial_subset(ds, lat_range, lon_range)
    ds = time_subset(ds)
    ds = handle_nan(ds, nan_method)
    print("Preprocessing completed!")
    return ds
