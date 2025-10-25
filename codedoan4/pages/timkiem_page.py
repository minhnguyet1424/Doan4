from selenium.webdriver.common.by import By 
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from base.base_page import BasePage 
from base.config import BASE_URL 
 
class TrangTimKiem(BasePage): 
    """Trang tìm kiếm sản phẩm.""" 
 
    TIM_KIEM = (By.CSS_SELECTOR, "div[class='wd-search-form wd-header-search-form wd-display-form whb-9x1ytaxq7aphtb3npidp'] input[placeholder='Tìm kiếm sản phẩm']") 
    BTN_TIM_KIEM = (By.CSS_SELECTOR, "body > div:nth-child(2) > header:nth-child(1) button[type='submit']") 
    SP_DAU_TIEN = (By.CSS_SELECTOR, "div.wd-product h3 a") 
    TB_KHONG_TIM_THAY_SP = (By.CSS_SELECTOR, "div[role='status']") 
    SP_LIST = (By.CSS_SELECTOR, "div.wd-content-area.site-content.wd-grid-col h3 a")  # Lấy trực tiếp link sản phẩm

    def __init__(self, driver, timeout=10): 
        super().__init__(driver, timeout) 
        self.url_trang_chu = BASE_URL 
        self.wait = WebDriverWait(driver, timeout) 
 
    def mo_trang_tim_kiem(self): 
        self.mo_trang(self.url_trang_chu) 
 
    def nhap_tu_khoa(self, tu_khoa): 
        element = self.wait.until(EC.visibility_of_element_located(self.TIM_KIEM)) 
        element.clear() 
        element.send_keys(tu_khoa) 
 
    def bam_tim_kiem(self): 
        element = self.wait.until(EC.element_to_be_clickable(self.BTN_TIM_KIEM)) 
        element.click() 
 
    def lay_san_pham_dau_tien(self): 
        try: 
            sps = self.wait.until(EC.visibility_of_all_elements_located(self.SP_DAU_TIEN)) 
            sps = self.driver.find_elements(*self.SP_DAU_TIEN) 
            if sps: 
                return sps[0].text.strip() 
        except TimeoutException: 
            pass 
 
        try: 
            tb = self.driver.find_element(*self.TB_KHONG_TIM_THAY_SP) 
            return tb.text.strip() 
        except NoSuchElementException: 
            return "Không tìm thấy kết quả" 
 
    def chon_san_pham_theo_ten(self, tensp): 
        """Chọn sản phẩm theo tên: click vào sản phẩm rồi click add-to-cart""" 
        try: 
            # Chờ các link sản phẩm load xong 
            self.wait.until(EC.presence_of_all_elements_located(self.SP_LIST)) 
            sps = self.driver.find_elements(*self.SP_LIST) 
 
            for link_sp in sps: 
                try: 
                    ten = link_sp.text.strip() 
                    if ten == tensp: 
                        # Scroll và click vào sản phẩm 
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", link_sp) 
                        link_sp.click() 
 
                        # Chờ nút add-to-cart trên trang chi tiết 
                        btn_add = self.wait.until(EC.element_to_be_clickable((By.NAME, "add-to-cart"))) 
                        btn_add.click() 
                        return True 
                except Exception: 
                    continue  # Nếu sản phẩm nào lỗi thì bỏ qua 
        except TimeoutException: 
            return False 
 
        return False  # Không tìm thấy sản phẩm
