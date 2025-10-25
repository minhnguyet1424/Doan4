from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from base.base_page import BasePage


class TrangDangKy(BasePage):
    # --- Locators ---
    TEN_TK = (By.ID, "reg_username")
    EMAIL = (By.ID, "reg_email")
    MATKHAU = (By.ID, "reg_password")
    BTN_DANGKY = (By.NAME, "register")
    TB_LOI = (By.CSS_SELECTOR, "ul[role='alert']")
    TB_THANHCONG = (
        By.CSS_SELECTOR,
        "body > div:nth-child(2) > div:nth-child(3) > main:nth-child(2) > "
        "div:nth-child(1) > article:nth-child(1) > div:nth-child(1) > "
        "div:nth-child(1) > div:nth-child(2) > p:nth-child(2)"
    )
    TB_VE_MK = (By.ID, "password_strength")

    # --- Khởi tạo ---
    def __init__(self, driver, url_dang_ky, timeout=10):
        super().__init__(driver, timeout)
        self.url_dang_ky = url_dang_ky

    # --- Mở trang đăng ký ---
    def mo_trang_dang_ky(self):
        self.mo_trang(self.url_dang_ky)

    # --- Hành động nhập ---
    def nhap_ten_tai_khoan(self, tentaikhoan):
        self.nhap_text(self.TEN_TK, tentaikhoan)

    def nhap_email(self, email):
        self.nhap_text(self.EMAIL, email)

    def nhap_mat_khau(self, matkhau):
        self.nhap_text(self.MATKHAU, matkhau)

    def bam_dang_ky(self):
        self.bam(self.BTN_DANGKY)

    # --- LẤY THÔNG BÁO HTML5 ---
    def lay_thong_bao_html5(self):
        """
        Trích xuất thông báo validationMessage của các trường input HTML5.
        Dùng cho các lỗi kiểu: 'Please fill out this field', 
        'Please include an "@" in the email address'...
        """
        fields = [self.TEN_TK, self.EMAIL, self.MATKHAU]
        for field in fields:
            try:
                element = self.driver.find_element(*field)
                msg = element.get_attribute("validationMessage")
                if msg and msg.strip():
                    return msg.strip()
            except NoSuchElementException:
                continue
        return None

    # --- Lấy thông báo phản hồi (tích hợp HTML5) ---
    def lay_thong_bao(self, timeout=10):
    
        #Thứ tự ưu tiên:Nếu có thông báo HTML5 → trả về ngay, Nếu nút Đăng ký bị disable → chỉ lấy thông báo độ mạnh mật khẩu, Nếu nút enable → lấy lỗi hoặc thành công.
        #  Kiểm tra thông báo HTML5 trước 
        msg_html5 = self.lay_thong_bao_html5()
        if msg_html5:
            return msg_html5

        #  Kiểm tra trạng thái nút Đăng ký
        try:
            btn = self.driver.find_element(*self.BTN_DANGKY)
            nut_disable = not btn.is_enabled()
        except NoSuchElementException:
            nut_disable = False

        # Nếu nút bị disable: chỉ lấy thông báo mật khẩu 
        if nut_disable:
            try:
                tb_mk = self.cho_phan_tu_xuat_hien(self.TB_VE_MK, timeout)
                if tb_mk.text.strip():
                    return f"Độ mạnh mật khẩu: {tb_mk.text.strip()}"
            except TimeoutException:
                pass
            return "Nút đăng ký bị vô hiệu hóa - không có thông báo mật khẩu"

        # --- Nếu nút enable: lấy lỗi hoặc thành công ---
        # Thông báo lỗi
        try:
            tb_loi = self.cho_phan_tu_xuat_hien(self.TB_LOI, timeout)
            lis = tb_loi.find_elements(By.TAG_NAME, "li")
            if lis:
                return " | ".join([li.text.strip() for li in lis if li.text.strip()])
            if tb_loi.text.strip():
                return tb_loi.text.strip()
        except TimeoutException:
            pass

        # Thông báo thành công
        try:
            tb_tc = self.cho_phan_tu_xuat_hien(self.TB_THANHCONG, timeout)
            if tb_tc.text.strip():
                return tb_tc.text.strip()
        except TimeoutException:
            pass

        # --- Không tìm thấy gì ---
        return "Không tìm thấy thông báo"
