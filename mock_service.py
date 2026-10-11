# -*- coding: utf-8 -*-
# @File    : mock_service.py
# @Time    : 2026/10/11 09:43
# @Author  : chenxiaolin 
# @Email   : 742428767@qq.com
# @Software: PyCharm

import sqlite3
from itertools import count
from pathlib import Path

from flask import Flask,request,jsonify

import requests

#mock_service--本地写订单服务（Flask +SQLite）
BASE = Path(__file__).resolve().parent
DB_FILE = BASE / "orders.db"



app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.executescript("""
            CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, amount REAL, status TEXT, created_at TEXT);
        INSERT OR IGNORE INTO users(id, name) VALUES (1,'Alice'),(2,'Bob');
    
    """)
    conn.commit();conn.close()

@app.post("/orders")
def create():
    d = request.get_json() or {}
    #两类异常：字段缺失、类型错误
    if "user_id" not in d or "amount" not in d:
        return jsonify(error="user_id and amount are required"), 400
    if not isinstance(d["amount"],(int, float)):
        return jsonify(error="amount must be an number"), 400
    conn = sqlite3.connect(DB_FILE)
    cur = conn.execute("INSERT INTO orders(user_id, amount,status,created_at) VALUES (?,?,?,?)",
                       (d["user_id"],d["amount"],"created",d["created"]))
    conn.commit();oid = cur.lastrowid;conn.close()
    return jsonify(id=oid,**d,status="created"),201

@app.post("/orders/<int:oid>/cancel")

def cancel(oid):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("UPDATE orders SET status = 'cancelled' WHERE oid = ?",(oid,))
    conn.commit();conn.close()
    return jsonify(id=oid,status="cancelled")

@app.get("/users/<int:uid>/summary")
def summary(uid):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("SELECT COUNT(*) c, COALESCE(SUM(amount),0) t "
        "FROM orders WHERE user_id=? AND status<>'cancelled'",(uid,)).fetchone()
    conn.close()
    return jsonify(user_id=uid,count=row[0],total_amount=row[1])

if __name__ == "__main__":
    init_db()
    app.run(port=5000) #接口地址http://127.0.0.1:5000

