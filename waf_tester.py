#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

class WAFTester:
    def __init__(self, config: Config):
        self.config = config
        self.results = []
        self.start_time = None
        self.end_time = None

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

    async def worker(self, session: aiohttp.ClientSession, progress: Progress, task: TaskID):
        """工作線程"""
        while time.time() - self.start_time < self.config.duration:
            if self.config.rate_limit > 0:
                await asyncio.sleep(1 / self.config.rate_limit)

            params = None
            if self.config._params:
                params = random.choice(self.config._params)

            result = await self.send_request(session, params)
            self.results.append(result)
            
            progress.update(task, completed=min(time.time() - self.start_time, self.config.duration))

    async def run_test(self, progress: Progress, task: TaskID):
        """運行測試"""
        async with aiohttp.ClientSession() as session:
            workers = [self.worker(session, progress, task) for _ in range(self.config.threads)]
            await asyncio.gather(*workers)

    def run(self, progress: Progress, task: TaskID) -> List[Dict[str, Any]]:
        """執行測試"""
        self.start_time = time.time()
        asyncio.run(self.run_test(progress, task))
        self.end_time = time.time()
        return self.results

    def generate_report(self, results: List[Dict[str, Any]]):
        """生成測試報告"""
        # 轉換結果為DataFrame
        df = pd.DataFrame(results)
        
        # 基本統計
        total_requests = len(results)
        successful_requests = len(df[df['status'] == 200])
        blocked_requests = len(df[df['status'] == 403])
        error_requests = len(df[df['status'] == -1])
        avg_response_time = df['response_time'].mean()

        # 生成報告
        report = f"""
WAF測試報告
===========
測試時間：{datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')}
持續時間：{self.config.duration}秒
並發線程：{self.config.threads}

統計摘要：
- 總請求數：{total_requests}
- 成功請求：{successful_requests} ({successful_requests/total_requests*100:.2f}%)
- 被阻擋請求：{blocked_requests} ({blocked_requests/total_requests*100:.2f}%)
- 錯誤請求：{error_requests} ({error_requests/total_requests*100:.2f}%)
- 平均響應時間：{avg_response_time*1000:.2f}ms
"""
        # 保存報告
        with open('waf_test_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)

        # 生成圖表
        plt.figure(figsize=(10, 6))
        df['response_time'].hist(bins=50)
        plt.title('響應時間分佈')
        plt.xlabel('響應時間 (秒)')
        plt.ylabel('請求數量')
        plt.savefig('response_time_distribution.png')
        plt.close()

        # 生成狀態碼分佈圖
        plt.figure(figsize=(8, 8))
        df['status'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('請求狀態碼分佈')
        plt.savefig('status_distribution.png')
        plt.close()

        # 保存詳細結果
        df.to_csv('detailed_results.csv', index=False) 