import requests

class RequestUtils:
    def __init__(self, session):
        self.session = session
        self.session.verify = False

    def send_request(self, method, url, data=None, headers=None):
        try:
            if method == 'get':
                response = self.session.get(url, headers=headers)
            elif method == 'post':
                response = self.session.post(url, headers=headers, data=data)
            else:
                raise ValueError(f"不支持的请求方法: {method}")
            
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            raise