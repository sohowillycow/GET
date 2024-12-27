#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2024 WillyCow
This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import click
from rich.console import Console
from rich.progress import Progress
from waf_tester import WAFTester
from config import Config

console = Console()

@click.command()
@click.option('--url', required=True, help='目標URL')
@click.option('--threads', default=10, help='並發線程數')
@click.option('--duration', default=10, help='測試持續時間(秒)')
@click.option('--rate-limit', default=0, help='請求速率限制(每秒請求數，0表示無限制)')
@click.option('--params', help='GET參數列表文件路徑')
@click.option('--headers', help='自定義Headers文件路徑(JSON格式)')
def main(url: str, threads: int, duration: int, rate_limit: int, params: str, headers: str):
    """WAF規則壓力測試工具"""
    try:
        # 載入配置
        config = Config(
            url=url,
            threads=threads,
            duration=duration,
            rate_limit=rate_limit,
            params_file=params,
            headers_file=headers
        )

        # 初始化測試器
        tester = WAFTester(config)

        with Progress() as progress:
            # 開始測試
            task = progress.add_task("[cyan]執行測試中...", total=duration)
            results = tester.run(progress, task)

            # 生成報告
            tester.generate_report(results)

        console.print("[green]測試完成！請查看報告文件。")

    except Exception as e:
        console.print(f"[red]錯誤：{str(e)}")
        raise click.Abort()

if __name__ == '__main__':
    main() 