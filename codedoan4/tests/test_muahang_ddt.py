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
    return ExcelReport(
        REPORT_FILE,
        sheet_name="MuaNgay",
        tieu_de_base="Báo cáo Mua Ngay",
        header=header
    )
# ================== TEST ==================
def test_mua_ngay(
    cau_hinh, tukhoa, tensp, ten, diachi,
    thanhpho, sdt, email, ghichu,
    ketquamongdoi, report, logger
):
    driver = cau_hinh["driver"]

    if not hasattr(test_mua_ngay, "stt"):
        test_mua_ngay.stt = 1
    stt = test_mua_ngay.stt

    ketqua_thuc_te = ""
    status = "Fail"

    try:
        logger.info(f"\n=== TEST CASE {stt} ===")
        logger.info(
            f"Bắt đầu test Mua Ngay | Từ khóa='{tukhoa}', Sản phẩm='{tensp}'"
        )

        # ===== 1. TÌM KIẾM =====
        trang_tim_kiem = TrangTimKiem(driver)
        trang_tim_kiem.mo_trang_tim_kiem()
        trang_tim_kiem.nhap_tu_khoa(tukhoa)
        trang_tim_kiem.bam_tim_kiem()
        time.sleep(2)

        # ===== 2. CHỌN SẢN PHẨM =====
        if not trang_tim_kiem.chon_san_pham_theo_ten(tensp):
            ketqua_thuc_te = "Không tìm thấy sản phẩm phù hợp"
            logger.info(f"Kết quả thực tế: {ketqua_thuc_te}")
        else:
            gio_hang = TrangMuaNgay(driver)

            # ===== 3. MUA NGAY =====
            logger.info("Đã nhấn nút Mua Ngay")
            gio_hang.bam_mua_ngay()
            time.sleep(3)

            # ===== 4. ĐIỀN THÔNG TIN =====
            logger.info(
                f"Đã nhập thông tin đặt hàng | Tên={ten}, Email={email}, "
                f"SĐT={sdt}, Địa chỉ={diachi}, Thành phố={thanhpho}"
            )
            gio_hang.nhap_thong_tin_dat_hang(
                ten=ten,
                email=email,
                sdt=sdt,
                diachi=diachi,
                thanhpho=thanhpho,
                ghi_chu=ghichu
            )

            # ===== 5. ĐẶT HÀNG =====
            logger.info("Đã nhấn nút Đặt hàng")
            gio_hang.dat_hang()

            # ===== 6. KẾT QUẢ =====
            ketqua_thuc_te = gio_hang.lay_thong_bao_dat_hang()
            logger.info(f"Kết quả thực tế: {ketqua_thuc_te}")

            if ketquamongdoi.lower() in ketqua_thuc_te.lower():
                status = "Pass"

        logger.info(
            f"Kết quả mong đợi: {ketquamongdoi} | Trạng thái: {status}"
        )

    except Exception as e:
        ketqua_thuc_te = f"Lỗi exception: {e}"
        status = "Fail"
        logger.error(f"Kết quả thực tế: {ketqua_thuc_te}", exc_info=True)
        logger.info(
            f"Kết quả mong đợi: {ketquamongdoi} | Trạng thái: {status}"
        )

    finally:
        report.add_row(
            stt, tukhoa, tensp, ten, diachi,
            thanhpho, sdt, email, ghichu,
            ketquamongdoi, ketqua_thuc_te, status
        )
        report.save()

        logger.info(f"Đã xóa cookie sau test")
        test_mua_ngay.stt += 1

    assert ketquamongdoi.lower() in ketqua_thuc_te.lower(), \
        f"{ketqua_thuc_te} != {ketquamongdoi}"
