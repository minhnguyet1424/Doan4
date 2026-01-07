from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from base.base_page import BasePage
import time


class TrangMuaNgay(BasePage):
    """Trang chi tiết sản phẩm và thanh toán"""

    # ===== LOCATORS =====
    BTN_MUA_NGAY = (By.NAME, "wd-add-to-cart")

    TEN = (By.ID, "billing_first_name")
    EMAIL = (By.ID, "billing_email")
    SDT = (By.ID, "billing_phone")
    DIA_CHI = (By.ID, "billing_address_1")
    THANH_PHO = (By.ID, "billing_city")
    GHI_CHU = (By.ID, "order_comments")

    BTN_DAT_HANG = (By.ID, "place_order")

    TB_THANH_CONG = (
        By.CSS_SELECTOR,
        ".woocommerce-notice.woocommerce-notice--success.woocommerce-thankyou-order-received"
    )
    TB_LOI = (By.CSS_SELECTOR, ".woocommerce-error")

    # ===== ACTIONS =====

    def bam_mua_ngay(self):
        """
        Click nút Mua ngay nếu còn ở trang sản phẩm.
        Nếu đã sang checkout thì bỏ qua.
        """
        try:
            btns = self.driver.find_elements(*self.BTN_MUA_NGAY)
            if btns:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btns[0]
                )
                time.sleep(0.5)
                btns[0].click()
                time.sleep(2)
        except Exception:
            pass  # bỏ qua nếu đã ở checkout

    def nhap_thong_tin_dat_hang(self, ten, email, sdt, diachi, thanhpho, ghi_chu=""):
        self.nhap_text(self.TEN, ten)
        self.nhap_text(self.EMAIL, email)
        self.nhap_text(self.SDT, sdt)
        self.nhap_text(self.DIA_CHI, diachi)
        self.nhap_text(self.THANH_PHO, thanhpho)
        self.nhap_text(self.GHI_CHU, ghi_chu)

    def dat_hang(self):
        """
        Click nút Đặt hàng – xử lý STALE ELEMENT cho WooCommerce
        """
        for _ in range(3):
            try:
                btn = self.wait.until(
                    EC.element_to_be_clickable(self.BTN_DAT_HANG)
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn
                )
                time.sleep(0.5)
                btn.click()
                return
            except StaleElementReferenceException:
                time.sleep(1)

        raise Exception("❌ Không thể click nút Đặt hàng (stale element)")

    def lay_thong_bao_dat_hang(self):
        try:
            tb = self.wait.until(
                EC.visibility_of_element_located(self.TB_THANH_CONG)
            )
            return tb.text.strip()
        except TimeoutException:
            try:
                return self.driver.find_element(*self.TB_LOI).text.strip()
            except:
                return "Không thấy thông báo"
