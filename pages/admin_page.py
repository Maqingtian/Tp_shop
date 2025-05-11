import requests
import re
from utils.config import BASE_URL, HEADERS

class AdminPage:
    delivery_data = ''

    def __init__(self):
        self.session = requests.Session()

    def admin_index(self):
        url = f'{BASE_URL}/index.php/Admin/Admin/login'
        self.session.get(url)

    def admin_verify_code(self):
        url = f'{BASE_URL}/admin/Admin/vertify'
        r = self.session.get(url)
        assert r.status_code == 200, '验证码请求失败'
        print('获取验证码成功')

    def admin_login(self):
        url = f'{BASE_URL}/index.php?m=Admin&c=Admin&a=login&t=0.8090519999028916'
        data = {
            'username': 'admin',
            'password': '123456',
            'verify_code': '8888'
        }
        r = self.session.post(url, headers=HEADERS, data=data)
        data_login = r.json()
        assert data_login['status'] == 1, data_login['msg']
        print('登录成功')

    def confirm_order(self, result):
        url = f'{BASE_URL}/index.php/Admin/order/order_action/order_id/{result}/type/confirm'
        r = self.session.post(url)
        data_confirm = r.json()
        assert data_confirm['status'] == 1, data_confirm['msg']
        print('确认订单', data_confirm['msg'])

    def admin_pay(self, result):
        url = f'{BASE_URL}/index.php/Admin/order/order_action/order_id/{result}/type/pay'
        r = self.session.post(url)
        data_pay = r.json()
        assert data_pay['status'] == 1, data_pay['msg']
        print('后台付款', data_pay['msg'])

    def delivery(self, result):
        url = f'{BASE_URL}/index.php/admin/Order/delivery_info/order_id/{result}'
        r = self.session.get(url)
        pattern = r'<input type="checkbox" name="goods\[\]" value="(\d+)" checked="checked">'
        match = re.search(pattern, r.text)
        self.delivery_data = match.group(1)
        print('发货商品:', self.delivery_data)

    def confirm_delivery(self, result):
        url = f'{BASE_URL}/index.php/Admin/order/deliveryHandle'
        data = {
            'shipping': '0',
            'shipping_name': '顺丰快递',
            'shipping_code': 'shunfeng',
            'invoice_no': '123456213',
            'goods[]': self.delivery_data,
            'order_id': result,
        }
        self.session.post(url, data=data)


