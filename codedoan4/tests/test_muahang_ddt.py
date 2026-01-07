import pytest
import time
from pages.timkiem_page import TrangTimKiem
from pages.muahang_page import TrangMuaNgay
from utils.report_helper import ExcelReport

REPORT_FILE = "reports/report.xlsx"

# ================== REPORT ==================
@pytest.fixture(scope="module")
def report():
    header = [
        "STT", "Từ khóa", "Tên SP", "Tên KH", "Địa chỉ", "Thành phố",
        "SĐT", "Email", "Ghi chú", "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
    ]
    return ExcelReport(REPORT_FILE, sheet_name="MuaNgay", tieu_de_base="Báo cáo Mua Ngay", header=header)

# ================== TEST ==================
def test_mua_ngay(cau_hinh, tukhoa, tensp, ten, diachi, thanhpho, sdt, email, ghichu, ketquamongdoi, report, logger):
    driver = cau_hinh["driver"]

    # --- STT tự động ---
    if not hasattr(test_mua_ngay, "stt"):
        test_mua_ngay.stt = report.ws.max_row  # bắt đầu từ số dòng hiện tại
    stt = test_mua_ngay.stt

    try:
        logger.info(f"\n=== TEST CASE {stt} ===")
        logger.info(f"Bắt đầu test Mua Ngay | Từ khóa='{tukhoa}', Sản phẩm='{tensp}'")

        # --- Mở trang tìm kiếm ---
        trang_tim_kiem = TrangTimKiem(driver)
        logger.info("Mở trang tìm kiếm")
        trang_tim_kiem.mo_trang_tim_kiem()
        logger.info(f"Nhập từ khóa tìm kiếm: {tukhoa}")
        trang_tim_kiem.nhap_tu_khoa(tukhoa)
        trang_tim_kiem.bam_tim_kiem()
        time.sleep(2)

        # --- Chọn sản phẩm ---
        if not trang_tim_kiem.chon_san_pham_theo_ten(tensp):
            ketqua_thuc_te = "Không tìm thấy sản phẩm phù hợp."
            status = "Fail"
            logger.warning(ketqua_thuc_te)
        else:
            # --- Điền thông tin checkout ---
            gio_hang = TrangMuaNgay(driver)
            logger.info(f"Điền thông tin checkout cho KH: {ten}, {email}, {sdt}, {diachi}, {thanhpho}")
            gio_hang.nhap_thong_tin_checkout(ten, email, sdt, diachi, thanhpho, ghi_chu=ghichu)
            gio_hang.dat_hang()
            time.sleep(2)

            # --- Lấy kết quả ---
            ketqua_thuc_te = gio_hang.lay_thong_bao_dat_hang()
            if ketquamongdoi.lower() in ketqua_thuc_te.lower():
                status = "Pass"
                logger.info(f"Đặt hàng thành công: {ketqua_thuc_te}")
            else:
                status = "Fail"
                logger.warning(f"Đặt hàng thất bại: {ketqua_thuc_te}")

    except Exception as e:
        ketqua_thuc_te = f"Lỗi exception: {e}"
        status = "Fail"
        logger.error(ketqua_thuc_te, exc_info=True)

    finally:
        # --- Ghi vào báo cáo Excel ---
        report.add_row(
            stt, tukhoa, tensp, ten, diachi, thanhpho, sdt, email, ghichu,
            ketquamongdoi, ketqua_thuc_te, status
        )
        report.save()
        logger.info(f"[END] Test Mua Ngay: STT={stt}, Status={status}")

        # --- Tăng STT cho test case tiếp theo ---
        test_mua_ngay.stt += 1

    # --- Assert để pytest báo Fail ---
    assert ketquamongdoi.lower() in ketqua_thuc_te.lower(), f"{ketqua_thuc_te} != {ketquamongdoi}"
