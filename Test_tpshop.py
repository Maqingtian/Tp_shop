import requests
import Admin
import User
import unittest
import ddt

@ddt.ddt
class TestShop(unittest.TestCase):
    counter = 0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 调用父类的构造函数
        self.admin = Admin.Admin()
        self.user = User.UserAccount()
        self.shop = User.Shop()
    def setUp(self):
        TestShop.counter += 1
        if TestShop.counter == 1:
            print('注册测试开始')
        if TestShop.counter == 2:
            print('用户操作测试1开始')
        if TestShop.counter == 3:
            print('管理员操作测试开始')
        if TestShop.counter == 4:
            print('用户操作测试2开始')

    def tearDown(self):
        if TestShop.counter == 1:
            print('注册测试结束')
        if TestShop.counter == 2:
            print('用户操作测试1结束')
        if TestShop.counter == 3:
            print('管理员操作测试结束')
        if TestShop.counter == 4:
            print('用户操作测试2结束')

    @ddt.data(*User.acount_data)
    @ddt.unpack    
    def test_1(self,username):
        self.user.get_verify_code()
        self.user.get_index()
        self.user.register(username)

    def test_2(self):          #用户操作，收货前
        self.shop.lg_verify_code()
        self.shop.login('maqingtian1@qq.com')
        self.shop.add_cart()
        self.shop.get_cart('maqingtian1@qq.com')
        self.shop.get_order_id()
        self.shop.pay_type()
        self.shop.pay_status()

    def test_3(self):          #管理员操作
        self.admin.admin_index()
        self.admin.admin_verify_code()
        self.admin.admin_login()
        self.admin.confirm_order(User.result)
        self.admin.admin_pay(User.result)
        self.admin.delivery(User.result)
        self.admin.confirm_delivery(User.result)


    def test_4(self):          #用户操作，收货
        self.shop.lg_verify_code()
        self.shop.login('maqingtian1@qq.com')
        self.shop.order_confirm()
        self.shop.add_comment()


# if __name__ == '__main__':
#     unittest.main()

