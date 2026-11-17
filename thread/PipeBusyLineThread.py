# 管道段紧张段落分析
# 读取所选文件夹内包含管道段的.CSV资源文件，筛选红线范围为红线外且起始、终止设施类型均为人手井的管道段，
# 对起始/终止设施名称正则提取段落名称，按段落名称统计利用率超80%的紧张管道段长度，按长度倒序输出
# sheet1紧张段落清单、sheet2紧张管道段明细清单。

from PySide6.QtCore import QThread, Signal
import os
import re
import datetime
import pandas as pd
from .publicFunc import *


class PipeBusyLineThread(QThread):
    state_signal = Signal(str)
    error_signal = Signal(str)

    # 列名提取
    PIPE_COLS = ['管道段名称', '管道段编码', '所属区县','所属管道', '实际长度', '起始设施名称', '起始设施类型',
                 '终止设施名称', '终止设施类型', '红线范围', '管孔数', '子孔总数', '占用子孔数']

    def __init__(self, file_dir):
        super().__init__()
        self.file_dir = file_dir

    def run(self):
        try:
            # 读取文件夹内所有包含管道段且后缀名为.CSV（大写）的文件
            files = [os.path.join(self.file_dir, f) for f in os.listdir(self.file_dir)
                     if '管道段' in f and f.endswith('.CSV')]
            if not files:
                self.error_signal.emit('所选文件夹内未找到包含管道段的.CSV文件')
                return
            dfs = []
            for i, file in enumerate(files):
                self.state_signal.emit(f'正在读取文件({i + 1}/{len(files)})：{os.path.basename(file)}')
                dfs.append(readCsvFile(file))
            df = pd.concat(dfs, ignore_index=True)

            # 列名提取
            missing_cols = [col for col in self.PIPE_COLS if col not in df.columns]
            if missing_cols:
                self.error_signal.emit(f'文件缺少所需列：{"、".join(missing_cols)}')
                return
            df = df[self.PIPE_COLS].copy()

            # 筛选红线范围为红线外，且起始设施类型和终止设施类型均为人手井
            for col in ['红线范围', '起始设施类型', '终止设施类型']:
                df[col] = df[col].fillna('').astype(str).str.strip()
            df = df[(df['红线范围'] == '红线外') & (df['起始设施类型'] == '人手井')
                    & (df['终止设施类型'] == '人手井')].copy()
            if df.empty:
                self.error_signal.emit('未筛选到红线范围外且起始、终止设施类型均为人手井的管道段')
                return

            # 数值列转换
            for col in ['实际长度', '管孔数', '子孔总数', '占用子孔数']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            # 段落名称做正则提取起始设施名称、终止设施名称不含数字井号的字符串
            df['起始设施段落'] = df['起始设施名称'].apply(self.extractSectionName)
            df['终止设施段落'] = df['终止设施名称'].apply(self.extractSectionName)
            # 起始设施段落和终止设施段落相同时即为段落名称，否则以起始设施段落为名称
            df['段落名称'] = df.apply(
                lambda r: r['起始设施段落'] if r['起始设施段落'] == r['终止设施段落'] else r['起始设施段落'],
                axis=1)

            # 利用率：占用子孔数/子孔总数，利用率超80%为紧张
            df['利用率(%)'] = df.apply(
                lambda r: round(r['占用子孔数'] / r['子孔总数'] * 100, 2) if r['子孔总数'] > 0 else 0,
                axis=1)
            busy_df = df[df['利用率(%)'] > 80].copy()
            if busy_df.empty:
                self.error_signal.emit('未分析到利用率超80%的紧张管道段')
                return

            self.state_signal.emit('正在统计紧张段落长度...')
            # 按段落名称统计利用率紧张的长度，按长度倒序排序
            stat_df = busy_df.groupby('段落名称').agg(
                紧张管道段数=('管道段名称', 'count'),
                紧张长度=('实际长度', 'sum')
            ).reset_index()
            stat_df['紧张长度'] = stat_df['紧张长度'].round(2)
            stat_df['紧张管道段数'] = stat_df['紧张管道段数'].astype(int)
            stat_df = stat_df.sort_values(by='紧张长度', ascending=False).reset_index(drop=True)

            # 紧张管道段明细按长度倒序输出
            detail_df = busy_df[['段落名称'] + self.PIPE_COLS + ['利用率(%)'] + ['起始设施段落', '终止设施段落']].copy()
            detail_df = detail_df.sort_values(by='实际长度', ascending=False).reset_index(drop=True)

            self.state_signal.emit('正在生成分析结果文件...')
            dt = datetime.datetime.now().strftime('%Y-%m-%d')
            os.makedirs('结果', exist_ok=True)
            out_path = os.path.join('结果', f'管道紧张段落分析-{dt}.xlsx')
            with pd.ExcelWriter(out_path) as writer:
                stat_df.to_excel(writer, sheet_name='紧张段落清单', index=False)
                detail_df.to_excel(writer, sheet_name='紧张管道段明细清单', index=False)

            self.state_signal.emit(f'分析完成，结果已保存至：{out_path}')
        except Exception as e:
            self.error_signal.emit(f'管道紧张段落分析失败：{str(e)}')

    def extractSectionName(self, name):
        '''正则提取名称中不含数字、井号的字符串作为段落名称'''
        if pd.isnull(name):
            return ''
        name = str(name).strip()
        m = re.match(r'(.*?)\d+[#号井]+', name)
        if m:
            return m.group(1).strip()
        return name
