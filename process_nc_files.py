from google.colab import files
import xarray as xr

# Yêu cầu người dùng tải nhiều tệp .nc lên
uploaded = files.upload()

# Duyệt qua tất cả các tệp đã tải lên và xử lý
for filename in uploaded.keys():
    print(f"Đã tải lên tệp: {filename}")
    
    # Đọc tệp NetCDF (.nc) với xarray
    ds = xr.open_dataset(filename)
    
    # Hiển thị thông tin về tệp NetCDF
    print(ds)
    
    # Bạn có thể xử lý dữ liệu từ tệp này tùy theo yêu cầu
    # Ví dụ: Truy cập một biến cụ thể trong tệp NetCDF
    # print(ds['variable_name'])  # Thay 'variable_name' bằng tên biến trong tệp .nc của bạn
