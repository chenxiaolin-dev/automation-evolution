# -*- coding: utf-8 -*-
# @File    : db.py
# @Time    : 2026/10/11 15:32
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm

#测试侧的数据库工具，连一次查多次
import _sqlite3
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent

class DB:
    def __init__(self,path=None):
        self.path = path
        self.conn = sqlite3.connect(path or (BASE / "orders.db"))
        self.conn.row_factory = sqlite3.Row #关键：结果能按‘字段名’去，而不是下标


    def query_one(self,sql,args=()):
        row = self.conn.execute(sql,args).fetchone()
        return dict(row) if row else None  #查不到--》None（用来断言“没落库”）

    def query_all(self,sql,args=()):

        return [dict(r)  for r in (self.conn.execute(sql,args).fetchall()) ]

    def close(self):
        self.conn.close()

