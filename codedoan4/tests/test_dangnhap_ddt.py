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

# === FIXTURE TẠO REPORT ===
@pytest.fixture(scope="module")
def report():
    login_header = [
        "STT", "Thời gian", "Email/Tài khoản", "Mật khẩu",
        "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
    ]
    rep = ExcelReport(
        REPORT_FILE,
        sheet_name="DangNhap",
        tieu_de_base="Báo cáo Đăng nhập",
        header=login_header
    )
    return rep


# === PARAMETRIZE DATA ===
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


# === TEST CASE CHÍNH ===
def test_dang_nhap_excel(cau_hinh, email, matkhau, ketquamongdoi, report, logger):
    driver = cau_hinh["driver"]
    trang = TrangDangNhap(driver, URL_DANG_NHAP)

    logger.info(f"Bắt đầu test đăng nhập với Email: {email} | Mật khẩu: {matkhau}")

    # Thực hiện test
    trang.mo_trang_dang_nhap()
    logger.info(f"Mở trang đăng nhập: {URL_DANG_NHAP}")

    trang.nhap_email(email)
    trang.nhap_mat_khau(matkhau)
    trang.bam_dang_nhap()
    logger.info("Đã nhập thông tin và nhấn nút đăng nhập")

    # Lấy kết quả thực tế
    ketqua_thuc_te = trang.lay_thong_bao()
    logger.info(f"Kết quả thực tế: {ketqua_thuc_te}")

    # So sánh kết quả
    status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"
    logger.info(f"Kết quả mong đợi: {ketquamongdoi} | Trạng thái: {status}")

    # --- STT tự động ---
    if not hasattr(test_dang_nhap_excel, "stt_counter"):
        test_dang_nhap_excel.stt_counter = 1
    stt = test_dang_nhap_excel.stt_counter
    test_dang_nhap_excel.stt_counter += 1

    # --- Ghi vào report ---
    report.add_row(
        stt,
        email,
        matkhau,
        ketquamongdoi,
        ketqua_thuc_te,
        status
    )
    report.save()

    # --- Nếu lỗi thì chụp ảnh ---
    try:
        assert ketquamongdoi.lower() in ketqua_thuc_te.lower(), (
            f"Thông báo thực tế: {ketqua_thuc_te} != Kết quả mong đợi: {ketquamongdoi}"
        )
    except AssertionError as e:
        anh_path = trang.save_screenshot(name=f"dangnhap_fail_{email or 'empty'}")
        logger.error(f" Test FAIL - Đã lưu ảnh lỗi: {anh_path}")
        raise e

    # --- Dọn cookie ---
    driver.delete_all_cookies()
    logger.info("Đã xóa cookie sau test.\n")
