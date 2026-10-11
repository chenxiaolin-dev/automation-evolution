# -*- coding: utf-8 -*-
# @File    : test_day4.py
# @Time    : 2026/10/11 16:01
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm
def test_create_order_writes_to_db(api_Local_mock,db):
    payload = {"user_id":1,"amount":99.5,"created":"2026-10-11"}

    #1调接口创建订单，断言状态码201，把返回的新id取出来-------接口侧
    resp = api_Local_mock.post("/orders",json=payload)
    print(resp.url)
    assert resp.status_code == 201,f"创建失败：{resp.text}"
    new_id = resp.json()["id"]

    #2数据库侧：按新id查真正的那一行
    row = db.query_one("select user_id,amount,status from orders where id = ?",(new_id,))
    assert row is not None,f"接口返回201，但库里查不到订单 id={new_id}--数据没落库！"
    assert row["user_id"] == payload["user_id"]
    assert row["amount"] == payload["amount"]
    assert row["status"] == "created"
