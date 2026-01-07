import pytest
from pathlib import Path
from utils.logger import get_logger
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

@pytest.fixture
def logger(request):
    test_file_name = Path(request.node.fspath).stem
    return get_logger(test_file_name)


# ================= DRIVER =================
@pytest.fixture(scope="function")
def cau_hinh():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield {"driver": driver}
    driver.quit()
