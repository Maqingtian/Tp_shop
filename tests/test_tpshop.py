import pytest
from pages.user_page import UserPage
from pages.admin_page import AdminPage
from pages.shop_page import ShopPage
from utils.config import ACCOUNT_DATA
import allure

@allure.epic("TP Shop电商系统")
@allure.feature("完整订单流程测试")
class TestShop:

    @allure.story("用户下单流程")
    @allure.title("测试用户下单支付流程")
    @pytest.mark.run(order=1)
    def test_user_operations_before_receipt(self, setup_shop_page):
        self.shop_page = setup_shop_page
        self.shop_page.lg_verify_code()
        self.shop_page.login('maqingtian1@qq.com')
        self.shop_page.add_cart()
        self.shop_page.get_cart('maqingtian1@qq.com')
        self.shop_page.get_order_id()
        self.shop_page.pay_type()
        self.shop_page.pay_status()

    @allure.story("后台订单处理")
    @allure.title("测试后台订单处理流程")
    @pytest.mark.run(order=2)
    def test_admin_operations(self, setup_shop_page, setup_admin_page):
        self.shop_page = setup_shop_page
        self.admin_page = setup_admin_page
        self.admin_page.admin_index()
        self.admin_page.admin_verify_code()
        self.admin_page.admin_login()
        self.admin_page.confirm_order(self.shop_page.result)
        self.admin_page.admin_pay(self.shop_page.result)
        self.admin_page.delivery(self.shop_page.result)
        self.admin_page.confirm_delivery(self.shop_page.result)

    @allure.story("用户确认收货")
    @allure.title("测试用户确认收货流程")
    @pytest.mark.run(order=3)
    def test_user_operations_after_receipt(self, setup_shop_page):
        self.shop_page = setup_shop_page
        self.shop_page.lg_verify_code()
        self.shop_page.login('maqingtian1@qq.com')
        self.shop_page.order_confirm()
        self.shop_page.add_comment()