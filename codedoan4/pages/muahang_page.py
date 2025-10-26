from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base.base_page import BasePage
import time

class TrangMuaNgay(BasePage):
    """Trang chi tiết sản phẩm và thanh toán trực tiếp."""

    # Locators
    BTN_MUA_NGAY = (By.NAME, "wd-add-to-cart")
    TEN = (By.ID, "billing_first_name")
    DIA_CHI = (By.ID, "billing_address_1")
    THANH_PHO = (By.ID, "billing_city")
    SDT = (By.ID, "billing_phone")
    EMAIL = (By.ID, "billing_email")
    GHI_CHU = (By.ID, "order_comments")
    BTN_DAT_HANG = (By.ID, "place_order")

    # Thông báo
    TB_THANH_CONG = (By.CSS_SELECTOR, ".woocommerce-notice.woocommerce-notice--success.woocommerce-thankyou-order-received")  # trang xác nhận đơn
    TB_LOI = (By.CSS_SELECTOR, ".woocommerce-error")

    def bam_mua_ngay(self):
        """Click nút 'Mua ngay' rồi đi tới trang thanh toán."""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.BTN_MUA_NGAY))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(1)
            btn.click()
        except TimeoutException:
            raise Exception(" Không tìm thấy nút Mua ngay.")

    def nhap_thong_tin_checkout(self, ten, email, sdt, diachi, thanhpho, ghi_chu=""):
        """Điền thông tin thanh toán."""
        self.nhap_text(self.TEN, ten)
        self.nhap_text(self.EMAIL, email)
        self.nhap_text(self.SDT, sdt)
        self.nhap_text(self.DIA_CHI, diachi)
        self.nhap_text(self.THANH_PHO, thanhpho)
        self.nhap_text(self.GHI_CHU, ghi_chu)

    def dat_hang(self):
        """Click nút Đặt hàng."""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.BTN_DAT_HANG))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(1)
            btn.click()
        except TimeoutException:
            raise Exception(" Không tìm thấy nút Đặt hàng.")

    def lay_thong_bao_dat_hang(self):
        """Lấy thông báo thành công hoặc lỗi sau khi đặt hàng."""
        try:
            tb = self.wait.until(EC.visibility_of_element_located(self.TB_THANH_CONG))
            return tb.text.strip()
        except TimeoutException:
            try:
                tb = self.driver.find_element(*self.TB_LOI)
                return tb.text.strip()
            except:
                return "Không thấy thông báo"
