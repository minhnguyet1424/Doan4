from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from base.base_page import BasePage
import time
class TrangThongTinTaiKhoan(BasePage):
    # --- Locators ---
    HO = (By.ID, "account_last_name")
    TEN = (By.ID, "account_first_name")
    TEN_HIEN_THI = (By.ID, "account_display_name")
    EMAIL = (By.ID, "account_email")
    MAT_KHAU_HIEN_TAI = (By.ID, "password_current")
    PASS_MOI = (By.ID, "password_1")
    XAC_NHAN_PASS_MOI = (By.ID, "password_2")
    BTN_LUU = (By.NAME, "save_account_details")
    THONG_BAO_THANH_CONG = (By.CLASS_NAME, "woocommerce-message")
    THONG_BAO_LOI = (By.CLASS_NAME, "woocommerce-error")
    THONG_BAO_DO_MANH_MK = (By.CSS_SELECTOR, "#password_strength")
    def __init__(self, driver, url_edit_account):
        super().__init__(driver)
        self.url_edit_account = url_edit_account
    # --- MỞ TRANG HỒ SƠ --- #
    def mo_trang_thong_tin(self):
        self.mo_trang(self.url_edit_account)
# --- CẬP NHẬT THÔNG TIN --- #
    def cap_nhat_thong_tin(
        self,  ten=None,ho=None, ten_hien_thi=None,
        email=None, mk_hien_tai=None, mk_moi=None, xac_nhan_mk=None):
        """Nhập thông tin cập nhật và bấm lưu."""   
        if ten is not None:
            self.nhap_text(self.TEN, ten)
        if ho is not None:
            self.nhap_text(self.HO, ho)
        if ten_hien_thi is not None:
            self.nhap_text(self.TEN_HIEN_THI, ten_hien_thi)
        if email is not None:
            self.nhap_text(self.EMAIL, email)
        if mk_hien_tai is not None:
            self.nhap_text(self.MAT_KHAU_HIEN_TAI, mk_hien_tai)
        if mk_moi is not None:
            self.nhap_text(self.PASS_MOI, mk_moi)
        if xac_nhan_mk is not None:
            self.nhap_text(self.XAC_NHAN_PASS_MOI, xac_nhan_mk)

        # Bấm nút Lưu (dùng JS click nếu bị chặn bởi HTML5)
        try:
            btn = self.cho_phan_tu_co_the_click(self.BTN_LUU)
            self.driver.execute_script("arguments[0].click();", btn)
        except TimeoutException:
            print("[!] Không tìm thấy nút Lưu để click")
        time.sleep(0.5)
    # --- LẤY THÔNG BÁO PHẢN HỒI --- #
    def lay_thong_bao(self):
        """Lấy thông báo thành công, lỗi, độ mạnh mật khẩu hoặc HTML5."""
        try:
            pt_loi = self.cho_phan_tu_xuat_hien(self.THONG_BAO_LOI)
            if pt_loi and pt_loi.text.strip():
                return pt_loi.text.strip()
        except TimeoutException:
            pass
        try:
            pt_ok = self.cho_phan_tu_xuat_hien(self.THONG_BAO_THANH_CONG)
            if pt_ok and pt_ok.text.strip():
                return pt_ok.text.strip()
        except TimeoutException:
            pass
        try:
            pt_mk = self.cho_phan_tu_xuat_hien(self.THONG_BAO_DO_MANH_MK)
            if pt_mk and pt_mk.text.strip():
                return pt_mk.text.strip()
        except TimeoutException:
            pass
        # Nếu không thấy thông báo, kiểm tra HTML5
        html5 = self.lay_thong_bao_html5()
        if html5:
            return html5
        return "Không thấy thông báo phản hồi"
    # --- LẤY THÔNG BÁO HTML5 --- #
    def lay_thong_bao_html5(self):
        """Trích thuộc tính validationMessage từ các input."""
        fields = [self.EMAIL, self.PASS_MOI, self.XAC_NHAN_PASS_MOI]
        for field in fields:
            try:
                element = self.driver.find_element(*field)
                msg = element.get_attribute("validationMessage")
                if msg and msg.strip():
                    return msg.strip()
            except NoSuchElementException:
                continue
        return None
    # --- LẤY ĐỘ MẠNH MẬT KHẨU --- #
    def lay_thong_bao_do_manh_mat_khau(self):
        """Trả về text cảnh báo độ mạnh mật khẩu."""
        try:
            pt = self.cho_phan_tu_xuat_hien(self.THONG_BAO_DO_MANH_MK)
            return pt.text.strip() if pt else "Không thấy cảnh báo độ mạnh mật khẩu"
        except TimeoutException:
            return "Không thấy cảnh báo độ mạnh mật khẩu"
