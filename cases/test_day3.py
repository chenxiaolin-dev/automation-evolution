
# -*- coding: utf-8 -*-
# @File    : test_day3.py
# @Time    : 2026/10/10 10:26
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm
from pathlib import Path

import pytest

import yaml


DATA_FILE = Path(__file__).parent.parent / "data"/"posts_cases.yaml"


def load_cases():
    with open(DATA_FILE,encoding="utf-8") as f:
        return yaml.safe_load(f)["cases"]

#数据从YAML来；ids=让报告显示case_id,而不是一串dict
@pytest.mark.parametrize("case", load_cases(),ids=lambda c:c["case_id"])
def test_get_posts(api_client,case):
    #1取数：case字典里拿参数 2.调用：api层封装好的方法
    resp = api_client.get(f"/posts/{case['post_id']}")

    #3断言：预期状态码默认200，反向用例在YAML里写404覆盖
    expected = case.get("expected_status",200)
    assert resp.status_code == expected,\
        f"{case['case_id']}预期{expected},实际{resp.status_code}"

    if expected==200:
        assert resp.json()["id"] == case["post_id"]