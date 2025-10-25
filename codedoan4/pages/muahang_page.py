# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
# from base.base_page import BasePage
# from selenium.common.exceptions import TimeoutException

# class TrangGioHang(BasePage):
#     """Page Object cho giỏ hàng & checkout."""

#     # --- Locators ---
#     BTN_ADD_TO_CART = (By.NAME, "add-to-cart")  # thêm giỏ hàng
#     BTN_THANH_TOAN = (By.CSS_SELECTOR, ".button.checkout.wc-forward")  # nút Thanh toán click chuyển sang trang thông tin thanh toán 

#     # --- Các trường checkout ---
#     TEN = (By.ID, "billing_first_name")
#     DIA_CHI = (By.ID, "billing_address_1")
#     THANHPHO = (By.ID, "billing_city")
#     SDT = (By.ID, "billing_phone")
#     DCEMAIL = (By.ID, "billing_email")
#     GHICHU = (By.ID, "order_comments")
#     BTN_DAT_HANG = (By.ID, "place_order")# nút Đặt hàng

#     THONG_BAO_THANH_CONG = (By.CSS_SELECTOR, ".woocommerce-NoticeGroup.woocommerce-NoticeGroup-checkout")
#     THONG_BAO_LOI = (By.CSS_SELECTOR, ".woocommerce-error")
#     THONG_BAO_HET_HANG = (By.CSS_SELECTOR, "p.stock.out-of-stock span")

#     # --- Các hành động ---
#     def them_vao_gio(self):
#         """Click nút Thêm vào giỏ trên trang chi tiết SP."""
#         btn = self.wait.until(EC.element_to_be_clickable(self.BTN_ADD_TO_CART))
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
#         btn.click()

#     def vao_checkout(self):
#         """Click nút Thanh toán để vào trang checkout."""
#         btn = self.wait.until(EC.element_to_be_clickable(self.BTN_THANH_TOAN))
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
#         btn.click()

#     def nhap_thong_tin_checkout(self, ten, email, phone, dia_chi, tinh, ghi_chu=""):
#         self.nhap_text(self.TEN, ten)
#         self.nhap_text(self.DCEMAIL, email)
#         self.nhap_text(self.SDT, phone)
#         self.nhap_text(self.DIA_CHI, dia_chi)
#         self.nhap_text(self.GHICHU, ghi_chu)
#         # Chọn Tỉnh/Thành phố nếu có dropdown
#         try:
#             select_tinh = Select(self.driver.find_element(*self.THANHPHO))
#             select_tinh.select_by_visible_text(tinh)
#         except Exception:
#             pass

#     def dat_hang(self):
#         btn = self.wait.until(EC.element_to_be_clickable(self.BTN_DAT_HANG))
#         btn.click()

#     def lay_thong_bao_dat_hang(self):
#         try:
#             tb = self.wait.until(EC.visibility_of_element_located(self.THONG_BAO_THANH_CONG))
#             return tb.text.strip()
#         except TimeoutException:
#             pass
#         try:
#             tb = self.driver.find_element(*self.THONG_BAO_LOI)
#             return tb.text.strip()
#         except:
#             pass
#         try:
#             tb = self.driver.find_element(*self.THONG_BAO_HET_HANG)
#             return tb.text.strip()
#         except:
#             return "Không tìm thấy thông báo"


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base.base_page import BasePage
import time

class TrangGioHang(BasePage):
    """Page Object cho giỏ hàng & checkout."""

    # --- Locators ---
    BTN_ADD_TO_CART = (By.NAME, "add-to-cart")
    BTN_THANH_TOAN = (By.CSS_SELECTOR, ".button.checkout.wc-forward")  # nút Thanh toán

    # --- Trường checkout ---
    TEN = (By.ID, "billing_first_name")
    DIA_CHI = (By.ID, "billing_address_1")
    THANHPHO = (By.ID, "billing_city")
    SDT = (By.ID, "billing_phone")
    DCEMAIL = (By.ID, "billing_email")
    GHICHU = (By.ID, "order_comments")
    BTN_DAT_HANG = (By.ID, "place_order")

    # --- Thông báo ---
    THONG_BAO_THANH_CONG = (By.CSS_SELECTOR, ".woocommerce-NoticeGroup.woocommerce-NoticeGroup-checkout")
    THONG_BAO_LOI = (By.CSS_SELECTOR, ".woocommerce-error")
    THONG_BAO_HET_HANG = (By.CSS_SELECTOR, "p.stock.out-of-stock span")

    # --- Hàm hành động ---
    def them_vao_gio(self):
        """Click nút Thêm vào giỏ trên trang chi tiết SP."""
        btn = self.wait.until(EC.element_to_be_clickable(self.BTN_ADD_TO_CART))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(1)
        btn.click()
        print("[INFO] ✅ Đã thêm sản phẩm vào giỏ hàng.")

    def vao_checkout(self):
        """Chờ hiển thị nút Thanh toán rồi click để sang trang checkout."""
        try:
            print("[INFO] ⏳ Đang chờ nút Thanh toán hiển thị...")
            # Chờ nút xuất hiện (max 15s)
            self.wait.until(EC.presence_of_element_located(self.BTN_THANH_TOAN))
            time.sleep(2)

            btn = self.wait.until(EC.element_to_be_clickable(self.BTN_THANH_TOAN))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(1)
            try:
                btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)
            print("[INFO] ✅ Đã click nút Thanh toán, chuyển sang trang checkout.")
        except TimeoutException:
            print("[ERROR] ❌ Không tìm thấy nút Thanh toán sau khi thêm giỏ hàng.")
            raise

    def nhap_thong_tin_checkout(self, ten, email, phone, dia_chi, tinh, ghi_chu=""):
        """Nhập đầy đủ thông tin thanh toán."""
        self.nhap_text(self.TEN, ten)
        self.nhap_text(self.DCEMAIL, email)
        self.nhap_text(self.SDT, phone)
        self.nhap_text(self.DIA_CHI, dia_chi)
        self.nhap_text(self.GHICHU, ghi_chu)

        # Chọn tỉnh/thành phố nếu có dropdown
        try:
            select_tinh = Select(self.driver.find_element(*self.THANHPHO))
            select_tinh.select_by_visible_text(tinh)
        except Exception:
            pass

    def dat_hang(self):
        """Click nút Đặt hàng."""
        btn = self.wait.until(EC.element_to_be_clickable(self.BTN_DAT_HANG))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(1)
        btn.click()
        print("[INFO] ✅ Đã bấm nút Đặt hàng.")

    def lay_thong_bao_dat_hang(self):
        """Lấy thông báo sau khi đặt hàng."""
        try:
            tb = self.wait.until(EC.visibility_of_element_located(self.THONG_BAO_THANH_CONG))
            return tb.text.strip()
        except TimeoutException:
            pass
        try:
            tb = self.driver.find_element(*self.THONG_BAO_LOI)
            return tb.text.strip()
        except:
            pass
        try:
            tb = self.driver.find_element(*self.THONG_BAO_HET_HANG)
            return tb.text.strip()
        except:
            return "Không tìm thấy thông báo"
