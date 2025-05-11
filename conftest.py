import pytest
from pages.user_page import UserPage
from pages.admin_page import AdminPage
from pages.shop_page import ShopPage

# 定义 fixture，作用域为 class
@pytest.fixture(scope="class")
def setup_shop_page():
    shop_page = ShopPage()
    yield shop_page

@pytest.fixture(scope="class")
def setup_user_page():
    user_page = UserPage()
    yield user_page

@pytest.fixture(scope="class")
def setup_admin_page():
    admin_page = AdminPage()
    yield admin_page