# -*- coding: utf-8 -*-
"""Day 1 练习 · 调 3 个公开 API
================================================
跑法（二选一）:
  1) PyCharm 打开 D:\\PyCharm\\day1_api_practice 文件夹,
     右下角解释器选 D:\\PyCharm\\automation-framework\\.venv\\Scripts\\python.exe,
     然后右键编辑器 → Run 'day1_apis'
  2) 或在 PyCharm 底部 Terminal 里执行:
     D:/PyCharm/automation-framework/.venv/Scripts/python.exe day1_apis.py

今天的验收标准（对照 30 天计划 Day 1）:
  ① 终端跑通不报错
  ② 能解释代码里每一个 requests.get 参数的作用
  ③ 跑通后 push 成功（这个文件夹可以以后并进你的仓库）
"""
import requests
import pytest


# ================================================================
# 先搞懂 requests.get 的四个最常用参数 —— 面试必问
# ================================================================
# requests.get(
#     url,      # 必填:接口地址
#     params=…, # 可选:查询参数,自动拼到 url 后面变成 ?key=value
#     headers=…,# 可选:请求头,比如伪装 User-Agent、带 token
#     timeout=…,# 可选:超时秒数,超过就抛异常。生产代码必带,防止用例卡死
# )
#
# 返回的 resp 常用属性:
#   resp.status_code  状态码(200成功 / 404不存在 / 500服务端错)
#   resp.json()       把响应体解析成 dict(接口测试 90% 用这个)
#   resp.text         响应体原文(字符串)
#   resp.elapsed      请求耗时(性能排查时用)
# ================================================================


def api_1_jsonplaceholder():
    """接口 1:JSONPlaceholder —— 专门给开发者练手的假数据接口,免注册、免 key"""
    print("\n>>> 接口 1:JSONPlaceholder /posts/1(取一篇帖子)")

    resp = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1",
        timeout=10,
    )

    print("状态码:", resp.status_code)
    data = resp.json()          # 把 JSON 响应解析成 Python 字典
    print("返回字段:", list(data.keys()))   # 看看有哪些字段
    print("标题:", data["title"])

    # ---- 断言:预期不对就报 AssertionError,用例就算失败 ----
    assert resp.status_code == 200, f"预期 200,实际 {resp.status_code}"
    assert data["id"] == 1, f"预期 id=1,实际 {data['id']}"
    assert "title" in data, "返回里必须有 title 字段"
    print("✅ 3 条断言全部通过")


def api_2_httpbin():
    """接口 2:httpbin —— 它会把你发的参数原样返回来,最适合看懂 params"""
    print("\n>>> 接口 2:httpbin /get(演示 params 参数)")

    resp = requests.get(
        "https://httpbin.org/get",
        params={"source": "day1", "owner": "xiaolin"},  # 自动拼成 ?source=day1&owner=xiaolin
        headers={"User-Agent": "day1-practice"},        # 告诉服务器我是谁
        timeout=10,
    )

    print("实际请求 URL:", resp.url)      # 看,params 被拼进 URL 了
    data = resp.json()
    print("服务端收到的 headers.User-Agent:", data["headers"]["User-Agent"])

    assert resp.status_code == 200
    # httpbin 会把你发的参数回显回来 —— 这就是"参数传递"的最直观证明
    assert data["args"]["source"] == "day1", "服务端应该收到 source=day1"
    assert data["headers"]["User-Agent"] == "day1-practice"
    print("✅ 断言通过:params 和 headers 都按预期送达")


def api_3_dogceo():
    """接口 3:Dog CEO —— 练'字段结构不确定'时怎么断言(只断结构不断值)"""
    print("\n>>> 接口 3:dog.ceo 随机狗图(练'值会变'的断言写法)")

    resp = requests.get("https://dog.ceo/api/breeds/image/random", timeout=10)
    data = resp.json()

    print("状态码:", resp.status_code, "| status:", data["status"])
    print("图片地址:", data["message"])

    assert resp.status_code == 200
    assert data["status"] == "success"
    # 每次返回的图片地址都不一样 —— 所以不能断言具体值,只能断言"规律"
    assert data["message"].startswith("https://"), "message 应该是个图片 URL"
    print("✅ 断言通过(断言的是规律,不是写死的值)")


if __name__ == "__main__":
    api_1_jsonplaceholder()
    api_2_httpbin()
    api_3_dogceo()
    print("\n" + "=" * 50)
    print("🎉 Day 1 任务完成:3 个 API 全部调通、断言全过")
    print("下一步:把每行注释盖住,看代码自己说一遍作用 —— 说不出的那行,明天再讲一遍")
