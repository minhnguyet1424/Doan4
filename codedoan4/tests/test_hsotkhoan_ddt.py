
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
