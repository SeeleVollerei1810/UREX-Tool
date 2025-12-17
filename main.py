import argparse
from preprocess import combine_preprocess
from utilities import save_indices_to_netcdf
from indices import tinh_chi_so_khi_hau

def main():
    # Thiết lập argparse để nhận tham số từ dòng lệnh
    parser = argparse.ArgumentParser(description="Phân tích chỉ số khí hậu ETCCDI")
    parser.add_argument('--lat_range', type=str, required=True, help="Phạm vi vĩ độ")
    parser.add_argument('--lon_range', type=str, required=True, help="Phạm vi kinh độ")
    parser.add_argument('--output_dir', type=str, required=True, help="Thư mục lưu kết quả")
    parser.add_argument('--input_data', type=str, required=True, help="Đường dẫn tệp dữ liệu đầu vào")

    args = parser.parse_args()

    # Chuyển đổi các giá trị nhập vào thành tuple
    LAT_RANGE = tuple(map(float, args.lat_range.split(',')))
    LON_RANGE = tuple(map(float, args.lon_range.split(',')))
    OUTPUT_DIR = args.output_dir
    INPUT_DATA = args.input_data

    print("===================================================")
    print("=== BẮT ĐẦU PHÂN TÍCH CHỈ SỐ KHÍ HẬU ETCCDI ===")
    print("===================================================")

    # --- BƯỚC 1: TẢI DỮ LIỆU ---
    print(f"Tải dữ liệu từ: {INPUT_DATA}")
    # Ví dụ: Tải tệp NetCDF
    import xarray as xr
    ds = xr.open_dataset(INPUT_DATA)

    # --- BƯỚC 2: TIỀN XỬ LÝ DỮ LIỆU ---
    processed_data = combine_preprocess(
        ds=ds, 
        lat_range=LAT_RANGE, 
        lon_range=LON_RANGE, 
        nan_method='keep'
    )
    
    if processed_data is None:
        print("🛑 Lỗi tiền xử lý dữ liệu. Chương trình dừng lại.")
        return

    # --- BƯỚC 3: TÍNH TOÁN CHỈ SỐ KHÍ HẬU ---
    annual_indices_ds = tinh_chi_so_khi_hau(processed_data)  # Tính toán chỉ số khí hậu từ dữ liệu đã xử lý
    
    if annual_indices_ds is not None:
        print("Các chiều trong dataset:", annual_indices_ds.dims)
    else:
        print("Dataset không có dữ liệu.")
        return

    # --- BƯỚC 4: LƯU TRỮ VÀ HOÀN TẤT ---
    print("\n--- BƯỚC 4: LƯU TRỮ VÀ HOÀN TẤT ---")
    save_indices_to_netcdf(
        ds_indices=annual_indices_ds, 
        output_filename='calculated_indices.nc',
        output_dir=OUTPUT_DIR
    )
    print("===================================================")
    print("✅ CHƯƠNG TRÌNH HOÀN TẤT THÀNH CÔNG!")
    print("===================================================")

# ----------------------------------------------------------------------
# VII. KHỐI KHỞI CHẠY (ENTRY POINT)
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
