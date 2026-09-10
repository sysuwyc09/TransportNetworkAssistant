# -*- coding: utf-8 -*-
"""
预测模块
基于训练好的随机森林模型，预测 OLT 站点 PON 口资源需求并给出扩容建议。
"""
import numpy as np
import pandas as pd

from .data_processor import DataProcessor


class Predictor:
    """PON 口资源需求预测器。"""

    def __init__(self, model_trainer=None):
        """
        Args:
            model_trainer: 已训练好的 ModelTrainer 实例
        """
        self.trainer = model_trainer

    def set_model(self, model_trainer):
        self.trainer = model_trainer

    # ------------------------------------------------------------------
    # 单 PON 口预测
    # ------------------------------------------------------------------
    def predict(self, X) -> np.ndarray:
        """对特征矩阵 X 进行预测，返回扩容 PON 口需求量数组。"""
        if self.trainer is None or not self.trainer.is_trained:
            raise RuntimeError('模型未训练，无法预测')
        X = np.asarray(X, dtype=float)
        return self.trainer.model.predict(X)

    # ------------------------------------------------------------------
    # 批量预测 - 基于 DataProcessor 输出
    # ------------------------------------------------------------------
    def predict_from_features(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """根据 build_features() 输出进行批量预测。

        返回带预测列的 DataFrame：
            - 预测扩容PON口需求量
            - 是否需要扩容 (bool)
            - 建议措施 (text)
        """
        if self.trainer is None or not self.trainer.is_trained:
            raise RuntimeError('模型未训练，无法预测')

        feature_cols = self.trainer.feature_names
        missing = [c for c in feature_cols if c not in features_df.columns]
        if missing:
            raise ValueError(f'特征矩阵缺少列: {missing}')

        X = features_df[feature_cols].values
        preds = self.trainer.model.predict(X)

        result = features_df.copy()
        result['预测扩容PON口需求量'] = np.round(preds, 2)

        # 扩容阈值：预测需求量 > 0.5 视为需要扩容
        result['是否需要扩容'] = result['预测扩容PON口需求量'] > 0.5

        def _advice(row):
            need = row['是否需要扩容']
            demand = row['预测扩容PON口需求量']
            if not need:
                return '资源充足，无需扩容'
            if demand >= 1.0:
                return f'建议新增 {int(np.ceil(demand))} 个 PON 口'
            return '关注端子利用率，规划扩容'
        result['建议措施'] = result.apply(_advice, axis=1)
        return result

    # ------------------------------------------------------------------
    # 按 OLT 站点汇总
    # ------------------------------------------------------------------
    def get_recommendations(self, prediction_df: pd.DataFrame,
                            olt_df: pd.DataFrame = None) -> pd.DataFrame:
        """按 OLT 所属站点汇总预测结果，输出扩容建议汇总表。

        Args:
            prediction_df: predict_from_features() 输出（需含 OLT所属站点 列，
                           由 DataProcessor 追溯得到）
            olt_df: OLT 端口资源表（可选，其 所属站点 列即 OLT 站点，
                    用于关联空闲 PON 口）

        Returns:
            DataFrame 列：
                - OLT所属站点
                - OLT网元数
                - PON口数量
                - 预测总扩容PON口需求量
                - 当前空闲PON口数
                - 是否需要扩容
                - 高风险PON口数
                - 综合建议
        """
        if prediction_df.empty:
            return pd.DataFrame()

        # 优先用追溯得到的 OLT所属站点；缺失时回退到所属站点
        site_col = 'OLT所属站点' if 'OLT所属站点' in prediction_df.columns \
            else '所属站点'

        # OLT 站点维度聚合
        site_agg = prediction_df.groupby(site_col, as_index=False).agg(
            PON口数量=('PON口', 'count'),
            预测总扩容PON口需求量=('预测扩容PON口需求量', 'sum'),
            高风险PON口数=('是否需要扩容', lambda x: int(x.sum())),
        )
        # 重命名为标准列名
        site_agg = site_agg.rename(columns={site_col: 'OLT所属站点'})
        site_agg['预测总扩容PON口需求量'] = site_agg['预测总扩容PON口需求量'].round(2)

        # 关联 OLT 空闲 PON 口数据（olt_df 的 所属站点 即 OLT 站点）
        if olt_df is not None and not olt_df.empty and '所属站点' in olt_df.columns:
            olt_sum = olt_df.groupby('所属站点', as_index=False).agg(
                当前空闲PON口数=('PON口空闲数', 'sum'),
                OLT网元数=('OLT网元', 'count'),
            ).rename(columns={'所属站点': 'OLT所属站点'})
            site_agg = site_agg.merge(olt_sum, on='OLT所属站点', how='left')
        else:
            site_agg['当前空闲PON口数'] = 0
            site_agg['OLT网元数'] = 0

        site_agg['当前空闲PON口数'] = site_agg['当前空闲PON口数'].fillna(0).astype(int)
        site_agg['OLT网元数'] = site_agg['OLT网元数'].fillna(0).astype(int)
        site_agg['PON口数量'] = site_agg['PON口数量'].astype(int)
        site_agg['高风险PON口数'] = site_agg['高风险PON口数'].astype(int)
        site_agg['是否需要扩容'] = (
            site_agg['预测总扩容PON口需求量'] > site_agg['当前空闲PON口数']
        )

        def _overall_advice(row):
            need = row['是否需要扩容']
            demand = row['预测总扩容PON口需求量']
            free = row['当前空闲PON口数']
            if not need:
                return f'空闲 PON 口充足（{free}），暂无需扩容'
            shortage = demand - free
            return (f'预计缺口 {shortage:.1f} 个 PON 口，'
                    f'建议新增 OLT 板卡或扩容 PON 口资源')
        site_agg['综合建议'] = site_agg.apply(_overall_advice, axis=1)

        # 列顺序
        cols = ['OLT所属站点', 'OLT网元数', 'PON口数量', '预测总扩容PON口需求量',
                '当前空闲PON口数', '是否需要扩容', '高风险PON口数', '综合建议']
        return site_agg[cols]


if __name__ == '__main__':
    from db_manager import DatabaseManager
    from model_trainer import ModelTrainer

    db = DatabaseManager()
    if db.connect():
        obd_df = db.get_obd_data()
        olt_df = db.get_olt_data()

        # 数据处理 + 训练
        dp = DataProcessor()
        dp.load_data(obd_df, olt_df)
        X, y, names = dp.prepare_training_data()

        trainer = ModelTrainer()
        trainer.train(X, y, feature_names=names, n_estimators=100, random_state=42)

        # 预测
        predictor = Predictor(trainer)
        features_df = dp.features_df
        pred_df = predictor.predict_from_features(features_df)
        print('[预测结果（前 10 行）]')
        print(pred_df[['PON口', 'OLT所属站点', '预测扩容PON口需求量',
                       '是否需要扩容', '建议措施']].head(10).to_string(index=False))

        rec_df = predictor.get_recommendations(pred_df, olt_df)
        print('\n[OLT 站点扩容建议汇总]')
        print(rec_df.to_string(index=False))
        db.close()
