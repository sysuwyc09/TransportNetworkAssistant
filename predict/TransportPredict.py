# -*- coding: utf-8 -*-
"""
TransportPredict 业务逻辑实现
连接 UI 与各业务模块（DB / 数据处理 / 模型 / 预测），实现 4 个 tab 页功能。
"""
import os

import pandas as pd
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from .ui_TransportPredict import Ui_TransportPredict
from .db_manager import DatabaseManager
from .data_processor import DataProcessor
from .model_trainer import ModelTrainer
from .predictor import Predictor

# matplotlib 嵌入 PySide6
import matplotlib
matplotlib.use('QtAgg')
# 中文字体配置（解决图表中文乱码）
import matplotlib.font_manager as fm
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei',
                                          'DengXian', 'SimSun']
matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import warnings
warnings.filterwarnings('ignore')  # 抑制 matplotlib 中文字体警告


class WorkerThread(QtCore.QThread):
    """通用后台工作线程。

    在子线程中执行耗时任务，通过 state_signal 报告进度文本，
    通过 finished_signal 投递（结果, 错误信息）。

    用法：
        def task(state_callback):
            state_callback('开始加载...')
            result = do_heavy_work()
            state_callback('完成')
            return result
        worker = WorkerThread(task)
        worker.state_signal.connect(self._on_state)
        worker.finished_signal.connect(self._on_finished)
        worker.start()
    """
    state_signal = QtCore.Signal(str)
    finished_signal = QtCore.Signal(object, str)  # (result, error_message)

    def __init__(self, func, parent=None):
        super().__init__(parent)
        self._func = func

    def run(self):
        try:
            result = self._func(state_callback=self._emit_state)
            self.finished_signal.emit(result, '')
        except Exception as e:
            self.finished_signal.emit(None, str(e))

    def _emit_state(self, msg):
        self.state_signal.emit(str(msg))


class PandasModel(QtCore.QAbstractTableModel):
    """QTableView 用的 pandas DataFrame 模型。"""

    def __init__(self, df: pd.DataFrame = None):
        super().__init__()
        self._df = df if df is not None else pd.DataFrame()

    def set_dataframe(self, df: pd.DataFrame):
        self.beginResetModel()
        self._df = df.copy() if df is not None else pd.DataFrame()
        self.endResetModel()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        val = self._df.iloc[index.row(), index.column()]
        if pd.isna(val):
            return ''
        if isinstance(val, float):
            return f'{val:.4f}' if abs(val) < 100 else f'{val:.2f}'
        return str(val)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return str(self._df.columns[section])
        return str(section + 1)


