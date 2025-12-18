from utilities import _clean_coords
import xarray as xr
import numpy as np
import warnings
from typing import Dict, Union

warnings.filterwarnings("ignore", message="All-NaN slice encountered")

INDEX_INFO: Dict[str, Dict[str, str]] = {
    "TXx": {"long_name": "Annual maximum of daily maximum temperature", "units": "°C"},
    "TXn": {"long_name": "Annual minimum of daily maximum temperature", "units": "°C"},
    "TNx": {"long_name": "Annual maximum of daily minimum temperature", "units": "°C"},
    "TNn": {"long_name": "Annual minimum of daily minimum temperature", "units": "°C"},
    "DTR": {"long_name": "Mean daily temperature range", "units": "°C"},
    "SU25": {"long_name": "Number of summer days (Tmax > 25°C)", "units": "days"},
    "TR20": {"long_name": "Number of tropical nights (Tmin > 20°C)", "units": "days"},
    "Tmean": {"long_name": "Annual mean surface air temperature", "units": "°C"},
    "Rx1day": {"long_name": "Annual maximum 1-day precipitation amount", "units": "mm"},
    "Rx5day": {"long_name": "Annual maximum consecutive 5-day precipitation amount", "units": "mm"},
    "SDII": {"long_name": "Simple daily intensity index (PRCPTOT/wet_days)", "units": "mm/day"},
    "PRCPTOT": {"long_name": "Annual total wet-day precipitation (PR > 1mm)", "units": "mm"},
    "R95p": {"long_name": "Annual total precipitation above 95th percentile", "units": "mm"},
    "R99p": {"long_name": "Annual total precipitation above 99th percentile", "units": "mm"},
    "CWD": {"long_name": "Consecutive wet days", "units": "days"},
    "CDD": {"long_name": "Consecutive dry days", "units": "days"},
    "R10mm": {"long_name": "Number of days with precipitation ≥ 10mm", "units": "days"},
    "R20mm": {"long_name": "Number of days with precipitation ≥ 20mm", "units": "days"},
    "WSDI": {"long_name": "Warm Spell Duration Index", "units": "days"},
    "CSDI": {"long_name": "Cold Spell Duration Index", "units": "days"},
    "R1mm": {"long_name": "Number of days with precipitation ≥ 1mm", "units": "days"},
    "RRR": {"long_name": "Annual total precipitation in the wettest period", "units": "mm"},
    "FDD": {"long_name": "Frost days (Tmin ≤ 0°C)", "units": "days"},
    "R50mm": {"long_name": "Number of days with precipitation ≥ 50mm", "units": "days"},
}

def TXx(tasmax: xr.DataArray) -> xr.DataArray:
    return tasmax.where(~np.isnan(tasmax)).groupby('time.year').max(dim='time', skipna=True)

def TXn(tasmax: xr.DataArray) -> xr.DataArray:
    return tasmax.where(~np.isnan(tasmax)).groupby('time.year').min(dim='time', skipna=True)

def TNx(tasmin: xr.DataArray) -> xr.DataArray:
    return tasmin.where(~np.isnan(tasmin)).groupby('time.year').max(dim='time', skipna=True)

def TNn(tasmin: xr.DataArray) -> xr.DataArray:
    return tasmin.where(~np.isnan(tasmin)).groupby('time.year').min(dim='time', skipna=True)

def DTR(tasmax: xr.DataArray, tasmin: xr.DataArray) -> xr.DataArray:
    dtr_daily = tasmax - tasmin
    return dtr_daily.where(~np.isnan(dtr_daily)).groupby('time.year').mean(dim='time', skipna=True)

def SU25(tasmax: xr.DataArray) -> xr.DataArray:
    return (tasmax > 25).groupby("time.year").sum(dim="time", skipna=True)

def TR20(tasmin: xr.DataArray) -> xr.DataArray:
    return (tasmin > 20).groupby("time.year").sum(dim="time", skipna=True)

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

def CWD(pr: xr.DataArray) -> xr.DataArray:
    return pr.where(pr > 1.0).rolling(time=5, min_periods=1).count().resample(time='YE').max(dim='time', skipna=True)

