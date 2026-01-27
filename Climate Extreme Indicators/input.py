import xarray as xr
from pathlib import Path
import os
import glob

def get_drive_data_path() -> str:
    default_path = '/content/drive/MyDrive/Group Project 2025/data/'
    return default_path

def load_all_datasets_dynamically():
    base_path = get_drive_data_path()  
    nc_files = glob.glob(os.path.join(base_path, '*.nc'))

    datasets = {}
    for file_path in nc_files:

            name = Path(file_path).stem.split('_')[-1]
            ds = xr.open_dataset(file_path, chunks={'time': -1})
            datasets[name] = ds

    print("\nTotal number of datasets downloaded:", len(datasets))
    return datasets
    
def combine_datasets(datasets):
    priority_vars = ['tas', 'tasmax', 'tasmin', 'pr']
    datasets_to_merge = [datasets[name] for name in priority_vars if name in datasets]

    merged = xr.merge(datasets_to_merge, compat='override', join='outer')
    print(f"\nDataset has been combined. Variables:{list(merged.data_vars)}")
    return merged

def load_all_data_for_analysis():
    all_datasets = load_all_datasets_dynamically()
    combined_data = combine_datasets(all_datasets)

    return combined_data

