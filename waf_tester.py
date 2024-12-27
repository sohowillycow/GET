#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2024 WillyCow
This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import asyncio
import time
from datetime import datetime
import aiohttp
import pandas as pd
import matplotlib.pyplot as plt
from rich.progress import Progress, TaskID
from typing import Dict, List, Any
import random
from config import Config
import matplotlib as mpl
import platform

# 翻譯字典
TRANSLATIONS = {
    'zh_TW': {
        'report_title': 'WAF測試報告',
        'test_time': '測試時間',
        'duration': '持續時間',
        'threads': '並發線程',
        'seconds': '秒',
        'statistics': '統計摘要',
        'total_requests': '總請求數',
        'successful_requests': '成功請求',
        'blocked_requests': '被阻擋請求',
        'error_requests': '錯誤請求',
        'avg_response_time': '平均響應時間',
        'response_time_dist': '響應時間分佈',
        'response_time': '響應時間 (秒)',
        'request_count': '請求數量',
        'status_dist': '請求狀態碼分佈',
        'report_error': '生成報告時出錯',
        'chart_error': '生成圖表時出錯',
        'no_data': '沒有測試結果數據',
        'missing_column': '結果數據中缺少必要的列'
    },
    'en_US': {
        'report_title': 'WAF Test Report',
        'test_time': 'Test Time',
        'duration': 'Duration',
        'threads': 'Concurrent Threads',
        'seconds': 'seconds',
        'statistics': 'Statistics Summary',
        'total_requests': 'Total Requests',
        'successful_requests': 'Successful Requests',
        'blocked_requests': 'Blocked Requests',
        'error_requests': 'Error Requests',
        'avg_response_time': 'Average Response Time',
        'response_time_dist': 'Response Time Distribution',
        'response_time': 'Response Time (seconds)',
        'request_count': 'Request Count',
        'status_dist': 'Request Status Distribution',
        'report_error': 'Error generating report',
        'chart_error': 'Error generating charts',
        'no_data': 'No test result data',
        'missing_column': 'Missing required column in results'
    }
}

# 設置中文字體
if platform.system() == 'Windows':
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微軟雅黑
elif platform.system() == 'Darwin':
    plt.rcParams['font.sans-serif'] = ['PingFang HK']     # macOS
else:
    plt.rcParams['font.sans-serif'] = ['Noto Sans TC']    # Linux

plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

