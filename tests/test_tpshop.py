import pytest
from pages.user_page import UserPage
from pages.admin_page import AdminPage
from pages.shop_page import ShopPage
from utils.config import ACCOUNT_DATA

class TestShop:
    # 移除 setup_method 方法，因为要使用 fixture
    # def setup_method(self):
    #     self.user_page = UserPage()
    #     self.admin_page = AdminPage()
    #     self.shop_page = ShopPage()

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

    # @pytest.mark.run(order=2)
    # def test_qwer(self, setup_shop_page):
    #     self.shop_page = setup_shop_page
    #     print("开始执行 test_qwer 方法")
    #     if hasattr(self.shop_page, 'result'):
    #         print(f"self.shop_page.result 的值为: {self.shop_page.result}")
    #     else:
    #         print("self.shop_page 没有 result 属性")
    #     print("结束执行 test_qwer 方法")
        
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

    @pytest.mark.run(order=3)
    def test_user_operations_after_receipt(self, setup_shop_page):
        self.shop_page = setup_shop_page
        self.shop_page.lg_verify_code()
        self.shop_page.login('maqingtian1@qq.com')
        self.shop_page.order_confirm()
        self.shop_page.add_comment()