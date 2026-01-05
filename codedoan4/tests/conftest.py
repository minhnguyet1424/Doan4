import pytest
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# CẤU HÌNH LOGS 
LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)
@pytest.fixture(scope="module")
def logger(request):
    import os, logging
    os.makedirs("logs", exist_ok=True)

    test_file = os.path.basename(request.node.fspath)  # tên file test
    base_name = os.path.splitext(test_file)[0]
    log_file = f"logs/{base_name}.log"

    # Xóa log cũ để ghi đè
    if os.path.exists(log_file):
        os.remove(log_file)

    logger = logging.getLogger(base_name)
    logger.setLevel(logging.INFO)

    # tránh tạo handler trùng
    if not logger.handlers:
        fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        ch = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
        fh.setFormatter(fmt)
        ch.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(ch)

    logger.info(f"===== BẮT ĐẦU TEST FILE: {test_file} =====")
    yield logger
    logger.info(f"===== KẾT THÚC TEST FILE: {test_file} =====")

# TÙY CHỌN DỮ LIỆU VÀO (excel/json/csv) 
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
    logging.info(" Chrome driver đã đóng")
