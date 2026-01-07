# import pytest
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

# from pages.dangnhap_page import TrangDangNhap
# from pages.hsotkhoan import TrangThongTinTaiKhoan
# from base.config import URL_DANG_NHAP, URL_EDIT_ACCOUNT
# from utils.data_utils import (
#     doc_du_lieu_thong_tin_excel,
#     doc_du_lieu_thong_tin_csv,
#     doc_du_lieu_thong_tin_json
# )
# from utils.report_helper import ExcelReport

# REPORT_FILE = "reports/report.xlsx"

# # Fixture tạo file báo cáo
# @pytest.fixture(scope="module")
# def report():
#     header = [
#         "STT", "Thời gian", "Email", "Mật khẩu", "Tên", "Họ", "Tên hiển thị", "Địa chỉ Email",
#         "Mật khẩu hiện tại", "Mật khẩu mới", "Xác nhận MK",
#         "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
#     ]
#     rep = ExcelReport(
#         REPORT_FILE,
#         sheet_name="ThongTinCaNhan",
#         tieu_de_base="Báo cáo Thông tin tài khoản",
#         header=header
#     )
#     return rep

# #  Sinh dữ liệu test (Excel / CSV / JSON)
# def pytest_generate_tests(metafunc):
#     if "ho" in metafunc.fixturenames:
#         data_mode = metafunc.config.getoption("data_mode")
#         duong_dan_excel = "data/input_case.xlsx"

#         if data_mode == "excel":
#             test_cases = doc_du_lieu_thong_tin_excel(duong_dan_excel, ten_sheet="Hsotkhoan")
#         elif data_mode == "csv":
#             test_cases = doc_du_lieu_thong_tin_csv("data\input_account_case.csv")
#         elif data_mode == "json":
#             test_cases = doc_du_lieu_thong_tin_json("data\input_accont_case.json")
#         else:
#             raise ValueError(f"Data mode '{data_mode}' không hợp lệ. Hãy dùng: excel, csv hoặc json.")

#         metafunc.parametrize(
#             "email,matkhau,ten,ho,tenhienthi,dcemail,matkhauhientai,matkhaumoi,nhaplaimk,ketquamongdoi",
#             test_cases
#         )
# def test_cap_nhat_thong_tin(
#     cau_hinh,
#     email, matkhau, ten, ho, tenhienthi, dcemail,
#     matkhauhientai, matkhaumoi, nhaplaimk, ketquamongdoi,
#     report,
#     logger  # <- thêm logger
# ):
#     driver = cau_hinh["driver"]
#     trang_tt = None  
#     ketqua_thuc_te = "Không lấy được kết quả"
#     status = "Fail"

#     logger.info(f"Bắt đầu test cập nhật thông tin cho Email: {email}")

#     try:
#         # --- Đăng nhập ---
#         trang_dang_nhap = TrangDangNhap(driver, URL_DANG_NHAP)
#         trang_dang_nhap.mo_trang_dang_nhap()
#         logger.info(f"Mở trang đăng nhập: {URL_DANG_NHAP}")
#         trang_dang_nhap.nhap_email(email)
#         trang_dang_nhap.nhap_mat_khau(matkhau)
#         trang_dang_nhap.bam_dang_nhap()
#         logger.info("Đã nhập thông tin đăng nhập và nhấn đăng nhập")

#         WebDriverWait(driver, 10).until(EC.url_contains("/my-account"))

#         # --- Cập nhật thông tin ---
#         trang_tt = TrangThongTinTaiKhoan(driver, URL_EDIT_ACCOUNT)
#         trang_tt.mo_trang_thong_tin()
#         logger.info(f"Mở trang thông tin tài khoản: {URL_EDIT_ACCOUNT}")

#         trang_tt.cap_nhat_thong_tin(ten, ho, tenhienthi, dcemail, matkhauhientai, matkhaumoi, nhaplaimk)
#         logger.info("Đã nhập dữ liệu cập nhật thông tin")

#         time.sleep(3)
#         ketqua_thuc_te = trang_tt.lay_thong_bao()
#         logger.info(f"Kết quả thực tế: {ketqua_thuc_te}")

#         # --- Kiểm tra kết quả ---
#         if ketquamongdoi.lower() in ketqua_thuc_te.lower():
#             status = "Pass"
#             logger.info(f"Kết quả mong đợi: {ketquamongdoi} | Trạng thái: {status}")
#         else:
#             anh_path = trang_tt.save_screenshot(name=f"thongtin_fail_{email or 'empty'}")
#             logger.error(f"Test FAIL - Đã lưu ảnh lỗi: {anh_path}")
#             status = "Fail"
#             pytest.fail(f"Kết quả thực tế: {ketqua_thuc_te} != Kết quả mong đợi: {ketquamongdoi}")

