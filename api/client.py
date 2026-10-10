# -*- coding: utf-8 -*-
# @File    : client.py
# @Time    : 2026/10/10 10:00
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm



#api/client.py  ---怎么发请求 ，只写一次
import requests


class ApiClient:
    #所有接口共用的“客户端”：域名和超时在这里定死
    def __init__(self, base_url,timeout=10):
        self.base_url = base_url.rstrip("/")  #防止域名结尾多一个斜杠
        self.timeout = timeout
        self.session = requests.Session()  #复用连接+共享header

    def get(self,path,**kwargs):
        #用例只写/post/1，不用关心域名和超时
        kwargs.setdefault("timeout",self.timeout)
        return self.session.get(f"{self.base_url}{path}",**kwargs)

    def post(self,path,**kwargs):
        kwargs.setdefault("timeout",self.timeout)
        return self.session.post(f"{self.base_url}{path}",**kwargs)

    def close(self):
        self.session.close()
