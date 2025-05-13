import requests
import re
from utils.config import BASE_URL, HEADERS
from utils.request_utils import RequestUtils

class ShopPage:
    def __init__(self):
        self.session = requests.Session()
        self.request_utils = RequestUtils(self.session)
        self.result = ''
        self.order_id = ''

    def lg_verify_code(self):
        url = f'{BASE_URL}/index.php?m=Home&c=User&a=verify'
        response = self.request_utils.send_request('get', url)
        assert response.status_code == 200, '验证码请求失败'
        print('获取验证码成功')

    def login(self, username, password='123456', verify_code='8888'):
        url = f'{BASE_URL}/index.php?m=Home&c=User&a=do_login'
        data = {
            'username': username,
            'password': password,
            'verify_code': verify_code,
        }
        r = self.session.post(url, headers=HEADERS, data=data)
        data_login = r.json()
        assert data_login['status'] == 1, data_login['msg']
        print(data_login['msg'])

    def add_cart(self, goods_id, goods_spec, goods_num, goods_prom_type='0', shop_price='2799.00', store_count='100', market_price='2899.00', item_id='220'):
        url = f'{BASE_URL}/index.php?m=Home&c=Cart&a=ajaxAddCart'
        data = {
            'goods_id': goods_id,
            'goods_spec[尺寸]': goods_spec,
            'goods_num': goods_num,
            'goods_prom_type': goods_prom_type,
            'shop_price': shop_price,
            'store_count': store_count,
            'market_price': market_price,
            'item_id': item_id
        }
        r = self.session.post(url, headers=HEADERS, data=data)
        data_add = r.json()
        assert data_add['status'] == 1, data_add['msg']
        print(data_add['msg'])

    def get_cart(self, username):
        url = f'{BASE_URL}/Home/Cart/cart3.html'
        data = {
            'address_id': '829',
            'invoice_desc': '不开发票',
            'couponTypeSelect': '1',
            'coupon_id': '0',
            'shipping_code': 'shentong',
            'user_note': username,
            'paypwd': '123456',
            'act': 'submit_order',
        }
        r = self.session.post(url, headers=HEADERS, data=data)
        data_cart = r.json()
        assert data_cart['status'] == 1, data_cart['msg']
        print(data_cart['msg'], '订单id为:', data_cart['result'], '请及时付款')
        self.result = data_cart['result']
        # 新增获取真实订单号
        # self.get_order_id()  # 调用已有方法获取订单号
        # return self.result

    def get_order_id(self):
        url = f'{BASE_URL}/index.php/Home/Order/order_detail/id/{self.result}.html'
        r = self.session.get(url)
        match_result = re.search(r'<a class="ddn3" style="margin-top:20px;" href="/index.php/Home/Cart/cart4/order_id/(.*?).html">立即付款</a>', r.text)
        assert match_result.group(1) == str(self.result), '订单号获取失败'
        pattern = r'<p class="ddn1"><span>订单号：<\/span><span>(\d+)<\/span><\/p>'
        match = re.search(pattern, r.text)
        self.order_id = match.group(1)
        print('订单号为:', self.order_id)

    def pay_type(self):
        url = f'{BASE_URL}/index.php/Home/Payment/getCode.html'
        data = {
            'pay_radio': 'pay_code=cod',
            'order_id': self.result,
            'master_order_sn': ''
        }
        r = self.session.post(url, data=data)
        pattern = r'<title>(.*?)(</title>)'
        match = re.search(pattern, r.text)
        status = match.group(1)
        assert '支付' in status, '支付失败'
        print('已选择支付')

    def pay_status(self):
        url = f'{BASE_URL}/index.php/home/Payment/returnUrl/pay_code/cod/order_sn/{self.order_id}.html'
        r = self.session.get(url)
        pattern = r'<h3>(.*?)<\/h3>'
        match = re.search(pattern, r.text)
        status = match.group(1)
        assert '订单提交成功' in status, '支付失败'
        print('支付成功')

    def order_confirm(self):
        url = f'{BASE_URL}/index.php?m=Home&c=Order&a=order_confirm'
        data = {
            'order_id': self.result,
        }
        r = self.session.post(url, data=data)
        data_order_confirm = r.json()
        assert data_order_confirm['status'] == 1, data_order_confirm['msg']
        print('确认收货', data_order_confirm['msg'])

    def add_comment(self, goods_id='65', score='5', content='6666666666'):
        url = f'{BASE_URL}/index.php/Home/Order/add_comment.html'
        data = {
            'order_id': self.result,
            'goods_id': goods_id,
            'order_prom_type': '0',
            'score': score,
            'goods_rank': '5',
            'service_rank': '5',
            'deliver_rank': '5',
            'content': content
        }
        r = self.session.post(url, data=data)
        data_comment = r.json()
        assert data_comment['status'] == 1, data_comment['msg']
        print(data_comment['msg'])