#     except Exception as e:
#         ketqua_thuc_te = str(e)
#         status = "Fail"
#         logger.error(f"Lỗi trong test với {email}: {e}")
#         raise e

#     finally:
#         # --- Ghi báo cáo ---
#         if not hasattr(test_cap_nhat_thong_tin, "stt_counter"):
#             test_cap_nhat_thong_tin.stt_counter = 1
#         stt = test_cap_nhat_thong_tin.stt_counter
#         test_cap_nhat_thong_tin.stt_counter += 1

#         report.add_row(
#             stt, email, matkhau, ten, ho, tenhienthi, dcemail,
#             matkhauhientai, matkhaumoi, nhaplaimk,
#             ketquamongdoi, ketqua_thuc_te, status
#         )
#         report.save()
#         logger.info(f"===== Kết thúc test với Email: {email} | Trạng thái: {status} =====\n")
import pytest
import time
from pages.dangnhap_page import TrangDangNhap
from pages.hsotkhoan import TrangThongTinTaiKhoan
from base.config import URL_DANG_NHAP, URL_EDIT_ACCOUNT
from utils.report_helper import ExcelReport

REPORT_FILE = "reports/report.xlsx"

# ================== REPORT ==================
@pytest.fixture(scope="module")
def report_thongtin():
    header = [
        "STT", "Thời gian", "Email", "Mật khẩu", "Tên", "Họ", "Tên hiển thị", "Địa chỉ Email",
        "Mật khẩu hiện tại", "Mật khẩu mới", "Nhập lại MK",
        "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
    ]
    return ExcelReport(
        REPORT_FILE,
        sheet_name="ThongTinTaiKhoan",
        tieu_de_base="Báo cáo Thông tin tài khoản",
        header=header
    )

# ================== TEST ==================
def test_cap_nhat_thong_tin_ddt(
    cau_hinh,
    email, matkhau, ten, ho, tenhienthi, dcemail,
    matkhauhientai, matkhaumoi, nhaplaimk, ketquamongdoi,
    report_thongtin,
    logger
):
    driver = cau_hinh["driver"]
    ketqua_thuc_te = "Không lấy được kết quả"
    status = "Fail"

    try:
        # --- STT tự động ---
        if not hasattr(test_cap_nhat_thong_tin_ddt, "stt"):
            test_cap_nhat_thong_tin_ddt.stt = 1
        stt = test_cap_nhat_thong_tin_ddt.stt

        logger.info(f"\n=== TEST CASE {stt} ===")
        logger.info(f"Bắt đầu test cập nhật thông tin | Email={email}")

        # --- Đăng nhập ---
        trang_dn = TrangDangNhap(driver, URL_DANG_NHAP)
        trang_dn.mo_trang_dang_nhap()
        trang_dn.nhap_email(email)
        trang_dn.nhap_mat_khau(matkhau)
        trang_dn.bam_dang_nhap()
        logger.info("Đã đăng nhập thành công")
        time.sleep(2)  # chờ load trang

        # --- Cập nhật thông tin ---
        trang_tt = TrangThongTinTaiKhoan(driver, URL_EDIT_ACCOUNT)
        trang_tt.mo_trang_thong_tin()
        trang_tt.cap_nhat_thong_tin(
            ten, ho, tenhienthi, dcemail, matkhauhientai, matkhaumoi, nhaplaimk
        )
        time.sleep(2)
        ketqua_thuc_te = trang_tt.lay_thong_bao()
        logger.info(f"Kết quả thực tế: {ketqua_thuc_te}")

        # --- So sánh và ghi báo cáo ---
        status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"
        report_thongtin.add_row(
            stt, email, matkhau, ten, ho, tenhienthi, dcemail,
            matkhauhientai, matkhaumoi, nhaplaimk,
            ketquamongdoi, ketqua_thuc_te, status
        )
        report_thongtin.save()
        logger.info(f"Kết quả mong đợi: {ketquamongdoi} | Trạng thái: {status}")

        # --- Assert ---
        assert ketquamongdoi.lower() in ketqua_thuc_te.lower()

      
    finally:
        test_cap_nhat_thong_tin_ddt.stt += 1
        driver.delete_all_cookies()
        logger.info("Đã xóa cookie sau test\n")
