# -*- coding: utf-8 -*-
"""
数据处理与特征工程模块
实现 OBD 分类、OBD→OLT 站点追溯、PON 口分组、端子利用率计算、ML 特征构造。

数据关系：
  - 一级 OBD：上联设备名称 = OLT 名称，PON口 = 具体 PON 口名称
  - 二级 OBD：上联设备名称 = 一级 OBD 名称，PON口 = 该一级 OBD 上联的 PON 口名称
  - 预测目标：OLT 所属站点（非 OBD 自身所属站点）
"""
import numpy as np
import pandas as pd


class DataProcessor:
    """OBD / PON 口数据处理与特征工程。"""

    # 利用率阈值：超过该值认为当前 PON 口需要扩容（占用新 PON 口）
    EXPANSION_THRESHOLD = 0.9

    def __init__(self):
        self.obd_df = pd.DataFrame()
        self.olt_df = pd.DataFrame()
        # 处理结果缓存
        self._obd_classified = pd.DataFrame()
        self._pon_groups = pd.DataFrame()
        self._features = pd.DataFrame()
        self._X = None
        self._y = None

    # ------------------------------------------------------------------
    # 数据装载
    # ------------------------------------------------------------------
    def load_data(self, obd_df: pd.DataFrame, olt_df: pd.DataFrame = None):
        """装入从 DB 查询得到的 OBD / OLT 数据。"""
        self.obd_df = obd_df.copy() if obd_df is not None else pd.DataFrame()
        self.olt_df = olt_df.copy() if olt_df is not None else pd.DataFrame()
        # 清空缓存
        self._obd_classified = pd.DataFrame()
        self._pon_groups = pd.DataFrame()
        self._features = pd.DataFrame()
        self._X = None
        self._y = None

    # ------------------------------------------------------------------
    # 1. OBD 分类 + OLT 站点追溯
    # ------------------------------------------------------------------
    def classify_obd(self) -> pd.DataFrame:
        """根据上联设备名称区分一级 / 二级 OBD，并追溯每个 OBD 上联的 OLT 所属站点。

        真实数据中上联设备名称为完整 OLT 名称（含"OLT"子串），
        如 '湛江吴川市敏宁路8号三楼机房传输1-OLT001-ZX-C600'。

        分类规则：
          - 上联设备名称含 "OLT"（不区分大小写）且非空 → 一级 OBD（上联为 OLT 的 PON 口）
          - 上联设备名称匹配某个 OBD名称 → 二级 OBD（上联为一级 OBD）
          - 其余（含空值） → 未分类
        """
        if self.obd_df.empty:
            return pd.DataFrame()

        df = self.obd_df.copy()
        uplink = df['上联设备名称'].fillna('').astype(str)
        obd_names_set = set(df['OBD名称'].dropna().astype(str))

        def _classify(name):
            if not name:
                return '未分类'
            if 'OLT' in name.upper():
                return '一级OBD'
            if name in obd_names_set:
                return '二级OBD'
            return '未分类'

        df['OBD级别'] = uplink.apply(_classify)

        # 派生端子利用率（行级）
        # 端子数为计数型，用 int 类型
        total = pd.to_numeric(df['下联端子总数'], errors='coerce').fillna(0)
        free = pd.to_numeric(df['下联端子空闲数'], errors='coerce').fillna(0)
        # 真实数据可能有"下联端子已用数"列，优先使用
        if '下联端子已用数' in df.columns:
            used = pd.to_numeric(df['下联端子已用数'], errors='coerce')
            # 已用数为空时回退到 total - free
            occupied = used.fillna(total - free)
        else:
            occupied = total - free
        occupied = occupied.clip(lower=0)
        # 端子数列保持 int 类型
        df['下联端子总数'] = total.astype(int)
        df['下联端子空闲数'] = free.astype(int)
        df['下联端子占用数'] = occupied.astype(int)
        # 利用率为比率，保留 float
        df['端子利用率'] = np.where(total > 0, occupied / total, 0.0)

        # 追溯 OLT 所属站点
        df = self._trace_olt_site(df)

        self._obd_classified = df
        return df

    def _trace_olt_site(self, df: pd.DataFrame) -> pd.DataFrame:
        """为每条 OBD 记录追溯其最终上联 OLT 的所属站点。

        - 构造 一级 OBD 名称 → 上联 OLT 名称 的映射
        - 构造 OLT 网元名称 → 所属站点 的映射（来自 OLT 数据集）
        - 一级 OBD：直接用上联设备名称作为 OLT 名称
        - 二级 OBD：上联设备名称是一级 OBD 名称，查映射得到 OLT 名称
        """
        if df.empty:
            return df

        # 一级 OBD：上联设备名称即 OLT 名称
        # 构造 一级OBD名称 → 上联OLT名称 映射（供二级 OBD 反查）
        first_level_mask = df['OBD级别'] == '一级OBD'
        obd_to_olt = dict(zip(
            df.loc[first_level_mask, 'OBD名称'].astype(str),
            df.loc[first_level_mask, '上联设备名称'].fillna('').astype(str)
        ))

        # OLT 网元 → 所属站点 映射
        olt_to_site = {}
        if not self.olt_df.empty and 'OLT网元' in self.olt_df.columns \
                and '所属站点' in self.olt_df.columns:
            olt_to_site = dict(zip(
                self.olt_df['OLT网元'].astype(str),
                self.olt_df['所属站点'].astype(str)
            ))

        def _resolve(row):
            uplink = str(row['上联设备名称']) if pd.notna(row['上联设备名称']) else ''
            if row['OBD级别'] == '一级OBD':
                olt_name = uplink
            elif row['OBD级别'] == '二级OBD':
                # 上联设备名称是一级 OBD 名称，反查其上联 OLT 名称
                olt_name = obd_to_olt.get(uplink, '')
            else:
                olt_name = ''
            site = olt_to_site.get(olt_name, '')
            return pd.Series({'上联OLT名称': olt_name, 'OLT所属站点': site})

        trace_df = df.apply(_resolve, axis=1)
        df['上联OLT名称'] = trace_df['上联OLT名称']
        df['OLT所属站点'] = trace_df['OLT所属站点']
        # 未追溯到的填为"未知站点"
        df['OLT所属站点'] = df['OLT所属站点'].replace('', '未知站点')
        return df

    # ------------------------------------------------------------------
    # 2. 按 PON 口分组聚合
    # ------------------------------------------------------------------
    def group_by_pon_port(self) -> pd.DataFrame:
        """按 PON 口分组（同一上联 PON 口下的所有 OBD 含一级/二级）。

        返回每个 PON 口下的聚合统计：
        - 下联端子总数 / 空闲数 / 占用数 / 利用率
        - OBD 数量、一级 OBD 数、二级 OBD 数
        - 关联上联 OLT 名称 / OLT 所属站点（用于按 OLT 站点预测）
        """
        if self._obd_classified.empty:
            self.classify_obd()
        if self._obd_classified.empty:
            return pd.DataFrame()

        df = self._obd_classified
        grouped = df.groupby('PON口', as_index=False).agg(
            下联端子总数=('下联端子总数', 'sum'),
            下联端子空闲数=('下联端子空闲数', 'sum'),
            下联端子占用数=('下联端子占用数', 'sum'),
            OBD数量=('OBD名称', 'count'),
            一级OBD数量=('OBD级别', lambda x: (x == '一级OBD').sum()),
            二级OBD数量=('OBD级别', lambda x: (x == '二级OBD').sum()),
            上联OLT名称=('上联OLT名称', 'first'),
            OLT所属站点=('OLT所属站点', 'first'),
        )
        # 端子计数列保持 int 类型
        grouped['下联端子总数'] = grouped['下联端子总数'].astype(int)
        grouped['下联端子空闲数'] = grouped['下联端子空闲数'].astype(int)
        grouped['下联端子占用数'] = grouped['下联端子占用数'].astype(int)
        grouped['OBD数量'] = grouped['OBD数量'].astype(int)
        grouped['一级OBD数量'] = grouped['一级OBD数量'].astype(int)
        grouped['二级OBD数量'] = grouped['二级OBD数量'].astype(int)
        # 派生 PON 口利用率
        grouped['PON口端子利用率'] = np.where(
            grouped['下联端子总数'] > 0,
            grouped['下联端子占用数'] / grouped['下联端子总数'],
            0.0
        )
        # 是否需要扩容（二分类辅助标签，仅用于报告展示）
        grouped['需要扩容'] = grouped['PON口端子利用率'] >= self.EXPANSION_THRESHOLD
        self._pon_groups = grouped
        return grouped

    # ------------------------------------------------------------------
    # 3. 特征工程 - 训练数据准备
    # ------------------------------------------------------------------
    def build_features(self) -> pd.DataFrame:
        """构造 ML 特征 DataFrame，从 PON 口聚合结果衍生。

        特征列：
            - 下联端子总数
            - 下联端子空闲数
            - 下联端子占用数
            - PON口端子利用率
            - OBD数量
            - 一级OBD数量
            - 二级OBD数量
            - 端子平均利用率（OBD 行级利用率均值）
            - 端子利用率方差
        目标列：
            - 扩容PON口需求量（连续值）：基于利用率估算需要的额外 PON 口数
        """
        if self._pon_groups.empty:
            self.group_by_pon_port()
        if self._pon_groups.empty:
            return pd.DataFrame()

        df = self._pon_groups.copy()
        # 关联 OBD 行级利用率的均值 / 方差
        obd_df = self._obd_classified
        obd_stats = obd_df.groupby('PON口')['端子利用率'].agg(['mean', 'std']).reset_index()
        obd_stats.columns = ['PON口', '端子平均利用率', '端子利用率方差']
        obd_stats['端子利用率方差'] = obd_stats['端子利用率方差'].fillna(0.0)

        df = df.merge(obd_stats, on='PON口', how='left')

        # 目标：扩容 PON 口需求量（连续值）
        # 综合多个因素并叠加噪声，避免模型退化为单变量决定
        # 需求量 ≈ 基础扩容量 + 二级 OBD 分流影响 + 占用率非线性项 + 噪声
        def _compute_demand(row):
            util = row['PON口端子利用率']
            total = float(row['下联端子总数'])
            occupied = float(row['下联端子占用数'])
            obd_cnt = float(row['OBD数量'])
            l2_cnt = float(row['二级OBD数量'])
            mean_util = float(row['端子平均利用率'])
            std_util = float(row['端子利用率方差'])

            # 基础需求：超出阈值的占用端子折算成需要的 PON 口数（假设单 PON 口 256 端子）
            overload = max(0.0, occupied - self.EXPANSION_THRESHOLD * total)
            base_demand = overload / 256.0

            # 二级 OBD 影响：二级 OBD 多时，分流上联一级 OBD，对 OLT 直连 PON 口需求略降
            l2_factor = 1.0 - 0.3 * (l2_cnt / max(obd_cnt, 1.0))
            base_demand *= l2_factor

            # 利用率方差影响：方差大说明部分 OBD 已饱和，需额外扩容
            std_penalty = std_util * 1.5

            # 平均利用率影响：整体水位高时，扩容需求放大
            mean_factor = 1.0 + 0.5 * (mean_util - 0.5)

            # 叠加少量噪声使模型需学习多特征
            noise = np.random.normal(0, 0.05)
            demand = base_demand * mean_factor + std_penalty + noise
            return float(max(0.0, round(demand, 2)))

        np.random.seed(42)  # 保证可重复
        df['扩容PON口需求量'] = df.apply(_compute_demand, axis=1)
        self._features = df
        return df

    def prepare_training_data(self):
        """返回 (X, y, feature_names) 用于模型训练。"""
        if self._features.empty:
            self.build_features()
        if self._features.empty:
            return None, None, []

        feature_cols = [
            '下联端子总数', '下联端子空闲数', '下联端子占用数',
            'PON口端子利用率', 'OBD数量', '一级OBD数量', '二级OBD数量',
            '端子平均利用率', '端子利用率方差'
        ]
        target_col = '扩容PON口需求量'

        X = self._features[feature_cols].values
        y = self._features[target_col].values
        self._X = X
        self._y = y
        return X, y, feature_cols

    # ------------------------------------------------------------------
    # 访问器
    # ------------------------------------------------------------------
    @property
    def obd_classified(self) -> pd.DataFrame:
        if self._obd_classified.empty:
            self.classify_obd()
        return self._obd_classified

    @property
    def pon_groups(self) -> pd.DataFrame:
        if self._pon_groups.empty:
            self.group_by_pon_port()
        return self._pon_groups

    @property
    def features_df(self) -> pd.DataFrame:
        if self._features.empty:
            self.build_features()
        return self._features

    def get_obd_summary(self) -> dict:
        """OBD 分类与 OLT 站点追溯统计摘要。"""
        df = self.obd_classified
        if df.empty:
            return {}
        total = len(df)
        l1 = int((df['OBD级别'] == '一级OBD').sum())
        l2 = int((df['OBD级别'] == '二级OBD').sum())
        avg_util = float(df['端子利用率'].mean()) if total else 0.0
        traced = int((df['OLT所属站点'] != '未知站点').sum())
        olt_sites = int(df['OLT所属站点'].nunique())
        return {
            '总数': total,
            '一级OBD数量': l1,
            '二级OBD数量': l2,
            '平均端子利用率': round(avg_util, 4),
            '已追溯OLT站点数': traced,
            '涉及OLT站点数': olt_sites,
        }


if __name__ == '__main__':
    from db_manager import DatabaseManager

    db = DatabaseManager()
    if db.connect():
        obd_df = db.get_obd_data()
        olt_df = db.get_olt_data()
        dp = DataProcessor()
        dp.load_data(obd_df, olt_df)

        print('[OBD 分类]')
        print(dp.classify_obd()['OBD级别'].value_counts())
        print('\n[OLT 站点追溯结果（前 8 行）]')
        print(dp.obd_classified[['OBD名称', '上联设备名称', 'OBD级别',
                                 '上联OLT名称', 'OLT所属站点', '所属站点']].head(8).to_string(index=False))
        print('\n[PON 口分组统计（含 OLT 所属站点）]')
        print(dp.group_by_pon_port()[['PON口', '上联OLT名称', 'OLT所属站点',
                                       'OBD数量', 'PON口端子利用率']].head().to_string(index=False))
        print('\n[特征工程结果]')
        feat = dp.build_features()
        print(feat.head())
        X, y, names = dp.prepare_training_data()
        print(f'\nX shape: {X.shape}, y shape: {y.shape}')
        print(f'特征列: {names}')
        print(f'\nOBD 摘要: {dp.get_obd_summary()}')
        db.close()
