# -*- coding: utf-8 -*-
# @File    : config.py
# @Time    : 2026/10/9 10:04
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm
import pytest

import requests

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