class TransportPredict(QtWidgets.QMainWindow):
    """传输资源预测主窗口。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TransportPredict()
        self.ui.setupUi(self)

        # 业务模块
        self.db = DatabaseManager()
        self.dp = DataProcessor()
        self.trainer = ModelTrainer()
        self.predictor = Predictor()

        # 数据缓存
        self._obd_df = pd.DataFrame()
        self._olt_df = pd.DataFrame()
        self._prediction_df = pd.DataFrame()
        self._recommendation_df = pd.DataFrame()

        # 图表画布
        self._util_canvas = None
        self._feat_canvas = None

        self._init_charts()
        self._connect_signals()
        self._update_conn_status(False)

        # 工作线程引用（防止被 GC）
        self._worker = None

    # ------------------------------------------------------------------
    # 初始化
    # ------------------------------------------------------------------
    def _connect_signals(self):
        self.ui.btnTestConn.clicked.connect(self.on_test_conn)
        self.ui.btnLoadOBD.clicked.connect(self.on_load_obd)
        self.ui.btnLoadOLT.clicked.connect(self.on_load_olt)
        self.ui.btnProcessData.clicked.connect(self.on_process_data)
        self.ui.btnTrainModel.clicked.connect(self.on_train_model)
        self.ui.btnPredict.clicked.connect(self.on_predict)
        self.ui.btnExportCSV.clicked.connect(self.on_export_csv)

    def _init_charts(self):
        # 端子利用率分布图
        layout_util = QtWidgets.QVBoxLayout(self.ui.widgetChartUtil)
        self._util_canvas = FigureCanvas(Figure(figsize=(6, 3)))
        layout_util.addWidget(self._util_canvas)

        # 特征重要性图
        layout_feat = QtWidgets.QVBoxLayout(self.ui.widgetChartFeatureImp)
        self._feat_canvas = FigureCanvas(Figure(figsize=(6, 3)))
        layout_feat.addWidget(self._feat_canvas)

    # ------------------------------------------------------------------
    # Tab 1 - 数据输入
    # ------------------------------------------------------------------
    def on_test_conn(self):
        ok = self.db.connect()
        self._update_conn_status(ok)
        if ok:
            tables = self.db.check_tables_exist()
            obd_cnt = self.db.get_table_row_count(DatabaseManager.OBD_TABLE)
            olt_cnt = self.db.get_table_row_count(DatabaseManager.OLT_TABLE)
            QtWidgets.QMessageBox.information(
                self, '连接成功',
                f'数据库连接成功！\n'
                f'  - {DatabaseManager.OBD_TABLE}: {obd_cnt} 行\n'
                f'  - {DatabaseManager.OLT_TABLE}: {olt_cnt} 行'
            )

    def on_load_obd(self):
        # 主线程仅做连通性预检，实际查询在子线程用独立连接
        if not self.db.is_connected and not self.db.connect():
            self._update_conn_status(False)
            QtWidgets.QMessageBox.warning(self, '错误', '数据库未连接')
            return
        self._update_conn_status(True)
        db_path = self.db.db_path

        def task(state_callback):
            state_callback('正在从数据库读取 OBD 数据...')
            # 子线程创建独立连接，避免 SQLite 跨线程报错
            db = DatabaseManager(db_path)
            if not db.connect():
                raise RuntimeError('子线程数据库连接失败')
            try:
                df = db.get_obd_data()
            finally:
                db.close()
            state_callback(
                f'OBD 数据加载完成：{len(df)} 行 × {len(df.columns)} 列')
            return df

        def on_finished(result, error):
            if error:
                self.statusBar().showMessage(f'OBD 加载失败：{error}', 5000)
                QtWidgets.QMessageBox.critical(self, '加载错误', error)
                return
            self._obd_df = result
            self._show_dataframe(result, self.ui.tableViewData)
            self.ui.labelDataSummary.setText(
                f'数据摘要：OBD 表 {len(result)} 行 × '
                f'{len(result.columns)} 列'
            )
            self.ui.labelTableTitle.setText(
                f'数据预览（OBD 表，共 {len(result)} 行）：')
            self.statusBar().showMessage('OBD 数据加载完成', 5000)

        self._start_worker(task, on_finished, '正在加载 OBD 数据...')

    def on_load_olt(self):
        # 主线程仅做连通性预检，实际查询在子线程用独立连接
        if not self.db.is_connected and not self.db.connect():
            self._update_conn_status(False)
            QtWidgets.QMessageBox.warning(self, '错误', '数据库未连接')
            return
        self._update_conn_status(True)
        db_path = self.db.db_path

        def task(state_callback):
            state_callback('正在从数据库读取 OLT 数据...')
            # 子线程创建独立连接，避免 SQLite 跨线程报错
            db = DatabaseManager(db_path)
            if not db.connect():
                raise RuntimeError('子线程数据库连接失败')
            try:
                df = db.get_olt_data()
            finally:
                db.close()
            state_callback(
                f'OLT 数据加载完成：{len(df)} 行 × {len(df.columns)} 列')
            return df

        def on_finished(result, error):
            if error:
                self.statusBar().showMessage(f'OLT 加载失败：{error}', 5000)
                QtWidgets.QMessageBox.critical(self, '加载错误', error)
                return
            self._olt_df = result
            self._show_dataframe(result, self.ui.tableViewData)
            self.ui.labelDataSummary.setText(
                f'数据摘要：OLT 表 {len(result)} 行 × '
                f'{len(result.columns)} 列'
            )
            self.ui.labelTableTitle.setText(
                f'数据预览（OLT 表，共 {len(result)} 行）：')
            self.statusBar().showMessage('OLT 数据加载完成', 5000)

        self._start_worker(task, on_finished, '正在加载 OLT 数据...')

    # ------------------------------------------------------------------
    # Tab 2 - 数据处理
    # ------------------------------------------------------------------
    def on_process_data(self):
        if self._obd_df.empty:
            QtWidgets.QMessageBox.warning(self, '提示', '请先加载 OBD 数据')
            return

        def task(state_callback):
            state_callback('正在装入数据...')
            self.dp.load_data(self._obd_df, self._olt_df)
            state_callback('正在执行 OBD 分类与端子统计...')
            self.dp.classify_obd()
            state_callback('正在按 PON 口分组聚合...')
            pon_df = self.dp.group_by_pon_port()
            state_callback('正在构造机器学习特征...')
            self.dp.build_features()
            summary = self.dp.get_obd_summary()
            state_callback(
                f'数据处理完成：{len(pon_df)} 个 PON 口，'
                f'涉及 {summary["涉及OLT站点数"]} 个 OLT 站点')
            return {'pon_df': pon_df, 'summary': summary}

        def on_finished(result, error):
            if error:
                self.statusBar().showMessage(f'数据处理失败：{error}', 5000)
                QtWidgets.QMessageBox.critical(self, '处理错误', error)
                return
            pon_df = result['pon_df']
            summary = result['summary']
            self._show_dataframe(pon_df, self.ui.tableViewPonStats)
            self.ui.labelObdSummary.setText(
                f'OBD 摘要：总数 {summary["总数"]}，'
                f'一级 {summary["一级OBD数量"]}，'
                f'二级 {summary["二级OBD数量"]}，'
                f'平均利用率 {summary["平均端子利用率"]:.2%}，'
                f'已追溯 {summary["已追溯OLT站点数"]} 条，'
                f'涉及 {summary["涉及OLT站点数"]} 个 OLT 站点'
            )
            self._draw_utilization_chart()
            self.statusBar().showMessage('数据处理完成', 5000)
            QtWidgets.QMessageBox.information(
                self, '处理完成',
                f'数据处理完成！\n'
                f'  - 共 {len(pon_df)} 个 PON 口\n'
                f'  - 一级 OBD: {summary["一级OBD数量"]}，'
                f'二级 OBD: {summary["二级OBD数量"]}\n'
                f'  - 已追溯 OLT 站点: {summary["已追溯OLT站点数"]} 条，'
                f'涉及 {summary["涉及OLT站点数"]} 个 OLT 站点'
            )

        self._start_worker(task, on_finished, '正在执行数据处理...')

    # ------------------------------------------------------------------
    # Tab 3 - 模型训练
    # ------------------------------------------------------------------
    def on_train_model(self):
        if self.dp.obd_classified.empty:
            QtWidgets.QMessageBox.warning(self, '提示', '请先执行数据处理')
            return

        # 预读参数（避免在子线程访问 UI 控件）
        n_est = self.ui.spinNEstimators.value()
        max_depth = self.ui.spinMaxDepth.value()
        rs = self.ui.spinRandomState.value()
        max_depth_arg = None if max_depth == 0 else max_depth

        self.ui.progressBarTrain.setValue(0)
        self.ui.btnTrainModel.setEnabled(False)

        def task(state_callback):
            state_callback('正在准备训练数据...')
            X, y, names = self.dp.prepare_training_data()

            def progress(p):
                # 训练器回调以 int 进度上报，转成文本状态
                state_callback(f'模型训练中... {p}%')

            state_callback(
                f'开始训练随机森林（n_estimators={n_est}, '
                f'max_depth={max_depth_arg}, random_state={rs}）...')
            metrics = self.trainer.train(
                X, y, feature_names=names,
                n_estimators=n_est,
                max_depth=max_depth_arg,
                random_state=rs,
                progress_callback=progress
            )
            self.predictor.set_model(self.trainer)
            state_callback(
                f'训练完成：R²={metrics["r2"]:.4f}, '
                f'RMSE={metrics["rmse"]:.4f}')
            return metrics

        def on_finished(result, error):
            if error:
                self.statusBar().showMessage(f'训练失败：{error}', 5000)
                self.ui.progressBarTrain.setValue(0)
                self.ui.btnTrainModel.setEnabled(True)
                QtWidgets.QMessageBox.critical(self, '训练错误', error)
                return
            metrics = result
            self.ui.progressBarTrain.setValue(100)
            self.ui.labelMetrics.setText(
                f'评估指标：R²={metrics["r2"]:.4f}, '
                f'RMSE={metrics["rmse"]:.4f}, '
                f'MAE={metrics["mae"]:.4f} '
                f'(训练集 {metrics["train_size"]}, '
                f'测试集 {metrics["test_size"]})'
            )
            self._draw_feature_importance_chart()
            self.statusBar().showMessage('模型训练完成', 5000)
            QtWidgets.QMessageBox.information(
                self, '训练完成',
                f'模型训练完成！\n  - R²: {metrics["r2"]:.4f}\n  - '
                f'RMSE: {metrics["rmse"]:.4f}\n  - MAE: {metrics["mae"]:.4f}'
            )
            self.ui.btnTrainModel.setEnabled(True)

        self._start_worker(task, on_finished, '正在执行模型训练...')

    # ------------------------------------------------------------------
    # Tab 4 - 结果预测
    # ------------------------------------------------------------------
    def on_predict(self):
        if not self.trainer.is_trained:
            QtWidgets.QMessageBox.warning(self, '提示', '请先训练模型')
            return
        features_df = self.dp.features_df
        if features_df.empty:
            QtWidgets.QMessageBox.warning(
                self, '提示', '特征数据为空，请重跑数据处理')
            return

        def task(state_callback):
            state_callback('正在执行模型预测...')
            prediction_df = self.predictor.predict_from_features(features_df)
            state_callback(
                f'已完成 {len(prediction_df)} 个 PON 口预测，'
                f'正在按 OLT 站点汇总...')
            recommendation_df = self.predictor.get_recommendations(
                prediction_df, self._olt_df)
            need_count = int(recommendation_df['是否需要扩容'].sum())
            state_callback(
                f'预测完成：共 {len(recommendation_df)} 个 OLT 站点，'
                f'需扩容 {need_count} 个')
            return {'prediction_df': prediction_df,
                    'recommendation_df': recommendation_df}

        def on_finished(result, error):
            if error:
                self.statusBar().showMessage(f'预测失败：{error}', 5000)
                QtWidgets.QMessageBox.critical(self, '预测错误', error)
                return
            self._prediction_df = result['prediction_df']
            self._recommendation_df = result['recommendation_df']
            self._show_dataframe(self._recommendation_df, self.ui.tableViewResult)
            advice_html = self._build_advice_html()
            self.ui.textEditAdvice.setHtml(advice_html)
            need_count = int(
                self._recommendation_df['是否需要扩容'].sum())
            self.statusBar().showMessage('结果预测完成', 5000)
            QtWidgets.QMessageBox.information(
                self, '预测完成',
                f'预测完成！\n  - 共 {len(self._recommendation_df)} 个 OLT 站点\n  - '
                f'需扩容站点: {need_count} 个'
            )

        self._start_worker(task, on_finished, '正在执行结果预测...')

    def on_export_csv(self):
        if self._recommendation_df.empty:
            QtWidgets.QMessageBox.warning(self, '提示', '无结果可导出，请先执行预测')
            return
        default_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'pon_demand_prediction.csv'
        )
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, '导出 CSV', default_path, 'CSV Files (*.csv)'
        )
        if not path:
            return
        try:
            self._recommendation_df.to_csv(path, index=False, encoding='utf-8-sig')
            QtWidgets.QMessageBox.information(self, '导出成功', f'已导出：{path}')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, '导出错误', str(e))

    # ------------------------------------------------------------------
    # 线程辅助方法
    # ------------------------------------------------------------------
    def _start_worker(self, task_func, on_finished,
                     initial_msg: str = '正在执行...'):
        """启动后台工作线程执行耗时任务。

        Args:
            task_func: 接受 state_callback 关键字参数的可调用对象，返回结果
            on_finished: 主线程回调 (result, error) -> None，用于更新 UI
            initial_msg: 状态栏初始提示
        """
        if self._worker is not None and self._worker.isRunning():
            QtWidgets.QMessageBox.information(
                self, '提示', '当前有任务正在执行，请稍后再试')
            return
        self.statusBar().showMessage(initial_msg)
        self._worker = WorkerThread(task_func, parent=self)
        self._worker.state_signal.connect(self._on_worker_state)
        self._worker.finished_signal.connect(on_finished)
        # 线程结束后清理引用
        self._worker.finished.connect(self._on_worker_destroyed)
        self._worker.start()

    def _on_worker_state(self, msg: str):
        """工作线程状态更新 → 状态栏。"""
        self.statusBar().showMessage(msg)

    def _on_worker_destroyed(self):
        """工作线程对象销毁时清理引用。"""
        sender = self.sender()
        if self._worker is sender:
            self._worker = None

    def _update_conn_status(self, connected: bool):
        if connected:
            self.ui.labelConnStatus.setText(
                '<span style="color:green;">● 数据库连接状态：已连接</span>'
            )
            self.ui.labelConnStatus.setTextFormat(Qt.RichText)
        else:
            self.ui.labelConnStatus.setText(
                '<span style="color:red;">● 数据库连接状态：未连接</span>'
            )
            self.ui.labelConnStatus.setTextFormat(Qt.RichText)

    def _show_dataframe(self, df: pd.DataFrame, tableview: QtWidgets.QTableView):
        model = PandasModel(df)
        tableview.setModel(model)
        tableview.resizeColumnsToContents()
        # 限制列宽避免过宽
        for col in range(model.columnCount()):
            width = tableview.columnWidth(col)
            tableview.setColumnWidth(col, min(max(width, 80), 200))

    def _draw_utilization_chart(self):
        self._util_canvas.figure.clear()
        ax = self._util_canvas.figure.add_subplot(111)
        pon_df = self.dp.pon_groups
        if pon_df.empty:
            ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        else:
            ax.hist(pon_df['PON口端子利用率'], bins=20, color='#4A90E2',
                    edgecolor='white', alpha=0.85)
            ax.axvline(DataProcessor.EXPANSION_THRESHOLD, color='red',
                       linestyle='--', label=f'扩容阈值 ({DataProcessor.EXPANSION_THRESHOLD})')
            ax.set_xlabel('PON 口端子利用率')
            ax.set_ylabel('PON 口数量')
            ax.set_title('PON 口端子利用率分布')
            ax.legend()
        self._util_canvas.figure.tight_layout()
        self._util_canvas.draw()

    def _draw_feature_importance_chart(self):
        self._feat_canvas.figure.clear()
        ax = self._feat_canvas.figure.add_subplot(111)
        importance = self.trainer.feature_importance()
        if not importance:
            ax.text(0.5, 0.5, '无数据', ha='center', va='center')
        else:
            names = [p[0] for p in importance]
            values = [p[1] for p in importance]
            y_pos = range(len(names))
            ax.barh(y_pos, values, color='#50C878', edgecolor='white')
            ax.set_yticks(list(y_pos))
            ax.set_yticklabels(names)
            ax.invert_yaxis()
            ax.set_xlabel('重要性')
            ax.set_title('特征重要性')
        self._feat_canvas.figure.tight_layout()
        self._feat_canvas.draw()

    def _build_advice_html(self) -> str:
        if self._recommendation_df.empty:
            return '<p>无预测结果。</p>'
        need_df = self._recommendation_df[
            self._recommendation_df['是否需要扩容']
        ]
        total_demand = float(self._recommendation_df['预测总扩容PON口需求量'].sum())
        total_sites = len(self._recommendation_df)
        need_count = len(need_df)

        html_parts = [
            '<h3>OLT 站点扩容建议汇总</h3>',
            f'<p>共 <b>{total_sites}</b> 个站点，其中 <b style="color:red;">{need_count}</b> '
            f'个需扩容，预测总扩容 PON 口需求量 <b>{total_demand:.2f}</b> 个。</p>'
        ]
        if need_count > 0:
            html_parts.append('<h4>需扩容 OLT 站点详情：</h4><ul>')
            for _, row in need_df.iterrows():
                html_parts.append(
                    f'<li><b>{row["OLT所属站点"]}</b>：'
                    f'预测需求 {row["预测总扩容PON口需求量"]:.2f}，'
                    f'当前空闲 {row["当前空闲PON口数"]:.0f}，'
                    f'{row["综合建议"]}</li>'
                )
            html_parts.append('</ul>')
        else:
            html_parts.append('<p>所有站点 PON 口资源充足，暂无需扩容。</p>')
        return ''.join(html_parts)

    def closeEvent(self, event):
        """窗口关闭时等待后台线程退出，避免僵尸线程。"""
        if self._worker is not None and self._worker.isRunning():
            self.statusBar().showMessage('正在等待后台任务结束...')
            self._worker.quit()
            self._worker.wait(5000)
        super().closeEvent(event)

    def setCloseCallback(self, callback):
        """设置窗口关闭时的回调函数"""
        self.close_callback = callback

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = TransportPredict()
    window.show()
    sys.exit(app.exec())
