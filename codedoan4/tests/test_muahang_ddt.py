import pytest
import time
from pages.dangnhap_page import TrangDangNhap
from pages.timkiem_page import TrangTimKiem
from pages.muahang_page import TrangGioHang
from base.config import URL_DANG_NHAP
from utils.data_utils import doc_du_lieu_muahang_excel
from utils.report_helper import ExcelReport

REPORT_FILE = "reports/report.xlsx"

# ========================== FIXTURE TẠO REPORT ========================== #
@pytest.fixture(scope="module")
def report():
    header = [
        "STT", "Thời gian", "Email", "Mật khẩu", "Từ khóa tìm kiếm", "Tên SP",
        "Tên", "Địa chỉ", "Thành phố", "SĐT", "ĐC Email", "Ghi chú",
        "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
    ]
    return ExcelReport(REPORT_FILE, sheet_name="MuaHang", tieu_de_base="Báo cáo Mua Hàng", header=header)

# ========================== PARAMETRIZE DATA ========================== #
def pytest_generate_tests(metafunc):
    if "email" in metafunc.fixturenames:
        duong_dan = "data/input_case.xlsx"
        test_cases = doc_du_lieu_muahang_excel(duong_dan, ten_sheet="Muahang")
        metafunc.parametrize(
            "email, matkhau, tukhoatimkiem, tensp, ten, diachi, thanhpho, sdt, dcemail, ghichu, ketquamongdoi",
            test_cases
        )

# ========================== TEST CASE MUA HÀNG ========================== #
def test_mua_hang_ddt(cau_hinh, email, matkhau, tukhoatimkiem, tensp, ten, diachi,
                       thanhpho, sdt, dcemail, ghichu, ketquamongdoi, report):
    driver = cau_hinh["driver"]

    # --- 1️⃣ Đăng nhập ---
    trang_dang_nhap = TrangDangNhap(driver, URL_DANG_NHAP)
    trang_dang_nhap.mo_trang_dang_nhap()
    trang_dang_nhap.nhap_email(email)
    trang_dang_nhap.nhap_mat_khau(matkhau)
    trang_dang_nhap.bam_dang_nhap()
    time.sleep(2)

    # --- 2️⃣ Tìm kiếm sản phẩm ---
    trang_tim_kiem = TrangTimKiem(driver)
    trang_tim_kiem.mo_trang_tim_kiem()
    trang_tim_kiem.nhap_tu_khoa(tukhoatimkiem)
    trang_tim_kiem.bam_tim_kiem()
    time.sleep(10)

    # --- 3️⃣ Chọn sản phẩm theo tên ---
    da_chon = trang_tim_kiem.chon_san_pham_theo_ten(tensp)
    if not da_chon:
        print(f"[!] Không tìm thấy sản phẩm: {tensp}")
        ketqua_thuc_te = f"Không tìm thấy sản phẩm: {tensp}"
        status = "Fail"
        # Ghi báo cáo rồi dừng test
        if not hasattr(test_mua_hang_ddt, "stt_counter"):
            test_mua_hang_ddt.stt_counter = 1
        stt = test_mua_hang_ddt.stt_counter
        test_mua_hang_ddt.stt_counter += 1
        report.add_row(
            stt, email, matkhau, tukhoatimkiem, tensp, ten,
            diachi, thanhpho, sdt, dcemail, ghichu,
            ketquamongdoi, ketqua_thuc_te, status
        )
        report.save()
        assert False, ketqua_thuc_te

    # --- 4️⃣ Thêm vào giỏ hàng & vào giỏ ---
    trang_gio_hang = TrangGioHang(driver)
    trang_gio_hang.them_vao_gio()
    time.sleep(8)
    trang_gio_hang.vao_checkout()
    time.sleep(10)

    # --- 5️⃣ Điền thông tin thanh toán ---
    trang_gio_hang.nhap_thong_tin_checkout(
        ten=ten,
        email=dcemail or email,
        phone=sdt,
        dia_chi=diachi,
        tinh=thanhpho,
        ghi_chu=ghichu
    )

    trang_gio_hang.dat_hang()
    time.sleep(3)

    # --- 6️⃣ Lấy kết quả thực tế ---
    ketqua_thuc_te = trang_gio_hang.lay_thong_bao_dat_hang()
    status = "Pass" if ketquamongdoi.lower() in ketqua_thuc_te.lower() else "Fail"

    # --- 7️⃣ STT tự động ---
    if not hasattr(test_mua_hang_ddt, "stt_counter"):
        test_mua_hang_ddt.stt_counter = 1
    stt = test_mua_hang_ddt.stt_counter
    test_mua_hang_ddt.stt_counter += 1

    # --- 8️⃣ Ghi báo cáo ---
    report.add_row(
        stt, email, matkhau, tukhoatimkiem, tensp, ten,
        diachi, thanhpho, sdt, dcemail, ghichu,
        ketquamongdoi, ketqua_thuc_te, status
    )
    report.save()

    # --- 9️⃣ Assert kết quả ---
    assert ketquamongdoi.lower() in ketqua_thuc_te.lower(), f"{ketqua_thuc_te} != {ketquamongdoi}"
