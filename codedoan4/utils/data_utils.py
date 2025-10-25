import pandas as pd
import json
import os

# HÀM CHUNG: Kiểm tra file, sheet, dữ liệu
def kiem_tra_file_ton_tai(duong_dan):
    """Kiểm tra file có tồn tại không."""
    if not os.path.exists(duong_dan):
        raise FileNotFoundError(f" Không tìm thấy file: {duong_dan}")

def kiem_tra_cot_bat_buoc(df, cot_bat_buoc, ten_sheet):
    """Kiểm tra các cột bắt buộc có trong DataFrame không."""
    thieu = [c for c in cot_bat_buoc if c not in df.columns]
    if thieu:
        raise ValueError(f" Sheet '{ten_sheet}' thiếu cột bắt buộc: {', '.join(thieu)}")

def kiem_tra_rong(df, ten_sheet):
    """Kiểm tra sheet có dữ liệu không."""
    if df.empty:
        raise ValueError(f" Sheet '{ten_sheet}' trống, không có dữ liệu nào.")

# ĐỌC FILE EXCEL (ĐĂNG NHẬP)
def doc_du_lieu_dang_nhap_excel(duong_dan, ten_sheet="Dangnhap"):
    kiem_tra_file_ton_tai(duong_dan)
    try:
        df = pd.read_excel(duong_dan, sheet_name=ten_sheet)
    except ValueError:
        raise ValueError(f" Không tìm thấy sheet '{ten_sheet}' trong file Excel.")
    df.columns = df.columns.str.strip().str.lower()
    kiem_tra_cot_bat_buoc(df, ['email', 'matkhau', 'ketquamongdoi'], ten_sheet)
    kiem_tra_rong(df, ten_sheet)
    df = df.fillna("")
    return [tuple(row) for row in df[['email', 'matkhau', 'ketquamongdoi']].values.tolist()]


# ĐỌC FILE CSV (ĐĂNG NHẬP)
def doc_du_lieu_dang_nhap_csv(duong_dan):
    kiem_tra_file_ton_tai(duong_dan)
    df = pd.read_csv(duong_dan)
    df.columns = df.columns.str.strip().str.lower()
    kiem_tra_cot_bat_buoc(df, ['email', 'matkhau', 'ketquamongdoi'], 'CSV')
    kiem_tra_rong(df, 'CSV')
    df = df.fillna("")
    return [tuple(row) for row in df[['email', 'matkhau', 'ketquamongdoi']].values.tolist()]

