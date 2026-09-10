#获取data\transportNetwork.db所有表名，列名，列数据类型
import sqlite3
import os

# 1. 设置数据库路径并连接
db_path = os.path.join("data", "transportNetwork.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 2. 获取所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()

    # 3. 遍历每个表，获取列信息
    for table in tables:
        table_name = table[0]
        print(f"\n📊 表名: {table_name}")
        print("-" * 40)
        
        # 使用 PRAGMA 获取表结构信息
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        # 打印列名和数据类型
        for col in columns:
            # col[1] 是列名, col[2] 是数据类型
            print(f"  - 列名: {col[1]:<20} | 数据类型: {col[2]}")

except Exception as e:
    print(f"发生错误: {e}")

finally:
    # 4. 关闭连接
    cursor.close()
    conn.close()