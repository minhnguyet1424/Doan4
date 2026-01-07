
import pytest
from pages.dangky_page import TrangDangKy
from utils.report_helper import ExcelReport
from base.config import URL_DANG_KY

REPORT_FILE = "reports/report.xlsx"

# ================== REPORT ==================
@pytest.fixture(scope="module")
def report():
    header = [
        "STT", "Thời gian", "Tên tài khoản", "Email",
        "Mật khẩu", "Kết quả mong đợi",
        "Kết quả thực tế", "Trạng thái"
    ]
    return ExcelReport(
        REPORT_FILE,
        sheet_name="DangKy",
        tieu_de_base="Báo cáo Đăng ký",
        header=header
    )

# ================== TEST ==================
def test_dang_ky_ddt(
    cau_hinh, tentaikhoan, email, matkhau, ketquamongdoi, report, logger
):
    driver = cau_hinh["driver"]
    trang = TrangDangKy(driver, URL_DANG_KY)

    # --- Đảm bảo cookie luôn được xóa dù test pass/fail ---
    try:
        # --- STT tự động và phân cách log ---
        if not hasattr(test_dang_ky_ddt, "stt"):
            test_dang_ky_ddt.stt = 1
        stt = test_dang_ky_ddt.stt

        logger.info(f"\n=== TEST CASE {stt} ===")
        logger.info(f"Bắt đầu test đăng ký | TK={tentaikhoan}, Email={email}")

        # --- Mở trang ---
        trang.mo_trang_dang_ky()

        # --- Nhập dữ liệu ---
        if tentaikhoan:
            trang.nhap_ten_tai_khoan(str(tentaikhoan))
        if email:
            trang.nhap_email(str(email))
        if matkhau:
            trang.nhap_mat_khau(str(matkhau))
        logger.info("Đã nhập dữ liệu đăng ký")

        # --- Submit ---
        try:
            trang.bam_dang_ky()
            logger.info("Đã nhấn nút Đăng ký")
        except Exception:
            logger.warning("Không thể nhấn nút Đăng ký")

        # --- Kết quả ---
        ketqua_thuc_te = trang.lay_thong_bao()
        logger.info(f"Kết quả thực tế: {ketqua_thuc_te}")

        status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"
        logger.info(f"Kết quả mong đợi: {ketquamongdoi} | Trạng thái: {status}")

        # --- Ghi vào báo cáo Excel ---
        report.add_row(
            stt,
            tentaikhoan, email, matkhau,
            ketquamongdoi, ketqua_thuc_te, status
        )
        report.save()

        # --- Assert ---
        assert ketquamongdoi.lower() in ketqua_thuc_te.lower()

        

    finally:
        # --- Cleanup: xóa cookie và log ---
        test_dang_ky_ddt.stt += 1
        driver.delete_all_cookies()
        logger.info("Đã xóa cookie sau test\n")
