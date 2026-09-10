# -*- coding: utf-8 -*-
"""
数据库管理模块
封装 SQLite 数据库连接与查询，提供 OBD / OLT 数据访问接口。
"""
import os
import sqlite3

import pandas as pd


class DatabaseManager:
    """transportNetwork 数据库管理器。"""

    # DEFAULT_DB_PATH = os.path.join(
    #     os.path.dirname(os.path.abspath(__file__)),
    #     'transportNetwork.db'
    # )
    DEFAULT_DB_PATH = 'data/transportNetwork.db'
    OBD_TABLE = 'OBD箱体'
    OLT_TABLE = 'OLT网元数据集'

    def __init__(self, db_path: str = None):
        self.db_path = db_path or self.DEFAULT_DB_PATH
        self._conn = None

    # ------------------------------------------------------------------
    # 连接管理
    # ------------------------------------------------------------------
    def connect(self) -> bool:
        """连接数据库，返回是否成功。"""
        try:
            if not os.path.exists(self.db_path):
                raise FileNotFoundError(f'数据库文件不存在: {self.db_path}')
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
            return True
        except Exception as e:
            self._conn = None
            print(f'[ERROR] 数据库连接失败: {e}')
            return False

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    @property
    def is_connected(self) -> bool:
        return self._conn is not None

    # ------------------------------------------------------------------
    # 校验
    # ------------------------------------------------------------------
    def check_tables_exist(self) -> dict:
        """检查业务表是否存在。返回 {表名: bool}。"""
        result = {self.OBD_TABLE: False, self.OLT_TABLE: False}
        if not self.is_connected:
            return result
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = {row[0] for row in cursor.fetchall()}
        result[self.OBD_TABLE] = self.OBD_TABLE in tables
        result[self.OLT_TABLE] = self.OLT_TABLE in tables
        return result

    def get_table_row_count(self, table_name: str) -> int:
        if not self.is_connected:
            return 0
        cursor = self._conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        return cursor.fetchone()[0]

    # ------------------------------------------------------------------
    # 数据查询
    # ------------------------------------------------------------------
    def get_obd_data(self) -> pd.DataFrame:
        """获取 OBD 箱体表全部数据。"""
        if not self.is_connected:
            return pd.DataFrame()
        query = f'SELECT * FROM "{self.OBD_TABLE}"'
        return pd.read_sql_query(query, self._conn)

    def get_olt_data(self) -> pd.DataFrame:
        """获取 OLT 端口资源表全部数据。"""
        if not self.is_connected:
            return pd.DataFrame()
        query = f'SELECT * FROM "{self.OLT_TABLE}"'
        return pd.read_sql_query(query, self._conn)

    # ------------------------------------------------------------------
    # 数据导入 - 用 DataFrame 替换指定表
    # ------------------------------------------------------------------
    def import_table_from_dataframe(self, df: pd.DataFrame,
                                     table_name: str,
                                     if_exists: str = 'replace') -> int:
        """将 DataFrame 写入指定表（默认先删后建）。

        Args:
            df: 待导入的 DataFrame（列名应与表字段匹配）
            table_name: 目标表名（obd_box 或 OLT网元数据集）
            if_exists: pandas to_sql 模式 {'replace', 'append', 'fail'}

        Returns:
            导入行数
        """
        if df is None or df.empty:
            raise ValueError('DataFrame 为空，无法导入')
        # 若未连接，尝试自动连接
        if not self.is_connected:
            if not self.connect():
                raise RuntimeError('数据库未连接')
        # 用 pandas to_sql 写入，自动按列推断 SQLite 类型
        df.to_sql(table_name, self._conn, if_exists=if_exists, index=False)
        self._conn.commit()
        return len(df)

    def get_obd_by_site(self, site: str) -> pd.DataFrame:
        """按所属站点筛选 OBD。"""
        if not self.is_connected:
            return pd.DataFrame()
        query = (
            f'SELECT * FROM "{self.OBD_TABLE}" '
            f'WHERE "所属站点" = ?'
        )
        return pd.read_sql_query(query, self._conn, params=(site,))

    def get_obd_by_uplink_device(self, device: str) -> pd.DataFrame:
        """按上联设备名称筛选 OBD。"""
        if not self.is_connected:
            return pd.DataFrame()
        query = (
            f'SELECT * FROM "{self.OBD_TABLE}" '
            f'WHERE "上联设备名称" LIKE ?'
        )
        return pd.read_sql_query(query, self._conn, params=(f'%{device}%',))


if __name__ == '__main__':
    db = DatabaseManager()
    if db.connect():
        print('[OK] 数据库连接成功')
        tables = db.check_tables_exist()
        print(f'  - 表存在情况: {tables}')
        print(f'  - obd_box 行数: {db.get_table_row_count(db.OBD_TABLE)}')
        print(f'  - OLT网元数据集 行数: {db.get_table_row_count(db.OLT_TABLE)}')

        obd_df = db.get_obd_data()
        olt_df = db.get_olt_data()
        print(f'  - OBD DataFrame 形状: {obd_df.shape}')
        print(f'  - OLT DataFrame 形状: {olt_df.shape}')
        print(f'  - OBD 列名: {list(obd_df.columns)}')
        db.close()
    else:
        print('[FAIL] 数据库连接失败')
