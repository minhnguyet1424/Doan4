# # import pytest
# # import os
# # import logging
# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.chrome.options import Options
# # from webdriver_manager.chrome import ChromeDriverManager

# # # CẤU HÌNH LOGS 
# # LOG_FOLDER = "logs"
# # os.makedirs(LOG_FOLDER, exist_ok=True)
# # @pytest.fixture(scope="module")
# # def logger(request):
# #     import os, logging
# #     os.makedirs("logs", exist_ok=True)

# #     test_file = os.path.basename(request.node.fspath)  # tên file test
# #     base_name = os.path.splitext(test_file)[0]
# #     log_file = f"logs/{base_name}.log"

# #     # Xóa log cũ để ghi đè
# #     if os.path.exists(log_file):
# #         os.remove(log_file)

# #     logger = logging.getLogger(base_name)
# #     logger.setLevel(logging.INFO)

# #     # tránh tạo handler trùng
# #     if not logger.handlers:
# #         fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
# #         ch = logging.StreamHandler()
# #         fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
# #         fh.setFormatter(fmt)
# #         ch.setFormatter(fmt)
# #         logger.addHandler(fh)
# #         logger.addHandler(ch)

# #     logger.info(f"===== BẮT ĐẦU TEST FILE: {test_file} =====")
# #     yield logger
# #     logger.info(f"===== KẾT THÚC TEST FILE: {test_file} =====")

# # # TÙY CHỌN DỮ LIỆU VÀO (excel/json/csv) 
# # # conftest.py
# # import pytest

# # def pytest_addoption(parser):
# #     parser.addoption(
# #         "--data-mode",
# #         action="store",
# #         default="excel",
# #         help="Chọn kiểu dữ liệu đầu vào: excel, csv, json"
# #     )
# # @pytest.fixture
# # def data_mode(request):
# #     return request.config.getoption("--data-mode")


# # @pytest.fixture(scope="function")
# # def cau_hinh():
# #     """Khởi tạo ChromeDriver, trả về trong dict 'cau_hinh'."""
# #     chrome_options = Options()
# #     chrome_options.add_argument("--start-maximized")
# #     chrome_options.add_argument("--disable-notifications")
# #     chrome_options.add_argument("--disable-infobars")
# #     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# #     service = Service(ChromeDriverManager().install())
# #     driver = webdriver.Chrome(service=service, options=chrome_options)

# #     config = {"driver": driver}
# #     logging.info(" Chrome driver khởi tạo thành công")

# #     yield config

# #     driver.quit()
# #     logging.info(" Chrome driver đã đóng")
# import pytest
# import os
# import logging
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# from utils.data_utils import (
#     doc_du_lieu_dang_ky_excel,
#     doc_du_lieu_dang_ky_csv,
#     doc_du_lieu_dang_ky_json
# )

# # ================== OPTION ==================
# def pytest_addoption(parser):
#     parser.addoption(
#         "--data-mode",
#         action="store",
#         default="excel",
#         help="Chọn kiểu dữ liệu đầu vào: excel, csv, json"
#     )

# # ================== PARAMETRIZE ==================
# def pytest_generate_tests(metafunc):
#     if "tentaikhoan" in metafunc.fixturenames:
#         data_mode = metafunc.config.getoption("--data-mode")

#         if data_mode == "excel":
#             test_cases = doc_du_lieu_dang_ky_excel(
#                 "data/input_case.xlsx", ten_sheet="Dangky"
#             )
#         elif data_mode == "csv":
#             test_cases = doc_du_lieu_dang_ky_csv(
#                 "data/input_regestered_case.csv"
#             )
#         elif data_mode == "json":
#             test_cases = doc_du_lieu_dang_ky_json(
#                 "data/input_regestered_case.json"
#             )
#         else:
#             raise ValueError(f"Data mode '{data_mode}' không hợp lệ")

#         metafunc.parametrize(
#             "tentaikhoan,email,matkhau,ketquamongdoi",
#             test_cases
#         )

# # ================== LOGGER ==================
# @pytest.fixture(scope="module")
# def logger(request):
#     os.makedirs("logs", exist_ok=True)
#     test_file = os.path.basename(request.node.fspath)
#     base_name = os.path.splitext(test_file)[0]
#     log_file = f"logs/{base_name}.log"

#     if os.path.exists(log_file):
#         os.remove(log_file)

