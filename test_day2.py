# -*- coding: utf-8 -*-
# @File    : test_day2.py
# @Time    : 2026/10/9 10:42
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm
from asyncio import timeout

#参数化五条用例+2个fixture
import pytest
import requests


@pytest.mark.parametrize("post_id",[1,2,3,10,100])
def test_get_post(config,http_session,post_id):
    #config,http_session,conftest.py里的fixture,没import也能用
    resp = http_session.get(f"{config['base_url']}/posts/{post_id}",
                            timeout=config["timeout"])
    assert resp.status_code == 200,f"post{post_id}预期 200，实际{resp.status_code}"
    assert resp.json()["id"] == post_id

#多参数参数化：用户名断言
@pytest.mark.parametrize("user_id,expected_name",[(1,"Leanne Graham"),(2,"Ervin Howell"),
])
def test_user_name(config,http_session,user_id,expected_name):
    resp = http_session.get(f"{config['base_url']}/users/{user_id}",
                            timeout=config["timeout"])
    assert resp.status_code == 200
    assert resp.json()["name"] == expected_name

#一条普通用例，证明function fixture 每条用例都新建
def test_session_header(http_session):
    #conftest里设置的User-Agent应该在会话的默认值请求头里
    assert http_session.headers["User-Agent"] == "day2-pytest-practice"

print(111)