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
                raise ValueError("沒有測試結果數據")

            # 轉換結果為DataFrame
            df = pd.DataFrame(results)
            
            # 確保必要的列存在
            required_columns = ['status', 'response_time']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"結果數據中缺少必要的列：{col}")
            
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
- 成功請求：{successful_requests} ({(successful_requests/total_requests*100) if total_requests > 0 else 0:.2f}%)
- 被阻擋請求：{blocked_requests} ({(blocked_requests/total_requests*100) if total_requests > 0 else 0:.2f}%)
- 錯誤請求：{error_requests} ({(error_requests/total_requests*100) if total_requests > 0 else 0:.2f}%)
- 平均響應時間：{avg_response_time*1000:.2f}ms
"""
            # 保存報告
            with open('waf_test_report.txt', 'w', encoding='utf-8') as f:
                f.write(report)

            # 生成圖表
            try:
                plt.figure(figsize=(10, 6))
                df['response_time'].hist(bins=50)
                plt.title('響應時間分佈')
                plt.xlabel('響應時間 (秒)')
                plt.ylabel('請求數量')
                plt.savefig('response_time_distribution.png')
                plt.close()

                # 生成狀態碼分佈圖
                plt.figure(figsize=(8, 8))
                status_counts = df['status'].value_counts()
                if not status_counts.empty:
                    status_counts.plot(kind='pie', autopct='%1.1f%%')
                    plt.title('請求狀態碼分佈')
                    plt.savefig('status_distribution.png')
                plt.close()
            except Exception as e:
                print(f"生成圖表時出錯：{str(e)}")

            # 保存詳細結果
            df.to_csv('detailed_results.csv', index=False)
            
        except Exception as e:
            raise Exception(f"生成報告時出錯：{str(e)}") 