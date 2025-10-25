import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.dangnhap_page import TrangDangNhap
from pages.hsotkhoan import TrangThongTinTaiKhoan
from base.config import URL_DANG_NHAP, URL_EDIT_ACCOUNT
from utils.data_utils import (
    doc_du_lieu_thong_tin_excel,
    doc_du_lieu_thong_tin_csv,
    doc_du_lieu_thong_tin_json
)
from utils.report_helper import ExcelReport

REPORT_FILE = "reports/report.xlsx"

# Fixture tạo file báo cáo
@pytest.fixture(scope="module")
def report():
    header = [
        "STT", "Thời gian", "Email", "Mật khẩu", "Tên", "Họ", "Tên hiển thị", "Địa chỉ Email",
        "Mật khẩu hiện tại", "Mật khẩu mới", "Xác nhận MK",
        "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
    ]
    rep = ExcelReport(
        REPORT_FILE,
        sheet_name="ThongTinCaNhan",
        tieu_de_base="Báo cáo Thông tin tài khoản",
        header=header
    )
    return rep

#  Sinh dữ liệu test (Excel / CSV / JSON)
def pytest_generate_tests(metafunc):
    if "ho" in metafunc.fixturenames:
        data_mode = metafunc.config.getoption("data_mode")
        duong_dan_excel = "data/input_case.xlsx"

        if data_mode == "excel":
            test_cases = doc_du_lieu_thong_tin_excel(duong_dan_excel, ten_sheet="Hsotkhoan")
        elif data_mode == "csv":
            test_cases = doc_du_lieu_thong_tin_csv("data\input_account_case.csv")
        elif data_mode == "json":
            test_cases = doc_du_lieu_thong_tin_json("data\input_accont_case.json")
        else:
            raise ValueError(f"Data mode '{data_mode}' không hợp lệ. Hãy dùng: excel, csv hoặc json.")

        metafunc.parametrize(
            "email,matkhau,ten,ho,tenhienthi,dcemail,matkhauhientai,matkhaumoi,nhaplaimk,ketquamongdoi",
            test_cases
        )

def test_cap_nhat_thong_tin(
    cau_hinh,
    email, matkhau, ten, ho, tenhienthi, dcemail,
    matkhauhientai, matkhaumoi, nhaplaimk, ketquamongdoi,
    report
):
    driver = cau_hinh["driver"]
    trang_tt = None  
    ketqua_thuc_te = "Không lấy được kết quả"   # Gán mặc định
    status = "Fail"                              #  Gán mặc định (nếu lỗi sớm)
    
    try:
        # --- Đăng nhập ---
        trang_dang_nhap = TrangDangNhap(driver, URL_DANG_NHAP)
        trang_dang_nhap.mo_trang_dang_nhap()
        trang_dang_nhap.nhap_email(email)
        trang_dang_nhap.nhap_mat_khau(matkhau)
        trang_dang_nhap.bam_dang_nhap()

        WebDriverWait(driver, 10).until(EC.url_contains("/my-account"))

        # --- Cập nhật thông tin ---
        trang_tt = TrangThongTinTaiKhoan(driver, URL_EDIT_ACCOUNT)
        trang_tt.mo_trang_thong_tin()
        trang_tt.cap_nhat_thong_tin(ten, ho, tenhienthi, dcemail, matkhauhientai, matkhaumoi, nhaplaimk)

        time.sleep(3)
        ketqua_thuc_te = trang_tt.lay_thong_bao()

        # --- Kiểm tra kết quả ---
        if ketquamongdoi.lower() in ketqua_thuc_te.lower():
            status = "Pass"
        else:
            anh_path = trang_tt.save_screenshot(name=f"thongtin_fail_{email or 'empty'}")
            print(f"[!] Đã lưu ảnh lỗi: {anh_path}")
            status = "Fail"
            pytest.fail(f"Kết quả thực tế: {ketqua_thuc_te} != Kết quả mong đợi: {ketquamongdoi}")

    except Exception as e:
        # Nếu có lỗi bất ngờ, vẫn ghi báo cáo Fail
        ketqua_thuc_te = str(e)
        status = "Fail"
        print(f" Lỗi trong test với {email}: {e}")
        raise e

    finally:
        # --- Ghi báo cáo ---
        if not hasattr(test_cap_nhat_thong_tin, "stt_counter"):
            test_cap_nhat_thong_tin.stt_counter = 1
        stt = test_cap_nhat_thong_tin.stt_counter
        test_cap_nhat_thong_tin.stt_counter += 1

        report.add_row(
            stt, email, matkhau, ten, ho, tenhienthi, dcemail,
            matkhauhientai, matkhaumoi, nhaplaimk,
            ketquamongdoi, ketqua_thuc_te, status
        )
        report.save()