# ĐỌC FILE JSON (ĐĂNG NHẬP)
def doc_du_lieu_dang_nhap_json(duong_dan):
    kiem_tra_file_ton_tai(duong_dan)
    with open(duong_dan, encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        raise ValueError(f" File JSON '{duong_dan}' trống hoặc không có dữ liệu.")
    df = pd.DataFrame(data).fillna("")
    kiem_tra_cot_bat_buoc(df, ['email', 'matkhau', 'ketquamongdoi'], 'JSON')
    return list(df.itertuples(index=False, name=None))

# ĐỌC FILE EXCEL (ĐĂNG KÝ)
def doc_du_lieu_dang_ky_excel(duong_dan, ten_sheet="Dangky"):
    kiem_tra_file_ton_tai(duong_dan)
    try:
        df = pd.read_excel(duong_dan, sheet_name=ten_sheet)
    except ValueError:
        raise ValueError(f" Không tìm thấy sheet '{ten_sheet}' trong file Excel.")
    df.columns = df.columns.str.strip().str.lower()
    kiem_tra_cot_bat_buoc(df, ['tentaikhoan', 'email', 'matkhau', 'ketquamongdoi'], ten_sheet)
    kiem_tra_rong(df, ten_sheet)
    df = df.fillna("")
    return [tuple(row) for row in df[['tentaikhoan', 'email', 'matkhau', 'ketquamongdoi']].values.tolist()]

# ĐỌC FILE JSON (ĐĂNG KÝ)
def doc_du_lieu_dang_ky_json(duong_dan):
    kiem_tra_file_ton_tai(duong_dan)
    with open(duong_dan, "r", encoding="utf-8") as f:
        data = json.load(f)
    ket_qua = []
    for item in data:
        tentaikhoan = item.get("tentaikhoan", "").strip()
        email = item.get("email", "").strip()
        matkhau = item.get("matkhau", "").strip()
        ketquamongdoi = item.get("ketquamongdoi", "").strip()
        ket_qua.append((tentaikhoan, email, matkhau, ketquamongdoi))
    return ket_qua

# ĐỌC FILE CSV (ĐĂNG KÝ)
def doc_du_lieu_dang_ky_csv(duong_dan):
    kiem_tra_file_ton_tai(duong_dan)
    df = pd.read_csv(duong_dan, encoding="utf-8")
    df.columns = df.columns.str.strip().str.lower()
    kiem_tra_cot_bat_buoc(df, ['tentaikhoan', 'email', 'matkhau', 'ketquamongdoi'], "CSV")
    kiem_tra_rong(df, "CSV")
    df = df.fillna("")
    return [tuple(row) for row in df[['tentaikhoan', 'email', 'matkhau', 'ketquamongdoi']].values.tolist()]

# ĐỌC FILE EXCEL (TÌM KIẾM)
def doc_du_lieu_tim_kiem_excel(duong_dan, ten_sheet="Timkiem"):
    kiem_tra_file_ton_tai(duong_dan)
    try:
        df = pd.read_excel(duong_dan, sheet_name=ten_sheet)
    except ValueError:
        raise ValueError(f" Không tìm thấy sheet '{ten_sheet}' trong file Excel.")
    df.columns = df.columns.str.strip().str.lower()
    kiem_tra_cot_bat_buoc(df, ['tukhoa', 'ketquatimkiem'], ten_sheet)
    kiem_tra_rong(df, ten_sheet)
    df = df.fillna("")
    data = []
    for row in df[['tukhoa', 'ketquatimkiem']].values.tolist():
        data.append(tuple(str(x) for x in row))
    return data

# ĐỌC FILE CSV (TÌM KIẾM)
def doc_du_lieu_tim_kiem_csv(duong_dan):
    kiem_tra_file_ton_tai(duong_dan)
    df = pd.read_csv(duong_dan, encoding="utf-8")
    df.columns = df.columns.str.strip().str.lower()
    kiem_tra_cot_bat_buoc(df, ['tukhoa', 'ketquatimkiem'], 'CSV')
    kiem_tra_rong(df, 'CSV')
    df = df.fillna("")
    data = []
    for row in df[['tukhoa', 'ketquatimkiem']].values.tolist():
        data.append(tuple(str(x) for x in row))
    return data

# ĐỌC FILE JSON (TÌM KIẾM)
def doc_du_lieu_tim_kiem_json(duong_dan):
    kiem_tra_file_ton_tai(duong_dan)
    with open(duong_dan, "r", encoding="utf-8") as f:
        data_json = json.load(f)
    if not data_json:
        raise ValueError(f" File JSON '{duong_dan}' trống hoặc không có dữ liệu.")
    data = []
    for item in data_json:
        tukhoa = item.get("tukhoa", "").strip()
        ketquatimkiem = item.get("ketquatimkiem", "").strip()
        data.append((tukhoa, ketquatimkiem))
    return data

def doc_du_lieu_thong_tin_excel(duong_dan, ten_sheet="Thongtin"):
    """
    Đọc dữ liệu cập nhật thông tin tài khoản từ file Excel.
    Cột bắt buộc: Ten, Ho, TenHienThi, Email, MatKhauHienTai, MatKhauMoi, XacNhanMK, KetQuaMongDoi
    """
    kiem_tra_file_ton_tai(duong_dan)
    try:
        df = pd.read_excel(duong_dan, sheet_name=ten_sheet)
    except ValueError:
        raise ValueError(f"Không tìm thấy sheet '{ten_sheet}' trong file Excel.")
    df.columns = df.columns.str.strip().str.lower()

    cot_bat_buoc = [
        'email', 'matkhau','ten', 'ho', 'tenhienthi', 'dcemail',
        'matkhauhientai', 'matkhaumoi', 'nhaplaimk', 'ketquamongdoi'
    ]
    kiem_tra_cot_bat_buoc(df, cot_bat_buoc, ten_sheet)
    kiem_tra_rong(df, ten_sheet)
    df = df.fillna("")
    return [tuple(row) for row in df[cot_bat_buoc].values.tolist()]

def doc_du_lieu_thong_tin_csv(duong_dan):
    """
    Đọc dữ liệu cập nhật thông tin tài khoản từ file CSV.
    Cột bắt buộc: Email, MatKhau,  Ten, Ho,TenHienThi, DcEmail, MatKhauHienTai, MatKhauMoi, NhapLaiMK, KetQuaMongDoi
    """
    kiem_tra_file_ton_tai(duong_dan)
    df = pd.read_csv(duong_dan, encoding="utf-8")
    df.columns = df.columns.str.strip().str.lower()

    cot_bat_buoc = [
        'email', 'matkhau',  'ten','ho', 'tenhienthi', 'dcemail',
        'matkhauhientai', 'matkhaumoi', 'nhaplaimk', 'ketquamongdoi'
    ]

    kiem_tra_cot_bat_buoc(df, cot_bat_buoc, 'CSV')
    kiem_tra_rong(df, 'CSV')

    df = df.fillna("")
    return [tuple(row) for row in df[cot_bat_buoc].values.tolist()]

def doc_du_lieu_thong_tin_json(duong_dan):
    """
    Đọc dữ liệu cập nhật thông tin tài khoản từ file JSON.
    Cột bắt buộc: Email, MatKhau,  Ten,Ho, TenHienThi, DcEmail, MatKhauHienTai, MatKhauMoi, NhapLaiMK, KetQuaMongDoi
    """
    kiem_tra_file_ton_tai(duong_dan)
    with open(duong_dan, "r", encoding="utf-8") as f:
        data_json = json.load(f)

    if not data_json:
        raise ValueError(f" File JSON '{duong_dan}' trống hoặc không có dữ liệu.")

    df = pd.DataFrame(data_json)
    df.columns = df.columns.str.strip().str.lower()

    cot_bat_buoc = [
        'email', 'matkhau',  'ten', 'ho','tenhienthi', 'dcemail',
        'matkhauhientai', 'matkhaumoi', 'nhaplaimk', 'ketquamongdoi'
    ]

    kiem_tra_cot_bat_buoc(df, cot_bat_buoc, 'JSON')
    kiem_tra_rong(df, 'JSON')

    df = df.fillna("")
    return [tuple(row) for row in df[cot_bat_buoc].values.tolist()]


##sửa ở dưới 
# ==================== ĐỌC FILE EXCEL (MUA HÀNG DDT) ==================== #
def doc_du_lieu_muahang_excel(duong_dan, ten_sheet="MuaHang"):
    """
    Đọc dữ liệu mua hàng từ file Excel.
    Cột bắt buộc: email, matkhau, tukhoatimkiem, tensp, ten, diachi, thanhpho, sdt, dcemail, ghichu, ketquamongdoi
    """
    kiem_tra_file_ton_tai(duong_dan)
    try:
        df = pd.read_excel(duong_dan, sheet_name=ten_sheet)
    except ValueError:
        raise ValueError(f" Không tìm thấy sheet '{ten_sheet}' trong file Excel.")

    df.columns = df.columns.str.strip().str.lower()

    cot_bat_buoc = [
        'email', 'matkhau', 'tukhoatimkiem', 'tensp', 'ten',
        'diachi', 'thanhpho', 'sdt', 'dcemail', 'ghichu', 'ketquamongdoi'
    ]

    kiem_tra_cot_bat_buoc(df, cot_bat_buoc, ten_sheet)
    kiem_tra_rong(df, ten_sheet)
    df = df.fillna("")

    return [tuple(row) for row in df[cot_bat_buoc].values.tolist()]

# ==================== ĐỌC FILE CSV (MUA HÀNG DDT) ==================== #
def doc_du_lieu_muahang_csv(duong_dan):
    kiem_tra_file_ton_tai(duong_dan)
    df = pd.read_csv(duong_dan, encoding="utf-8")
    df.columns = df.columns.str.strip().str.lower()

    cot_bat_buoc = [
        'email', 'matkhau', 'tukhoatimkiem', 'tensp', 'ten',
        'diachi', 'thanhpho', 'sdt', 'dcemail', 'ghichu', 'ketquamongdoi'
    ]

    kiem_tra_cot_bat_buoc(df, cot_bat_buoc, 'CSV')
    kiem_tra_rong(df, 'CSV')
    df = df.fillna("")

    return [tuple(row) for row in df[cot_bat_buoc].values.tolist()]

# ==================== ĐỌC FILE JSON (MUA HÀNG DDT) ==================== #
def doc_du_lieu_muahang_json(duong_dan):
    kiem_tra_file_ton_tai(duong_dan)
    with open(duong_dan, "r", encoding="utf-8") as f:
        data_json = json.load(f)

    if not data_json:
        raise ValueError(f" File JSON '{duong_dan}' trống hoặc không có dữ liệu.")

    df = pd.DataFrame(data_json)
    df.columns = df.columns.str.strip().str.lower()

    cot_bat_buoc = [
        'email', 'matkhau', 'tukhoatimkiem', 'tensp', 'ten',
        'diachi', 'thanhpho', 'sdt', 'dcemail', 'ghichu', 'ketquamongdoi'
    ]

    kiem_tra_cot_bat_buoc(df, cot_bat_buoc, 'JSON')
    kiem_tra_rong(df, 'JSON')
    df = df.fillna("")

    return [tuple(row) for row in df[cot_bat_buoc].values.tolist()]
