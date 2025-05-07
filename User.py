import requests
import re
import csv

result=''                # 订单ID
order_id=''           # 订单号

headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

acount_data = [{'username':'wchwchwch1@qq.com'},
              {'username':'wchwchwch2@qq.com'},
              {'username':'wchwchwch3@qq.com'},
              {'username':'wchwchwch4@qq.com'},
               {'username':'wchwchwch5@qq.com'}
             ]

class UserAccount:
    def __init__(self):                    # 初始化方法，实例化session对象
        self.session = requests.Session()
    def get_verify_code(self):            # 获取验证码
        url = 'http://localhost/index.php/Home/User/verify/type/user_reg.html'
        r = self.session.get(url)
        assert r.status_code == 200, '验证码请求失败'
        print('获取验证码成功')


    def get_index(self):                    # 获取首页
        url = 'http://localhost/index.php'
        r = self.session.get(url)
        assert r.status_code == 200, '首页请求失败'
        print('首页请求成功')
        

    def register(self,username):                    # 注册
        url = 'http://localhost/Home/User/reg.html'
        
        data = {
            'auth_code': 'TPSHOP',
            'scene': '2',
            'username': username ,
            'verify_code': '8888',
            'password': '123456',
            'password2': '123456',
            'invite': ''
        }

        r = self.session.post(url, headers=headers,data=data)
        data_register = r.json()
        assert data_register['status'] == 1, data_register['msg']
        print(data_register['msg'])
        


class Shop:                                                    # 购物
    def __init__(self):
        self.session = requests.Session()


    def lg_verify_code(self):                               # 登录验证码                            
        url = 'http://localhost/index.php?m=Home&c=User&a=verify'
        r = self.session.get(url)
        assert r.status_code == 200, '验证码请求失败'
        print('获取验证码成功')

    def login(self,username):                                         # 登录                 
        url = 'http://localhost/index.php?m=Home&c=User&a=do_login&t=0.8035430559061323'
        
        data = {
                'username':username,
                'password':'123456',
                'verify_code':'8888',
        }
        r = self.session.post(url, headers=headers, data=data)
        data_login = r.json()
        assert data_login['status'] == 1, data_login['msg']
        print(data_login['msg'])


    def add_cart(self):                                    # 添加购物车                             
        url = 'http://localhost/index.php?m=Home&c=Cart&a=ajaxAddCart'
        
      
        data = {                                              #商品身份信息较为复杂且无法预知或预测，故只添加一件商品,不做参数化
            'goods_id': '65',
            'goods_prom_type': '0',
            'shop_price': '2799.00',
            'store_count': '100',
            'market_price': '2899.00',
            'start_time': '',
            'end_time': '',
            'activity_title': '',
            'prom_detail': '',
            'activity_is_on': '',
            'item_id': '122',
            'exchange_integral': '0',
            'point_rate': '1',
            'is_virtual': '0',
            'goods_spec[尺寸]': '65',
            'goods_num': '1',
            'goods_id': '65'

        }
        r = self.session.post(url, headers=headers, data=data)
        data_add = r.json()
        assert data_add['status'] == 1, data_add['msg']
        print(data_add['msg'])
        

    def get_cart(self,username):                                    # 提交购物车                         
        url = 'http://localhost/Home/Cart/cart3.html'
        
        data = {
            'address_id': '829',
            'invoice_desc': '不开发票',
            'couponTypeSelect': '1',
            'coupon_id': '0',
            'shipping_code': 'shentong',
            'user_note':username,
            'paypwd':'123456',
            'act':'submit_order',
        }
        r = self.session.post(url, headers=headers, data=data)
        data_cart = r.json()
        assert data_cart['status'] == 1, data_cart['msg']
        print(data_cart['msg'],'订单id为:',data_cart['result'],'请及时付款')
        global result
        result = data_cart['result']

    def get_order_id(self):                                # 接口文档混乱，无法通过时间戳获取订单号，经检验可以用订单ID获取订单详情页的订单号
        url = f'http://localhost/index.php/Home/Order/order_detail/id/{result}.html'
        r = self.session.get(url)
        match_result = re.search(r'<a class="ddn3" style="margin-top:20px;" href="/index.php/Home/Cart/cart4/order_id/(.*?).html">立即付款</a>', r.text)
        assert match_result.group(1) == result, '订单号获取失败'
        pattern = r'<p class="ddn1"><span>订单号：<\/span><span>(\d+)<\/span><\/p>'
        match = re.search(pattern, r.text)
        global order_id
        order_id = match.group(1)
        print('订单号为:',order_id)

    def pay_type(self):                                    # 支付方式
        url = 'http://localhost/index.php/Home/Payment/getCode.html'
        data ={
            'pay_radio':'pay_code=cod',
            'order_id':result,
            'master_order_sn':''
        }
        r = self.session.post(url,data=data)
        pattern = r'<title>(.*?)(</title>)'
        match = re.search(pattern, r.text)
        status = match.group(1)
        assert '支付' in status, '支付失败'
        print('已选择支付')

    def pay_status(self):                                   # 支付状态
        url = f'http://localhost/index.php/home/Payment/returnUrl/pay_code/cod/order_sn/{order_id}.html'   #至此为止，接口中order_id概念定义不明确
        r = self.session.get(url)
        pattern = r'<h3>(.*?)<\/h3>'
        match = re.search(pattern, r.text)
        status = match.group(1)
        assert '订单提交成功' in status, '支付失败'
        print('支付成功')


#先执行完管理员发货的方法再执行以下方法，否则会出错
    def order_confirm(self):                                # 确认收货
        url = 'http://localhost/index.php?m=Home&c=Order&a=order_confirm'
        data = {
            'order_id': result,
            }
        r = self.session.post(url, data=data)
        data_order_confirm = r.json()
        assert data_order_confirm['status'] == 1, data_order_confirm['msg']
        print('确认收货',data_order_confirm['msg'])



    
    def add_comment(self):
        url = 'http://localhost/index.php/Home/Order/add_comment.html'
        data = {
            'order_id': result,
            'goods_id': '65',
            'order_prom_type': '0',
            'score': '5',
            'goods_rank': '5',
            'score': '5',
            'service_rank': '5',
            'score': '5',
            'deliver_rank': '5',
            'content': '6666666666'
        }
        r = self.session.post(url, data=data)
        data_comment = r.json()
        assert data_comment['status'] == 1, data_comment['msg']
        print(data_comment['msg'])



