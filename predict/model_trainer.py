# -*- coding: utf-8 -*-
"""
随机森林回归模型训练模块
基于 PON 口聚合特征预测扩容 PON 口需求量。
"""
import os

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


class ModelTrainer:
    """随机森林回归模型训练与评估。"""

    DEFAULT_MODEL_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'pon_demand_rf_model.pkl'
    )

    def __init__(self):
        self.model = None
        self.feature_names = []
        self._X_train = None
        self._X_test = None
        self._y_train = None
        self._y_test = None
        self._metrics = {}

    # ------------------------------------------------------------------
    # 训练
    # ------------------------------------------------------------------
    def train(self, X, y, feature_names=None,
              n_estimators=100, max_depth=None, random_state=42,
              test_size=0.2, progress_callback=None):
        """训练随机森林回归模型。

        Args:
            X: 特征矩阵
            y: 目标值
            feature_names: 特征名列表
            n_estimators: 树数量
            max_depth: 最大深度（None 表示不限制）
            random_state: 随机种子
            test_size: 测试集比例
            progress_callback: 可选回调，用于报告进度 (callable(int percent))

        Returns:
            metrics dict: {'r2', 'rmse', 'mae', 'train_size', 'test_size'}
        """
        if progress_callback:
            progress_callback(10)

        if feature_names is not None:
            self.feature_names = list(feature_names)

        # 划分训练 / 测试集（数据量小时使用 stratify 不适用，按回归处理）
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        if X.shape[0] < 4:
            # 数据过少：全部用于训练
            self._X_train, self._X_test = X, X
            self._y_train, self._y_test = y, y
        else:
            self._X_train, self._X_test, self._y_train, self._y_test = \
                train_test_split(
                    X, y, test_size=test_size, random_state=random_state
                )

        if progress_callback:
            progress_callback(30)

        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )

        if progress_callback:
            progress_callback(50)

        self.model.fit(self._X_train, self._y_train)

        if progress_callback:
            progress_callback(80)

        self._metrics = self.evaluate(self._X_test, self._y_test)
        self._metrics['train_size'] = int(len(self._X_train))
        self._metrics['test_size'] = int(len(self._X_test))

        if progress_callback:
            progress_callback(100)

        return self._metrics

    # ------------------------------------------------------------------
    # 评估
    # ------------------------------------------------------------------
    def evaluate(self, X_test, y_test) -> dict:
        """评估模型并返回指标。"""
        if self.model is None:
            return {}
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        return {
            'r2': float(r2_score(y_test, y_pred)),
            'rmse': float(np.sqrt(mse)),
            'mae': float(mean_absolute_error(y_test, y_pred)),
        }

    @property
    def metrics(self) -> dict:
        return self._metrics

    # ------------------------------------------------------------------
    # 特征重要性
    # ------------------------------------------------------------------
    def feature_importance(self) -> list:
        """返回 [(feature_name, importance), ...] 按重要性降序。"""
        if self.model is None or not self.feature_names:
            return []
        importances = self.model.feature_importances_
        pairs = list(zip(self.feature_names, importances))
        pairs.sort(key=lambda p: p[1], reverse=True)
        return [(name, float(imp)) for name, imp in pairs]

    # ------------------------------------------------------------------
    # 模型持久化
    # ------------------------------------------------------------------
    def save_model(self, path: str = None) -> str:
        if self.model is None:
            raise RuntimeError('未训练模型，无法保存')
        path = path or self.DEFAULT_MODEL_PATH
        joblib.dump({
            'model': self.model,
            'feature_names': self.feature_names,
            'metrics': self._metrics,
        }, path)
        return path

    def load_model(self, path: str = None) -> bool:
        path = path or self.DEFAULT_MODEL_PATH
        if not os.path.exists(path):
            return False
        data = joblib.load(path)
        self.model = data.get('model')
        self.feature_names = data.get('feature_names', [])
        self._metrics = data.get('metrics', {})
        return True

    @property
    def is_trained(self) -> bool:
        return self.model is not None


if __name__ == '__main__':
    from data_processor import DataProcessor
    from db_manager import DatabaseManager

    db = DatabaseManager()
    if db.connect():
        obd_df = db.get_obd_data()
        dp = DataProcessor()
        dp.load_data(obd_df, None)
        X, y, names = dp.prepare_training_data()

        trainer = ModelTrainer()

        def on_progress(p):
            print(f'  训练进度: {p}%')

        metrics = trainer.train(
            X, y, feature_names=names,
            n_estimators=100, random_state=42,
            progress_callback=on_progress
        )
        print('\n[评估指标]')
        for k, v in metrics.items():
            print(f'  {k}: {v}')

        print('\n[特征重要性]')
        for name, imp in trainer.feature_importance():
            print(f'  {name}: {imp:.4f}')

        model_path = trainer.save_model()
        print(f'\n[OK] 模型已保存: {model_path}')
        db.close()
