import pytest
from pages.timkiem_page import TrangTimKiem
from utils.data_utils import (
    doc_du_lieu_tim_kiem_excel,
    doc_du_lieu_tim_kiem_csv,
    doc_du_lieu_tim_kiem_json
)
from utils.report_helper import ExcelReport

REPORT_FILE = "reports/report.xlsx"
#  FIXTURE TẠO REPORT 
@pytest.fixture(scope="module")
def report():
    header = ["STT", "Thời gian", "Từ khóa", "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"]
    rep = ExcelReport(
        REPORT_FILE,
        sheet_name="TimKiem",
        tieu_de_base="Báo cáo Tìm kiếm",
        header=header
    )
    return rep
# PARAMETRIZE DATA 
def pytest_generate_tests(metafunc):
    if "tu_khoa" in metafunc.fixturenames:
        data_mode = metafunc.config.getoption("data_mode", default="excel")
        duong_dan_excel = "data/input_case.xlsx"

        if data_mode == "excel":
            test_cases = doc_du_lieu_tim_kiem_excel(duong_dan_excel, ten_sheet="Timkiem")
        elif data_mode == "csv":
            test_cases = doc_du_lieu_tim_kiem_csv("data/input_search_case.csv")
        elif data_mode == "json":
            test_cases = doc_du_lieu_tim_kiem_json("data/input_search_case.json")
        else:
            raise ValueError(f"Data mode '{data_mode}' không hợp lệ.")
        metafunc.parametrize("tu_khoa,ketquamongdoi", test_cases)
#  TEST CASE CHÍNH 
@pytest.mark.excel
def test_tim_kiem_excel(cau_hinh, tu_khoa, ketquamongdoi, report):
    driver = cau_hinh["driver"]
    trang = TrangTimKiem(driver)
    trang.mo_trang_tim_kiem()
    # Thực hiện tìm kiếm 
    if not tu_khoa.strip():
        trang.bam_tim_kiem()
        input_element = trang.wait.until(lambda d: d.find_element(*trang.TIM_KIEM))
        ketqua_thuc_te = input_element.get_attribute("validationMessage").strip()
    else:
        trang.nhap_tu_khoa(tu_khoa)
        trang.bam_tim_kiem()
        ketqua_thuc_te = trang.lay_san_pham_dau_tien()
    status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"
    # --- STT tự động tăng ---
    if not hasattr(test_tim_kiem_excel, "stt_counter"):
        test_tim_kiem_excel.stt_counter = 1
    stt = test_tim_kiem_excel.stt_counter
    test_tim_kiem_excel.stt_counter += 1

    # --- Ghi báo cáo ---
    report.add_row(stt, tu_khoa, ketquamongdoi, ketqua_thuc_te, status)
    report.save()

    # --- Screenshot khi Fail ---
    try:
        assert ketquamongdoi.lower() in ketqua_thuc_te.lower()
    except AssertionError:
        anh_path = trang.save_screenshot(name=f"timkiem_fail_{tu_khoa or 'empty'}")
        print(f"[!] Đã lưu ảnh lỗi: {anh_path}")
        raise
