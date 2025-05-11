import requests
import re
from utils.config import BASE_URL, HEADERS

class UserPage:
    def __init__(self):
        self.session = requests.Session()

    def get_verify_code(self):
        url = f'{BASE_URL}/index.php/Home/User/verify/type/user_reg.html'
        r = self.session.get(url)
        assert r.status_code == 200, '验证码请求失败'
        print('获取验证码成功')

    def get_index(self):
        url = f'{BASE_URL}/index.php'
        r = self.session.get(url)
        assert r.status_code == 200, '首页请求失败'
        print('首页请求成功')

    def register(self, username):
        url = f'{BASE_URL}/Home/User/reg.html'
        data = {
            'auth_code': 'TPSHOP',
            'scene': '2',
            'username': username,
            'verify_code': '8888',
            'password': '123456',
            'password2': '123456',
            'invite': ''
        }
        r = self.session.post(url, headers=HEADERS, data=data)
        data_register = r.json()
        assert data_register['status'] == 1, data_register['msg']
        print(data_register['msg'])