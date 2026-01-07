
import pytest
from pages.timkiem_page import TrangTimKiem
from utils.report_helper import ExcelReport

REPORT_FILE = "reports/report.xlsx"

# ================== REPORT ==================
@pytest.fixture(scope="module")
def report():
    header = ["STT", "Thời gian", "Từ khóa", "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"]
    return ExcelReport(
        REPORT_FILE,
        sheet_name="TimKiem",
        tieu_de_base="Báo cáo Tìm kiếm",
        header=header
    )

# ================== TEST ==================
def test_tim_kiem_ddt(cau_hinh, tukhoa, ketquamongdoi, report, logger):
    driver = cau_hinh["driver"]
    trang = TrangTimKiem(driver)

    try:
        # --- STT tự động ---
        if not hasattr(test_tim_kiem_ddt, "stt"):
            test_tim_kiem_ddt.stt = 1
        stt = test_tim_kiem_ddt.stt

        logger.info(f"\n=== TEST CASE {stt} ===")
        logger.info(f"Bắt đầu test tìm kiếm với từ khóa: '{tukhoa}'")

        # --- Mở trang ---
        trang.mo_trang_tim_kiem()

        # --- Thực hiện tìm kiếm ---
        if not tukhoa.strip():
            trang.bam_tim_kiem()
            input_element = trang.wait.until(lambda d: d.find_element(*trang.TIM_KIEM))
            ketqua_thuc_te = input_element.get_attribute("validationMessage").strip()
            logger.info(f"Từ khóa trống, thông báo HTML5: {ketqua_thuc_te}")
        else:
            trang.nhap_tu_khoa(tukhoa)
            trang.bam_tim_kiem()
            ketqua_thuc_te = trang.lay_san_pham_dau_tien()
            logger.info(f"Tìm kiếm từ khóa '{tukhoa}', kết quả đầu tiên: {ketqua_thuc_te}")

        # --- So sánh kết quả ---
        status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"
        logger.info(f"Kết quả mong đợi: {ketquamongdoi} | Trạng thái: {status}")

        # --- Ghi vào báo cáo ---
        report.add_row(stt, tukhoa, ketquamongdoi, ketqua_thuc_te, status)
        report.save()

        # --- Assert ---
        assert ketquamongdoi.lower() in ketqua_thuc_te.lower()

        # --- Tăng STT ---
        test_tim_kiem_ddt.stt += 1

    finally:
        test_tim_kiem_ddt.stt += 1
        driver.delete_all_cookies()
        logger.info("Đã xóa cookie sau test\n")

