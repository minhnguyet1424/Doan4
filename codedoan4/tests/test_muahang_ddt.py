import pytest
import time
from pages.timkiem_page import TrangTimKiem
from pages.muahang_page import TrangMuaNgay
from utils.data_utils import doc_du_lieu_muahang_excel
from utils.report_helper import ExcelReport

FILE_DU_LIEU = "data/input_case.xlsx"
REPORT_FILE = "reports/report.xlsx"


@pytest.fixture(scope="module")
def report():
    header = [
        "STT", "Từ khóa", "Tên SP", "Tên KH", "Địa chỉ", "Thành phố",
        "SĐT", "Email", "Ghi chú", "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
    ]
    return ExcelReport(REPORT_FILE, "MuaNgay", "Báo cáo Mua Ngay", header)

def pytest_generate_tests(metafunc):
    if "tukhoa" in metafunc.fixturenames:
        test_cases = doc_du_lieu_muahang_excel(FILE_DU_LIEU, ten_sheet="Muahang")
        metafunc.parametrize(
            "tukhoa, tensp, ten, diachi, thanhpho, sdt, email, ghichu, ketquamongdoi",
            test_cases
        )

def test_mua_ngay(cau_hinh, tukhoa, tensp, ten, diachi, thanhpho, sdt, email, ghichu, ketquamongdoi, report):
    driver = cau_hinh["driver"]

    #  Tìm kiếm sản phẩm 
    trang_tim_kiem = TrangTimKiem(driver)
    trang_tim_kiem.mo_trang_tim_kiem()
    trang_tim_kiem.nhap_tu_khoa(tukhoa)
    trang_tim_kiem.bam_tim_kiem()
    time.sleep(3)

    #  Chọn đúng sản phẩm theo tên 
    if not trang_tim_kiem.chon_san_pham_theo_ten(tensp):
        ketqua_thuc_te = "Không tìm thấy sản phẩm phù hợp."
        status = "Fail"
    else:
        # Điền form checkout
        gio_hang = TrangMuaNgay(driver)
        gio_hang.nhap_thong_tin_checkout(ten, email, sdt, diachi, thanhpho, ghi_chu=ghichu)
        gio_hang.dat_hang()
        time.sleep(3)
        ketqua_thuc_te = gio_hang.lay_thong_bao_dat_hang()
        status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"

    #  Báo cáo kết quả 
    if not hasattr(test_mua_ngay, "stt_counter"):
        test_mua_ngay.stt_counter = 1
    stt = test_mua_ngay.stt_counter
    test_mua_ngay.stt_counter += 1

    report.add_row(stt, tukhoa, tensp, ten, diachi, thanhpho, sdt, email, ghichu, ketquamongdoi, ketqua_thuc_te, status)
    report.save()

    # Kiểm tra 
    assert ketquamongdoi.lower() in ketqua_thuc_te.lower(), f"{ketqua_thuc_te} != {ketquamongdoi}"
