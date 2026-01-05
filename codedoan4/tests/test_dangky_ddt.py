
import pytest
from pages.dangky_page import TrangDangKy
from utils.data_utils import (
    doc_du_lieu_dang_ky_excel,
    doc_du_lieu_dang_ky_csv,
    doc_du_lieu_dang_ky_json
)
from utils.report_helper import ExcelReport
from base.config import URL_DANG_KY

REPORT_FILE = "reports/report.xlsx"

# --- FIXTURE TẠO REPORT ---
@pytest.fixture(scope="module")
def report():
    header = [
        "STT", "Thời gian", "Tên tài khoản", "Email", "Mật khẩu",
        "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
    ]
    rep = ExcelReport(
        REPORT_FILE,
        sheet_name="DangKy",
        tieu_de_base="Báo cáo Đăng ký",
        header=header
    )
    return rep


# --- PARAMETRIZE DATA ---
def pytest_generate_tests(metafunc):
    if "tentaikhoan" in metafunc.fixturenames:
        data_mode = metafunc.config.getoption("data_mode")
        duong_dan_excel = "data/input_case.xlsx"

        if data_mode == "excel":
            test_cases = doc_du_lieu_dang_ky_excel(duong_dan_excel, ten_sheet="Dangky")
        elif data_mode == "csv":
            test_cases = doc_du_lieu_dang_ky_csv("data/input_regestered_case.csv")
        elif data_mode == "json":
            test_cases = doc_du_lieu_dang_ky_json("data/input_regestered_case.json")
        else:
            raise ValueError(f"Data mode '{data_mode}' không hợp lệ.")

        metafunc.parametrize("tentaikhoan,email,matkhau,ketquamongdoi", test_cases)

def test_dang_ky_excel(cau_hinh, tentaikhoan, email, matkhau, ketquamongdoi, report, logger):
    driver = cau_hinh["driver"]
    trang = TrangDangKy(driver, URL_DANG_KY)
    trang.mo_trang_dang_ky()
    logger.info(f"Bắt đầu test đăng ký với Tài khoản: {tentaikhoan}, Email: {email}")

    # --- Nhập dữ liệu ---
    if tentaikhoan:
        trang.nhap_ten_tai_khoan(str(tentaikhoan))
    if email:
        trang.nhap_email(str(email))
    if matkhau:
        trang.nhap_mat_khau(str(matkhau))
    logger.info("Đã nhập dữ liệu vào form đăng ký")

    # --- Bấm nút đăng ký ---
    try:
        trang.bam_dang_ky()
        logger.info("Đã nhấn nút Đăng ký")
    except Exception:
        logger.warning("Nút Đăng ký không khả dụng (thường do mật khẩu yếu)")

    # --- Lấy kết quả ---
    ketqua_thuc_te = trang.lay_thong_bao()
    logger.info(f"Kết quả thực tế: {ketqua_thuc_te}")

    # --- So sánh kết quả ---
    status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"
    logger.info(f"Kết quả mong đợi: {ketquamongdoi} | Trạng thái: {status}")

    # --- STT tự tăng ---
    if not hasattr(test_dang_ky_excel, "stt_counter"):
        test_dang_ky_excel.stt_counter = 1
    stt = test_dang_ky_excel.stt_counter
    test_dang_ky_excel.stt_counter += 1

    # --- Ghi vào Excel ---
    report.add_row(stt, tentaikhoan, email, matkhau, ketquamongdoi, ketqua_thuc_te, status)
    report.save()

    # --- Nếu test FAIL thì chụp ảnh ---
    try:
        assert ketquamongdoi.lower() in ketqua_thuc_te.lower(), (
            f"Thông báo thực tế: {ketqua_thuc_te} != Kết quả mong đợi: {ketquamongdoi}"
        )
    except AssertionError as e:
        anh_path = trang.save_screenshot(name=f"dangky_fail_{tentaikhoan or 'empty'}")
        logger.error(f" Test FAIL - Đã lưu ảnh lỗi: {anh_path}")
        raise e

    # --- Dọn cookie ---
    driver.delete_all_cookies()
    logger.info("Đã xóa cookie sau test.\n")
