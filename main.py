from input import load_all_data_for_analy
from preoprocess import combine_preprocess
from utilities import save_indices_to_netcdf
from indices import tinh_chi_so_khi_hau

def main():
    # --- THAM SỐ CẤU HÌNH ---
    OUTPUT_DIR = '/content/drive/MyDrive/Group Project 2025/results' # Thư mục lưu kết quả
    LAT_RANGE = (8.0, 24.0) # Vĩ độ (ví dụ: phạm vi Việt Nam)
    LON_RANGE = (102.0, 110.0) # Kinh độ
    NAN_METHOD: Literal['keep'] = 'keep' 

    print("===================================================")
    print("=== BẮT ĐẦU PHÂN TÍCH CHỈ SỐ KHÍ HẬU ETCCDI ===")
    print("===================================================")
    
    # --- BƯỚC 1: TẢI VÀ KẾT HỢP DỮ LIỆU ---
    combined_data = load_all_data_for_analysis() 
    
    if combined_data is None:
        print("🛑 Không thể tải dữ liệu. Chương trình dừng lại.")
        return

    # --- BƯỚC 2: TIỀN XỬ LÝ DỮ LIỆU ---
    processed_data = combine_preprocess(
        ds=combined_data, 
        lat_range=LAT_RANGE, 
        lon_range=LON_RANGE, 
        nan_method=NAN_METHOD
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
