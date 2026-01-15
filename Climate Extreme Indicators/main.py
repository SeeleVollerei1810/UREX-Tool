import argparse
from preprocess import combine_preprocess
from utilities import save_indices_to_netcdf
from indices import climate_index

def main():
    OUTPUT_DIR = '/content/drive/MyDrive/Group Project 2025/results' #link_save
    LAT_RANGE = (8.0, 24.0) #currently Vietnam
    LON_RANGE = (102.0, 110.0)
    NAN_METHOD: Literal['keep'] = 'keep'

    combined_data = load_all_data_for_analysis()

    processed_data = combine_preprocess(
        ds=combined_data,
        lat_range=LAT_RANGE,
        lon_range=LON_RANGE,
        nan_method=NAN_METHOD
    )

    annual_indices_ds = climate_index(processed_data)

    save_indices_to_netcdf(
        ds_indices=annual_indices_ds,
        output_filename='calculated_indices.nc',
        output_dir=OUTPUT_DIR
    )
    print("PROGRAM COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
