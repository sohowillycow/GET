#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2024 WillyCow
This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from urllib.parse import urlparse

@dataclass
class Config:
    url: str
    threads: int
    duration: int
    rate_limit: int
    params_file: Optional[str] = None
    headers_file: Optional[str] = None
    _params: List[Dict] = None
    _headers: Dict = None

    def __post_init__(self):
        self.validate()
        self.load_params()
        self.load_headers()

    def validate(self):
        """驗證配置參數"""
        # 驗證URL
        if not self.url:
            raise ValueError("URL不能為空")
        if not self.url.startswith(('http://', 'https://')):
            raise ValueError("URL必須以http://或https://開頭")
        
        # 驗證URL格式
        parsed_url = urlparse(self.url)
        if not parsed_url.netloc:
            raise ValueError("URL格式無效：必須包含域名")
        if parsed_url.netloc == "":
            raise ValueError("URL格式無效：域名不能為空")
        if len(parsed_url.netloc) < 3:
            raise ValueError("URL格式無效：域名太短")
        if "." not in parsed_url.netloc:
            raise ValueError("URL格式無效：域名必須包含至少一個點號")
        
        # 驗證線程數
        if not isinstance(self.threads, int):
            raise ValueError("並發線程數必須是整數")
        if self.threads < 1:
            raise ValueError("並發線程數必須大於0")
        if self.threads > 100:
            raise ValueError("並發線程數不能超過100")
        
        # 驗證持續時間
        if not isinstance(self.duration, int):
            raise ValueError("測試持續時間必須是整數")
        if self.duration < 1:
            raise ValueError("測試持續時間必須大於0秒")
        if self.duration > 3600:
            raise ValueError("測試持續時間不能超過3600秒（1小時）")
        
        # 驗證速率限制
        if not isinstance(self.rate_limit, int):
            raise ValueError("請求速率限制必須是整數")
        if self.rate_limit < 0:
            raise ValueError("請求速率限制不能為負數")
        if self.rate_limit > 1000:
            raise ValueError("請求速率限制不能超過1000次/秒")

        # 驗證文件路徑
        if self.params_file:
            if not os.path.exists(self.params_file):
                raise ValueError(f"無法找到參數文件：{self.params_file}")
            if not self.params_file.endswith(('.json', '.txt')):
                raise ValueError("參數文件必須是.json或.txt格式")
            
        if self.headers_file:
            if not os.path.exists(self.headers_file):
                raise ValueError(f"無法找到Headers文件：{self.headers_file}")
            if not self.headers_file.endswith('.json'):
                raise ValueError("Headers文件必須是.json格式")

    def load_params(self):
        """載入GET參數列表"""
        if self.params_file:
            try:
                with open(self.params_file, 'r', encoding='utf-8') as f:
                    if self.params_file.endswith('.json'):
                        self._params = json.load(f)
                        if not isinstance(self._params, list):
                            raise ValueError("參數文件必須包含參數列表")
                    else:  # .txt 文件
                        self._params = [{'param': line.strip()} for line in f if line.strip()]
            except json.JSONDecodeError:
                raise ValueError("參數文件格式錯誤，必須是有效的JSON格式")
            except Exception as e:
                raise ValueError(f"無法載入參數文件：{str(e)}")
        else:
            self._params = []

    def load_headers(self):
        """載入自定義Headers"""
        if self.headers_file:
            try:
                with open(self.headers_file, 'r', encoding='utf-8') as f:
                    self._headers = json.load(f)
                    if not isinstance(self._headers, dict):
                        raise ValueError("Headers文件必須是鍵值對格式")
            except json.JSONDecodeError:
                raise ValueError("Headers文件格式錯誤，必須是有效的JSON格式")
            except Exception as e:
                raise ValueError(f"無法載入Headers文件：{str(e)}")
        else:
            self._headers = {} 