import requests
import re

# headers = {
#             'Content-Type': 'application/x-www-form-urlencoded'
#         }

class Admin:
    delivery_data=''          # 初始化一个变量，用于存储发货商品的种类
    def __init__(self):
        self.session = requests.Session()
    def admin_index(self):
        url = 'http://localhost/index.php/Admin/Admin/login'
        r = self.session.get(url)
    def admin_verify_code(self):
        url = 'http://localhost/admin/Admin/vertify'
        r = self.session.get(url)
        assert r.status_code == 200, '验证码请求失败'
        print('获取验证码成功')


    def admin_login(self):
        url = 'http://localhost/index.php?m=Admin&c=Admin&a=login&t=0.8090519999028916'
        data = {
            'username':'admin',
            'password':'123456',
            'verify_code':'8888'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = self.session.post(url, headers=headers, data=data)
        data_login = r.json()
        assert data_login['status'] == 1, data_login['msg']
        print('登录成功')

    
    def confirm_order(self,result):
        url = f'http://localhost/index.php/Admin/order/order_action/order_id/{result}/type/confirm' #原先写的是confirm
        r = self.session.post(url)
        data_confirm = r.json()
        assert data_confirm['status'] == 1, data_confirm['msg']
        print('确认订单',data_confirm['msg'])

    def admin_pay(self,result):
        url = f'http://localhost/index.php/Admin/order/order_action/order_id/{result}/type/pay'    
        r = self.session.post(url)
        data_pay = r.json()
        assert data_pay['status'] == 1, data_pay['msg']
        print('后台付款',data_pay['msg'])

    def delivery(self,result):
        url = f'http://localhost/index.php/admin/Order/delivery_info/order_id/{result}'
        r = self.session.get(url)
        # <input type="checkbox" name="goods[]" value="1832" checked="checked">
        pattern = r'<input type="checkbox" name="goods\[\]" value="(\d+)" checked="checked">'
        match = re.search(pattern, r.text)
        Admin.delivery_data = match.group(1)
        print('发货商品:',Admin.delivery_data)
        

    def confirm_delivery(self,result):
        url = 'http://localhost/index.php/Admin/order/deliveryHandle'    # 确认发货      经检验，该请求可以成功发货，但是会返回一个错误接口
        data= {
            'shipping':'0',
            'shipping_name':'顺丰快递',
            'shipping_code':'shunfeng',
            'invoice_no':'123456213',
            'goods[]':Admin.delivery_data,
            'order_id':result,
        }
        r = self.session.post(url, data=data)       #未找到断言方法




        
