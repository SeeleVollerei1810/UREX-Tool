import xarray as xr
from pathlib import Path
import os
import glob

def get_drive_data_path() -> str:z
    return '/content/drive/MyDrive/Group Project 2025/data/'

def load_and_process_tas():
    base_path = get_drive_data_path()
    nc_files = glob.glob(os.path.join(base_path, '*.nc'))

    tas_ds = None

    for file_path in nc_files:
        name = Path(file_path).stem.split('_')[-1]

        if name == 'tas':
            print(f"Loading variable: {name}")
            tas_ds = xr.open_dataset(file_path, chunks={'time': -1})
            break

    if tas_ds is not None:
        tas_ds['rh'] = 0.7

        print("\nDataset processed successfully.")
        print(f"Variables in dataset: {list(tas_ds.data_vars)}")
        return tas_ds
    else:
        print("Error: Could not find file for 'tas'.")
        return None

combined_data = load_and_process_tas()
