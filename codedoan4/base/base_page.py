import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    # --- Mở trang web ---
    def mo_trang(self, url):
        """Đi đến URL chỉ định."""
        self.driver.get(url)
    # --- Click vào phần tử ---
    def bam(self, locator):
        """Chờ phần tử có thể click được rồi mới click."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()
    # --- Nhập text vào ô ---
    def nhap_text(self, locator, text):
        """Nhập text vào ô nhập liệu sau khi nó hiển thị."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
      # # --- Lấy text từ phần tử ---
    def lay_text(self, locator):
        """Trả về text của phần tử hiển thị."""
        return self.wait.until(EC.visibility_of_element_located(locator)).text
    # --- Chờ phần tử xuất hiện (hiển thị trên trang) ---
    def cho_phan_tu_xuat_hien(self, locator, timeout=10):
        """Chờ đến khi phần tử hiển thị trên trang (visible)."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))
    # --- Chờ phần tử có thể click ---
    def cho_phan_tu_co_the_click(self, locator, timeout=10):
        """Chờ đến khi phần tử có thể click được."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator))
    # --- Lưu ảnh chụp màn hình ---
    def save_screenshot(self, name=None):
        """Lưu screenshot vào thư mục fail_screenshots và trả về đường dẫn."""
        folder = "fail_screenshots"
        os.makedirs(folder, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        path = os.path.join(folder, filename)
        try:
            self.driver.save_screenshot(path)
        except Exception as e:
            print(f"[WARNING] Chụp screenshot thất bại: {e}")
            return None
        return path
