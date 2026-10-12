# -*- coding: utf-8 -*-
# @File    : test_day5.py
# @Time    : 2026/10/12 14:49
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm
import allure



#TODO1:最外层是【大模块】（业务板块），用三层里最粗的那个注解
#      三层从小到大是：epic（业务模块）>feature（模块）>story(功能点）
@allure.epic("订单")
#TODO2:往里一层是【具体功能】，用中间那层
@allure.feature("创建订单")
class TestOrderReport:

    #TODO3:这行决定报告里显示 的标题-不用函数名
    @allure.title("接口创建订单后，数据应真的落库")
    #TODO4:核心业务的严重级别，五档：BLOCKER / CRITICAL / NORMAL / MINOR / TRIVIAL
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_writes_to_db(self,api_Local_mock,db):
        payload = {"user_id":1,"amount":99.5,"created":"2026-10-12"}

        #TODO5:让下面这一组操作，在报告里显示成【一个步骤】
        with allure.step("调接口创建订单"):
            resp= api_Local_mock.post("/orders",json=payload)
            assert resp.status_code == 201,f"创建失败：{resp.text}"
            new_id = resp.json()["id"]

        with allure.step("查库确认真的落库"):
            row = db.query_one(
                "select user_id,amount,status  from orders where id = ?",(new_id,) )
            assert row is not None,f"接口返回201单库里查不到id={new_id}"
            assert row["user_id"] == payload["user_id"]
            assert row["amount"] == payload["amount"]
            assert row["status"] == "created"


@allure.feature("创建订单")
def test_create_order_keeps_evidence(api_Local_mock, db):
    payload = {"user_id": 1, "amount": 88.0, "created": "2026-10-12"}
    resp = api_Local_mock.post("/orders", json=payload)
    new_id = resp.json()["id"]
    row = db.query_one("select * from orders where id = ?",(new_id,) )
    assert row["status"] == "created"

    # TODO 1 → allure.attach(...) + attachment_type.TEXT
    allure.attach(resp.text, name="接口返回体",
                  attachment_type=allure.attachment_type.TEXT)

    # TODO 2 → 同样用 attach，TEXT 就够（JSON 也行，看你想不想高亮）
    allure.attach(str(row), name="数据库里最新一行",
                  attachment_type=allure.attachment_type.TEXT)

    # ── 另外两种常见附件（今天不写，先知道有）──
    # 图片：allure.attach.file("screenshots/err.png", name="失败截图",
    #                          attachment_type=allure.attachment_type.PNG)
    # JSON：attachment_type=allure.attachment_type.JSON