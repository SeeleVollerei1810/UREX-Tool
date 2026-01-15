import argparse
import xarray as xr
from typing import Literal

def main():
    OUTPUT_DIR = '/content/drive/MyDrive/Group Project 2025/results' #link_save
    LAT_RANGE = (8.0, 24.0) #currently Vietnam
    LON_RANGE = (102.0, 110.0)
    NAN_METHOD: Literal['keep'] = 'keep'

    initial_data = combined_data

    processed_data = combine_preprocess(
        ds=initial_data,
        lat_range=LAT_RANGE,
        lon_range=LON_RANGE,
        nan_method=NAN_METHOD
    )

    annual_indices_ds = calculate_indices(processed_data)

    save_indices_to_netcdf(
        ds_indices=annual_indices_ds,
        output_filename='calculated_heatstress.nc',
        output_dir=OUTPUT_DIR
    )
    print("PROGRAM COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
