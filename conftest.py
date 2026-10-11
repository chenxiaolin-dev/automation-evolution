# -*- coding: utf-8 -*-
# @File    : config.py
# @Time    : 2026/10/9 10:04
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm
import pytest

import requests

from api.client import ApiClient

from db import DB

@pytest.fixture(scope="session")
def config():
    #session  全局作用域
    return {
        "base_url": "https://jsonplaceholder.typicode.com",
        "timeout":10,
    }

@pytest.fixture(scope="function")
def http_session():
    #function作用域
    s=requests.Session()

    s.headers.update({"User-Agent": "day2-pytest-practice"})
    yield s
    s.close()

@pytest.fixture(scope="session")
def api_client():
    #session 级：整个运行过程一个客户端，域名只配置一次
    client = ApiClient("https://jsonplaceholder.typicode.com", timeout=10)
    yield client
    client.close()

@pytest.fixture(scope="session")
def api_Local_mock():
    #session 级：整个运行过程一个客户端，域名只配置一次
    Local_mock = ApiClient("http://127.0.0.1:5000", timeout=10)
    yield Local_mock
    Local_mock.close()

@pytest.fixture(scope="session")
def db():
    #整个测试过程一个连接：连库是有开销的，不该每天用例都连
    conn = DB()
    yield conn  #yield 之后是teardown
    conn.close()