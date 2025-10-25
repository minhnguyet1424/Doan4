import pytest
import os
import time
import logging
import allure

# ==================== CẤU HÌNH LOGS & SCREENSHOTS ==================== #
LOG_FOLDER = "logs"
SCREENSHOT_FOLDER = "fail_screenshots"
os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_FOLDER, "test_log.log"),
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ==================== TÙY CHỌN DỮ LIỆU VÀO (excel/json/csv) ==================== #
# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--data-mode",
        action="store",
        default="excel",
        help="Chọn kiểu dữ liệu đầu vào: excel, csv, json"
    )

@pytest.fixture
def data_mode(request):
    return request.config.getoption("--data-mode")

# ==================== FIXTURE KHỞI TẠO WEBDRIVER ==================== #
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def cau_hinh():
    """Khởi tạo ChromeDriver, trả về trong dict 'cau_hinh'."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    config = {"driver": driver}
    logging.info(" Chrome driver khởi tạo thành công")

    yield config

    driver.quit()
    logging.info("🧹 Chrome driver đã đóng")
