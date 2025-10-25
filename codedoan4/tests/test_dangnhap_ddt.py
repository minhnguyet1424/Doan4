import pytest
from pages.dangnhap_page import TrangDangNhap
from base.config import URL_DANG_NHAP
from utils.data_utils import (
    doc_du_lieu_dang_nhap_excel,
    doc_du_lieu_dang_nhap_csv,
    doc_du_lieu_dang_nhap_json
)
from utils.report_helper import ExcelReport
REPORT_FILE = "reports/report.xlsx"
# ========================== FIXTURE TẠO REPORT ========================== #
@pytest.fixture(scope="module")
def report():
    login_header = [
        "STT", "Thời gian", "Email/Tài khoản", "Mật khẩu",
        "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"]
    rep = ExcelReport(
        REPORT_FILE,
        sheet_name="DangNhap",
        tieu_de_base="Báo cáo Đăng nhập",
        header=login_header)
    return rep
# ========================== PARAMETRIZE DATA ========================== #
def pytest_generate_tests(metafunc):
    if "email" in metafunc.fixturenames:
        data_mode = metafunc.config.getoption("data_mode")
        duong_dan_excel = "data/input_case.xlsx"
        if data_mode == "excel":
            test_cases = doc_du_lieu_dang_nhap_excel(duong_dan_excel, ten_sheet="Dangnhap")
        elif data_mode == "csv":
            test_cases = doc_du_lieu_dang_nhap_csv("data/input_login_case.csv")
        elif data_mode == "json":
            test_cases = doc_du_lieu_dang_nhap_json("data/input_login_case.json")
        else:
            raise ValueError(f"Data mode '{data_mode}' không hợp lệ.")
        metafunc.parametrize("email,matkhau,ketquamongdoi", test_cases)
# ========================== TEST CASE CHÍNH ========================== #
def test_dang_nhap_excel(cau_hinh, email, matkhau, ketquamongdoi, report):
    driver = cau_hinh["driver"]
    trang = TrangDangNhap(driver, URL_DANG_NHAP)
    trang.mo_trang_dang_nhap()
    trang.nhap_email(email)
    trang.nhap_mat_khau(matkhau)
    trang.bam_dang_nhap()
    ketqua_thuc_te = trang.lay_thong_bao()
    status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"
    # --- STT tự động tăng ---
    if not hasattr(test_dang_nhap_excel, "stt_counter"):
        test_dang_nhap_excel.stt_counter = 1
    stt = test_dang_nhap_excel.stt_counter
    test_dang_nhap_excel.stt_counter += 1
    # --- Ghi dữ liệu vào Excel report ---
    report.add_row(
        stt,          
        email,        
        matkhau,     
        ketquamongdoi, 
        ketqua_thuc_te, 
        status        
    )
    report.save()
    # --- Xử lý khi test FAIL ---
    try:
        assert ketquamongdoi.lower() in ketqua_thuc_te.lower(), (
            f"Thông báo thực tế: {ketqua_thuc_te} != Kết quả mong đợi: {ketquamongdoi}"
        )
    except AssertionError as e:
        # Chụp screenshot khi lỗi
        anh_path = trang.save_screenshot(name=f"dangnhap_fail_{email or 'empty'}")
        print(f"[!] Đã lưu ảnh lỗi: {anh_path}")
        raise e  # Vẫn ném lỗi để pytest đánh dấu Fail
    # --- Dọn cookie sau mỗi test ---
    driver.delete_all_cookies()