#     logger = logging.getLogger(base_name)
#     logger.setLevel(logging.INFO)

#     if not logger.handlers:
#         fh = logging.FileHandler(log_file, encoding="utf-8")
#         ch = logging.StreamHandler()
#         fmt = logging.Formatter(
#             "%(asctime)s | %(levelname)s | %(message)s",
#             "%Y-%m-%d %H:%M:%S"
#         )
#         fh.setFormatter(fmt)
#         ch.setFormatter(fmt)
#         logger.addHandler(fh)
#         logger.addHandler(ch)

#     yield logger

# # ================== DRIVER ==================
# @pytest.fixture(scope="function")
# def cau_hinh():
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")

#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     yield {"driver": driver}
#     driver.quit()
import pytest
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from utils.data_utils import (
    doc_du_lieu_dang_nhap_excel,
    doc_du_lieu_dang_ky_excel,
    doc_du_lieu_muahang_excel,
    doc_du_lieu_thong_tin_excel,
    doc_du_lieu_tim_kiem_excel
)

# ================= OPTION =================
def pytest_addoption(parser):
    parser.addoption(
        "--data-mode",
        action="store",
        default="excel",
        help="excel | csv | json"
    )

# ================= DATA PARAMETRIZE =================
def pytest_generate_tests(metafunc):
    duong_dan_excel = "data/input_case.xlsx"
    data_mode = metafunc.config.getoption("--data-mode")

    # ===== ĐĂNG NHẬP =====
    if metafunc.function.__name__.startswith("test_dang_nhap") and \
       {"email", "matkhau", "ketquamongdoi"}.issubset(metafunc.fixturenames):
        test_cases = doc_du_lieu_dang_nhap_excel(
            duong_dan_excel, ten_sheet="Dangnhap"
        )
        metafunc.parametrize("email,matkhau,ketquamongdoi", test_cases)

    # ===== ĐĂNG KÝ =====
    if metafunc.function.__name__.startswith("test_dang_ky") and \
       {"tentaikhoan", "email", "matkhau", "ketquamongdoi"}.issubset(metafunc.fixturenames):
        test_cases = doc_du_lieu_dang_ky_excel(
            duong_dan_excel, ten_sheet="Dangky"
        )
        metafunc.parametrize("tentaikhoan,email,matkhau,ketquamongdoi", test_cases)

      # ===== THÔNG TIN TÀI KHOẢN =====
    elif metafunc.function.__name__.startswith("test_cap_nhat_thong_tin"):
        test_cases = doc_du_lieu_thong_tin_excel(
            duong_dan_excel, ten_sheet="Hsotkhoan"
        )
        metafunc.parametrize(
            "email,matkhau,ten,ho,tenhienthi,dcemail,matkhauhientai,matkhaumoi,nhaplaimk,ketquamongdoi",
            test_cases
        )

    # ===== TÌM KIẾM =====
    elif metafunc.function.__name__.startswith("test_tim_kiem"):
        test_cases = doc_du_lieu_tim_kiem_excel(
            duong_dan_excel, ten_sheet="Timkiem"
        )
        metafunc.parametrize(
            "tukhoa,ketquamongdoi",
            test_cases
        )
      # ===== MUA HÀNG =====
    elif metafunc.function.__name__.startswith("test_mua_ngay") and \
        {"tukhoa", "tensp", "ten", "diachi", "thanhpho", "sdt", "email", "ghichu", "ketquamongdoi"}.issubset(metafunc.fixturenames):

        test_cases = doc_du_lieu_muahang_excel(
            duong_dan_excel, ten_sheet="Muahang"
        )

        metafunc.parametrize(
            "tukhoa, tensp, ten, diachi, thanhpho, sdt, email, ghichu, ketquamongdoi",
            test_cases
        )



# ================= LOGGER =================
@pytest.fixture(scope="module")
def logger(request):
    os.makedirs("logs", exist_ok=True)
    test_file = os.path.basename(request.node.fspath)
    log_file = f"logs/{test_file.replace('.py', '')}.log"

    if os.path.exists(log_file):
        os.remove(log_file)

    logger = logging.getLogger(test_file)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        ch = logging.StreamHandler()
        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        fh.setFormatter(fmt)
        ch.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(ch)

    yield logger

# ================= DRIVER =================
@pytest.fixture(scope="function")
def cau_hinh():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield {"driver": driver}
    driver.quit()
