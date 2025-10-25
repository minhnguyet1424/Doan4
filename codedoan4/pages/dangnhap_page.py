from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from base.base_page import BasePage
class TrangDangNhap(BasePage):
    """Trang đăng nhập (Page Object)."""
    # --- Locators ---
    EMAIL = (By.ID, "username")
    MATKHAU = (By.ID, "password")
    BTN_DANGNHAP = (By.NAME, "login")
    TB_LOI = (By.CSS_SELECTOR, "ul[role='alert']")
    TB_THANHCONG = (
        By.CSS_SELECTOR,
        "body > div:nth-child(2) > div:nth-child(3) > main:nth-child(2) > ""div:nth-child(1) > article:nth-child(1) > div:nth-child(1) > ""div:nth-child(1) > div:nth-child(2) > p:nth-child(2)")
    def __init__(self, driver, url_dang_nhap, timeout=10):
        super().__init__(driver, timeout)
        self.url_dang_nhap = url_dang_nhap
    # --- Mở trang đăng nhập ---
    def mo_trang_dang_nhap(self):
        self.mo_trang(self.url_dang_nhap)
    # --- Hành động nhập liệu ---
    def nhap_email(self, email):
        self.nhap_text(self.EMAIL, email)
    def nhap_mat_khau(self, matkhau):
        self.nhap_text(self.MATKHAU, matkhau)
    def bam_dang_nhap(self):
        self.bam(self.BTN_DANGNHAP)
    # --- Lấy thông báo phản hồi ---
    def lay_thong_bao(self, timeout=10):
        #Trả về thông báo lỗi hoặc thành công sau khi đăng nhập.
        #Ưu tiên:Thông báo lỗi, Thông báo thành công  
        # 1 Thông báo lỗi
        try:
            tb_loi = self.cho_phan_tu_xuat_hien(self.TB_LOI, timeout)
            lis = tb_loi.find_elements(By.TAG_NAME, "li")
            if lis:
                return " | ".join([li.text.strip() for li in lis if li.text.strip()])
            if tb_loi.text.strip():
                return tb_loi.text.strip()
        except TimeoutException:
            pass
        # 2 Thông báo thành công
        try:
            tb_tc = self.cho_phan_tu_xuat_hien(self.TB_THANHCONG, timeout)
            if tb_tc.text.strip():
                return tb_tc.text.strip()
        except TimeoutException:
            pass
        return "Không tìm thấy thông báo"
