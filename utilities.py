import xarray as xr
import os
from pathlib import Path

def _clean_coords(da: xr.DataArray) -> xr.DataArray:
    if 'quantile' in da.coords:
        da = da.drop_vars('quantile', errors='ignore')
    if 'quantile' in da.dims:
        da = da.isel(quantile=0, drop=True)
    return da

def save_indices_to_netcdf(ds_indices: xr.Dataset, output_filename: str, output_dir: str) -> str:

    os.makedirs(output_dir, exist_ok=True)
    output_path = Path(output_dir) / output_filename

    ds_indices.attrs["title"] = "Annual ETCCDI Climate Indices"
    ds_indices.attrs["Conventions"] = "CF-1.7"

    try:
        ds_indices.to_netcdf(output_path)
        print(f"\n Save {len(ds_indices.data_vars)} Success indicators at: {output_path.resolve()}")
        return str(output_path.resolve())
    except Exception as e:
        print(f" Error saving NetCDF file: {e}")
        return None