def CDD(pr: xr.DataArray) -> xr.DataArray:
    return pr.where(pr == 0).rolling(time=5, min_periods=1).count().resample(time='YE').max(dim='time', skipna=True)

def R10mm(pr: xr.DataArray) -> xr.DataArray:
    return (pr >= 10).groupby("time.year").sum(dim="time", skipna=True)

def R20mm(pr: xr.DataArray) -> xr.DataArray:
    return (pr >= 20).groupby("time.year").sum(dim="time", skipna=True)

def WSDI(tasmax: xr.DataArray) -> xr.DataArray:
    return tasmax.where(tasmax > 30).groupby("time.year").sum(dim="time", skipna=True)

def CSDI(tasmin: xr.DataArray) -> xr.DataArray:
    return tasmin.where(tasmin < 0).groupby("time.year").sum(dim="time", skipna=True)

def R1mm(pr: xr.DataArray) -> xr.DataArray:
    return (pr >= 1).groupby("time.year").sum(dim="time", skipna=True)

def RRR(pr: xr.DataArray) -> xr.DataArray:
    return pr.where(pr > 1).rolling(time=7).sum().resample(time="YE").max(dim="time", skipna=True)

def FDD(tasmin: xr.DataArray) -> xr.DataArray:
    return (tasmin <= 0).groupby("time.year").sum(dim="time", skipna=True)

def R50mm(pr: xr.DataArray) -> xr.DataArray:
    return (pr >= 50).groupby("time.year").sum(dim="time", skipna=True)

def climate_index(ds: xr.Dataset) -> xr.Dataset:
    required_vars = ['tasmax', 'tasmin', 'tas', 'pr']
    if not all(v in ds.data_vars for v in required_vars):
        missing = [v for v in required_vars if v not in ds.data_vars]
        raise ValueError(f"Required variables are missing from the dataset: {missing}")

    tasmax, tasmin, tas, pr = ds['tasmax'], ds['tasmin'], ds['tas'], ds['pr']
    results: Dict[str, Union[xr.DataArray, xr.Dataset]] = {}

    results["TXx"] = _clean_coords(TXx(tasmax))
    results["TXn"] = _clean_coords(TXn(tasmax))
    results["TNx"] = _clean_coords(TNx(tasmin))
    results["TNn"] = _clean_coords(TNn(tasmin))
    results["DTR"] = _clean_coords(DTR(tasmax, tasmin))
    results["SU25"] = _clean_coords(SU25(tasmax))
    results["TR20"] = _clean_coords(TR20(tasmin))
    results["Tmean"] = _clean_coords(Tmean(tas))
    results["Rx1day"] = _clean_coords(Rx1day(pr))
    results["Rx5day"] = _clean_coords(Rx5day(pr))
    results["SDII"] = _clean_coords(SDII(pr))
    results["PRCPTOT"] = _clean_coords(PRCPTOT(pr))
    results["R95p"] = _clean_coords(R95p(pr))
    results["R99p"] = _clean_coords(R99p(pr))
    results["CWD"] = _clean_coords(CWD(pr))
    results["CDD"] = _clean_coords(CDD(pr))
    results["R10mm"] = _clean_coords(R10mm(pr))
    results["R20mm"] = _clean_coords(R20mm(pr))
    results["WSDI"] = _clean_coords(WSDI(tasmax))
    results["CSDI"] = _clean_coords(CSDI(tasmin))
    results["R1mm"] = _clean_coords(R1mm(pr))
    results["RRR"] = _clean_coords(RRR(pr))
    results["FDD"] = _clean_coords(FDD(tasmin))
    results["R50mm"] = _clean_coords(R50mm(pr))

    ds_annual_indices = xr.Dataset(results)

    for name, da in ds_annual_indices.data_vars.items():
        if name in INDEX_INFO:
            da.name = name
            da.attrs.update(INDEX_INFO[name])

    if 'time' not in ds_annual_indices.coords:
        if 'year' in ds_annual_indices.dims:
            ds_annual_indices = ds_annual_indices.rename({'year': 'time'})

    print("ETCCDI indices calculation completed.")
    return ds_annual_indices