class WAFTester:
    def __init__(self, config: Config):
        self.config = config
        self.results = []
        self.start_time = None
        self.end_time = None
        self.current_lang = 'zh_TW'  # 默認使用中文

    def set_language(self, lang: str):
        """設置語言"""
        if lang in TRANSLATIONS:
            self.current_lang = lang

    async def send_request(self, session: aiohttp.ClientSession, params: Dict = None) -> Dict[str, Any]:
        """發送單個請求並記錄結果"""
        start_time = time.time()
        try:
            headers = self.config._headers.copy()
            if not headers.get('User-Agent'):
                headers['User-Agent'] = 'WAF-Tester/1.0'

            async with session.get(self.config.url, 
                                 params=params, 
                                 headers=headers,
                                 timeout=30) as response:
                end_time = time.time()
                return {
                    'timestamp': datetime.now().isoformat(),
                    'status': response.status,
                    'response_time': end_time - start_time,
                    'params': params,
                    'headers': headers
                }
        except Exception as e:
            end_time = time.time()
            return {
                'timestamp': datetime.now().isoformat(),
                'status': -1,
                'response_time': end_time - start_time,
                'error': str(e),
                'params': params,
                'headers': headers
            }

    async def worker(self, session: aiohttp.ClientSession):
        """工作線程"""
        while time.time() - self.start_time < self.config.duration:
            if self.config.rate_limit > 0:
                await asyncio.sleep(1 / self.config.rate_limit)

            params = None
            if self.config._params:
                params = random.choice(self.config._params)

            result = await self.send_request(session, params)
            self.results.append(result)

    async def run_test(self, progress_callback=None):
        """運行測試"""
        async with aiohttp.ClientSession() as session:
            workers = [self.worker(session) for _ in range(self.config.threads)]
            try:
                # 創建進度更新任務
                async def update_progress():
                    while True:
                        if progress_callback and progress_callback():
                            break
                        await asyncio.sleep(0.1)

                # 同時運行工作線程和進度更新
                await asyncio.gather(
                    update_progress(),
                    *workers
                )
            except Exception as e:
                print(f"Error during test: {str(e)}")
                raise

    def run(self, progress_callback=None) -> List[Dict[str, Any]]:
        """執行測試"""
        self.start_time = time.time()
        asyncio.run(self.run_test(progress_callback))
        self.end_time = time.time()
        return self.results

    def generate_report(self, results: List[Dict[str, Any]]):
        """生成測試報告"""
        try:
            # 確保結果不為空
            if not results:
                raise ValueError(TRANSLATIONS[self.current_lang]['no_data'])

            # 轉換結果為DataFrame
            df = pd.DataFrame(results)
            
            # 確保必要的列存在
            required_columns = ['status', 'response_time']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"{TRANSLATIONS[self.current_lang]['missing_column']}: {col}")
            
            # 基本統計
            total_requests = len(results)
            successful_requests = len(df[df['status'] == 200])
            blocked_requests = len(df[df['status'] == 403])
            error_requests = len(df[df['status'] == -1])
            avg_response_time = df['response_time'].mean()

            # 生成報告
            t = TRANSLATIONS[self.current_lang]
            report = f"""
{t['report_title']}
{'=' * len(t['report_title'])}
{t['test_time']}：{datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')}
{t['duration']}：{self.config.duration}{t['seconds']}
{t['threads']}：{self.config.threads}

{t['statistics']}：
- {t['total_requests']}：{total_requests}
- {t['successful_requests']}：{successful_requests} ({(successful_requests/total_requests*100) if total_requests > 0 else 0:.2f}%)
- {t['blocked_requests']}：{blocked_requests} ({(blocked_requests/total_requests*100) if total_requests > 0 else 0:.2f}%)
- {t['error_requests']}：{error_requests} ({(error_requests/total_requests*100) if total_requests > 0 else 0:.2f}%)
- {t['avg_response_time']}：{avg_response_time*1000:.2f}ms
"""
            # 保存報告
            with open('waf_test_report.txt', 'w', encoding='utf-8') as f:
                f.write(report)

            # 生成圖表
            try:
                # 響應時間分佈圖
                plt.figure(figsize=(10, 6))
                df['response_time'].hist(bins=50)
                plt.title(t['response_time_dist'], fontsize=12)
                plt.xlabel(t['response_time'], fontsize=10)
                plt.ylabel(t['request_count'], fontsize=10)
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.savefig('response_time_distribution.png', dpi=300, bbox_inches='tight')
                plt.close()

                # 狀態碼分佈圖
                plt.figure(figsize=(8, 8))
                status_counts = df['status'].value_counts()
                if not status_counts.empty:
                    colors = ['#2ecc71', '#e74c3c', '#3498db', '#f1c40f']  # 設置顏色
                    patches, texts, autotexts = plt.pie(
                        status_counts, 
                        labels=status_counts.index,
                        autopct='%1.1f%%',
                        colors=colors,
                        startangle=90
                    )
                    # 設置字體大小
                    plt.setp(autotexts, size=9, weight='bold')
                    plt.setp(texts, size=9)
                    plt.title(t['status_dist'], fontsize=12, pad=20)
                    plt.savefig('status_distribution.png', dpi=300, bbox_inches='tight')
                plt.close()
            except Exception as e:
                print(f"{t['chart_error']}: {str(e)}")

            # 保存詳細結果
            df.to_csv('detailed_results.csv', index=False)
            
        except Exception as e:
            raise Exception(f"{TRANSLATIONS[self.current_lang]['report_error']}: {str(e)}") 