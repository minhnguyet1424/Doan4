# import pytest
# from pages.dangnhap_page import TrangDangNhap
# from base.config import URL_DANG_NHAP
# from utils.data_utils import (
#     doc_du_lieu_dang_nhap_excel,
#     doc_du_lieu_dang_nhap_csv,
#     doc_du_lieu_dang_nhap_json
# )
# from utils.report_helper import ExcelReport

# REPORT_FILE = "reports/report.xlsx"

# # === FIXTURE TẠO REPORT ===
# @pytest.fixture(scope="module")
# def report():
#     login_header = [
#         "STT", "Thời gian", "Email/Tài khoản", "Mật khẩu",
#         "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
#     ]
#     rep = ExcelReport(
#         REPORT_FILE,
#         sheet_name="DangNhap",
#         tieu_de_base="Báo cáo Đăng nhập",
#         header=login_header
#     )
#     return rep


# # === PARAMETRIZE DATA ===
# def pytest_generate_tests(metafunc):
#     if "email" in metafunc.fixturenames:
#         data_mode = metafunc.config.getoption("data_mode")
#         duong_dan_excel = "data/input_case.xlsx"

#         if data_mode == "excel":
#             test_cases = doc_du_lieu_dang_nhap_excel(duong_dan_excel, ten_sheet="Dangnhap")
#         elif data_mode == "csv":
#             test_cases = doc_du_lieu_dang_nhap_csv("data/input_login_case.csv")
#         elif data_mode == "json":
#             test_cases = doc_du_lieu_dang_nhap_json("data/input_login_case.json")
#         else:
#             raise ValueError(f"Data mode '{data_mode}' không hợp lệ.")

#         metafunc.parametrize("email,matkhau,ketquamongdoi", test_cases)


# # === TEST CASE CHÍNH ===
# def test_dang_nhap_excel(cau_hinh, email, matkhau, ketquamongdoi, report, logger):
#     driver = cau_hinh["driver"]
#     trang = TrangDangNhap(driver, URL_DANG_NHAP)

#     logger.info(f"Bắt đầu test đăng nhập với Email: {email} | Mật khẩu: {matkhau}")

#     # Thực hiện test
#     trang.mo_trang_dang_nhap()
#     logger.info(f"Mở trang đăng nhập: {URL_DANG_NHAP}")

#     trang.nhap_email(email)
#     trang.nhap_mat_khau(matkhau)
#     trang.bam_dang_nhap()
#     logger.info("Đã nhập thông tin và nhấn nút đăng nhập")

#     # Lấy kết quả thực tế
#     ketqua_thuc_te = trang.lay_thong_bao()
#     logger.info(f"Kết quả thực tế: {ketqua_thuc_te}")

#     # So sánh kết quả
#     status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"
#     logger.info(f"Kết quả mong đợi: {ketquamongdoi} | Trạng thái: {status}")

#     # --- STT tự động ---
#     if not hasattr(test_dang_nhap_excel, "stt_counter"):
#         test_dang_nhap_excel.stt_counter = 1
#     stt = test_dang_nhap_excel.stt_counter
#     test_dang_nhap_excel.stt_counter += 1

#     # --- Ghi vào report ---
#     report.add_row(
#         stt,
#         email,
#         matkhau,
#         ketquamongdoi,
#         ketqua_thuc_te,
#         status
#     )
#     report.save()

#     # --- Nếu lỗi thì chụp ảnh ---
#     try:
#         assert ketquamongdoi.lower() in ketqua_thuc_te.lower(), (
#             f"Thông báo thực tế: {ketqua_thuc_te} != Kết quả mong đợi: {ketquamongdoi}"
#         )
#     except AssertionError as e:
#         anh_path = trang.save_screenshot(name=f"dangnhap_fail_{email or 'empty'}")
#         logger.error(f" Test FAIL - Đã lưu ảnh lỗi: {anh_path}")
#         raise e

#     # --- Dọn cookie ---
#     driver.delete_all_cookies()
#     logger.info("Đã xóa cookie sau test.\n")
import pytest
from pages.dangnhap_page import TrangDangNhap
from utils.report_helper import ExcelReport
from base.config import URL_DANG_NHAP

REPORT_FILE = "reports/report.xlsx"

# ================== REPORT ==================
@pytest.fixture(scope="module")
def report():
    header = [
        "STT", "Thời gian", "Email/Tài khoản", "Mật khẩu",
        "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
    ]
    return ExcelReport(
        REPORT_FILE,
        sheet_name="DangNhap",
        tieu_de_base="Báo cáo Đăng nhập",
        header=header
    )

# ================== TEST ==================
def test_dang_nhap_ddt(cau_hinh, email, matkhau, ketquamongdoi, report, logger):
    driver = cau_hinh["driver"]
    trang = TrangDangNhap(driver, URL_DANG_NHAP)

    # --- Đảm bảo cookie luôn được xóa dù test pass/fail ---
    try:
        # --- STT tự động và phân cách log ---
        if not hasattr(test_dang_nhap_ddt, "stt"):
            test_dang_nhap_ddt.stt = 1
        stt = test_dang_nhap_ddt.stt

        logger.info(f"\n=== TEST CASE {stt} ===")
        logger.info(f"Bắt đầu test đăng nhập | Email={email}, Mật khẩu={matkhau}")

        # --- Mở trang ---
        trang.mo_trang_dang_nhap()

        # --- Nhập dữ liệu ---
        if email:
            trang.nhap_email(str(email))
        if matkhau:
            trang.nhap_mat_khau(str(matkhau))
        logger.info("Đã nhập dữ liệu đăng nhập")

        # --- Submit ---
        try:
            trang.bam_dang_nhap()
            logger.info("Đã nhấn nút Đăng nhập")
        except Exception:
            logger.warning("Không thể nhấn nút Đăng nhập")

        # --- Kết quả ---
        ketqua_thuc_te = trang.lay_thong_bao()
        logger.info(f"Kết quả thực tế: {ketqua_thuc_te}")

        status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"
        logger.info(f"Kết quả mong đợi: {ketquamongdoi} | Trạng thái: {status}")

        # --- Ghi vào báo cáo Excel ---
        report.add_row(
            stt,
            email, matkhau,
            ketquamongdoi, ketqua_thuc_te, status
        )
        report.save()

        # --- Assert ---
        assert ketquamongdoi.lower() in ketqua_thuc_te.lower()


    finally:
        # --- Cleanup: xóa cookie và log ---
        test_dang_nhap_ddt.stt += 1
        driver.delete_all_cookies()
        logger.info("Đã xóa cookie sau test\n")
