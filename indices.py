from utilities import _clean_coords
import xarray as xr
import numpy as np
import warnings
from typing import Dict

warnings.filterwarnings("ignore", message="All-NaN slice encountered")
INDEX_INFO: Dict[str, Dict[str, str]] = {
    "TXx": {"long_name": "Annual maximum of daily maximum temperature", "units": "°C"},
    "TNn": {"long_name": "Annual minimum of daily minimum temperature", "units": "°C"},
    "SU25": {"long_name": "Number of summer days (Tmax > 25°C)", "units": "days"},
    "TR20": {"long_name": "Number of tropical nights (Tmin > 20°C)", "units": "days"},
    "DTR": {"long_name": "Mean daily temperature range", "units": "°C"},
    "Tmean": {"long_name": "Annual mean surface air temperature", "units": "°C"},
    "Rx1day": {"long_name": "Annual maximum 1-day precipitation amount", "units": "mm"},
    "Rx5day": {"long_name": "Annual maximum consecutive 5-day precipitation amount", "units": "mm"},
    "SDII": {"long_name": "Simple daily intensity index (PRCPTOT/wet_days)", "units": "mm/day"},
    "PRCPTOT": {"long_name": "Annual total wet-day precipitation (PR > 1mm)", "units": "mm"},
    "R95p": {"long_name": "Annual total precipitation above 95th percentile", "units": "mm"},
    "R99p": {"long_name": "Annual total precipitation above 99th percentile", "units": "mm"},
}

def TXx(tasmax: xr.DataArray) -> xr.DataArray:
    return tasmax.where(~np.isnan(tasmax)).groupby('time.year').max(dim='time', skipna=True)
def TNn(tasmin: xr.DataArray) -> xr.DataArray:
    return tasmin.where(~np.isnan(tasmin)).groupby('time.year').min(dim='time', skipna=True)
def SU25(tasmax: xr.DataArray) -> xr.DataArray:
    return (tasmax > 25).groupby("time.year").sum(dim="time", skipna=True)
def TR20(tasmin: xr.DataArray) -> xr.DataArray:
    return (tasmin > 20).groupby("time.year").sum(dim="time", skipna=True)
def DTR(tasmax: xr.DataArray, tasmin: xr.DataArray) -> xr.DataArray:
    dtr_daily = tasmax - tasmin
    return dtr_daily.where(~np.isnan(dtr_daily)).groupby('time.year').mean(dim='time', skipna=True)
def Tmean(tas: xr.DataArray) -> xr.DataArray:
    return tas.where(~np.isnan(tas)).groupby('time.year').mean(dim='time', skipna=True)
def Rx1day(pr: xr.DataArray) -> xr.DataArray:
    return pr.where(~np.isnan(pr)).resample(time='YE').max(dim='time', skipna=True)
def Rx5day(pr: xr.DataArray) -> xr.DataArray:
    pr_rolling = pr.where(~np.isnan(pr)).rolling(time=5, min_periods=1).sum(skipna=True)
    return pr_rolling.resample(time='YE').max(dim='time', skipna=True)
def SDII(pr: xr.DataArray) -> xr.DataArray:
    pr_rain = pr.where(pr > 1.0)
    prcptot = pr_rain.groupby('time.year').sum(dim='time', skipna=True)
    wet_days = pr_rain.groupby('time.year').count(dim='time')
    return prcptot / wet_days
def PRCPTOT(pr: xr.DataArray) -> xr.DataArray:
    pr_rain = pr.where(pr > 1.0)
    return pr_rain.groupby('time.year').sum(dim='time', skipna=True)
def R95p(pr: xr.DataArray) -> xr.DataArray:
    pr_valid = pr.where(~np.isnan(pr))
    thr = pr_valid.quantile(0.95, dim='time', skipna=True)
    pr95 = pr_valid.where(pr_valid > _clean_coords(thr))
    return pr95.groupby('time.year').sum(dim='time', skipna=True)
def R99p(pr: xr.DataArray) -> xr.DataArray:
    pr_valid = pr.where(~np.isnan(pr))
    thr = pr_valid.quantile(0.99, dim='time', skipna=True)
    pr99 = pr_valid.where(pr_valid > _clean_coords(thr))
    return pr99.groupby('time.year').sum(dim='time', skipna=True)

def climate_index(ds: xr.Dataset) -> xr.Dataset:
    
    required_vars = ['tasmax', 'tasmin', 'tas', 'pr']
    if not all(v in ds.data_vars for v in required_vars):
        missing = [v for v in required_vars if v not in ds.data_vars]
        raise ValueError(f"Required variables are missing from the Dataset: {missing}")

    tasmax, tasmin, tas, pr = ds['tasmax'], ds['tasmin'], ds['tas'], ds['pr']
    results: Dict[str, Union[xr.DataArray, xr.Dataset]] = {}

    results["TXx"] = _clean_coords(TXx(tasmax))
    results["TNn"] = _clean_coords(TNn(tasmin))
    results["SU25"] = _clean_coords(SU25(tasmax))
    results["TR20"] = _clean_coords(TR20(tasmin))
    results["DTR"] = _clean_coords(DTR(tasmax, tasmin))
    results["Tmean"] = _clean_coords(Tmean(tas))
    results["Rx1day"] = _clean_coords(Rx1day(pr))
    results["Rx5day"] = _clean_coords(Rx5day(pr))
    results["SDII"] = _clean_coords(SDII(pr))
    results["PRCPTOT"] = _clean_coords(PRCPTOT(pr))
    results["R95p"] = _clean_coords(R95p(pr))
    results["R99p"] = _clean_coords(R99p(pr))

    ds_annual_indices = xr.Dataset(results)

    for name, da in ds_annual_indices.data_vars.items():
        if name in INDEX_INFO:
            da.name = name
            da.attrs.update(INDEX_INFO[name])
    else:
         if 'year' in ds_annual_indices.dims:
            ds_annual_indices = ds_annual_indices.rename({'year': 'time'})
            print("Đã đổi tên chiều 'year' thành 'time'.")
            
    print("ETCCDI indices calculation completed.")

    return ds_annual_indices
