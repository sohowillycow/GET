#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from dataclasses import dataclass
from typing import Dict, List, Optional

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
        if not self.url.startswith(('http://', 'https://')):
            raise ValueError("URL必須以http://或https://開頭")
        
        if self.threads < 1:
            raise ValueError("並發線程數必須大於0")
        
        if self.duration < 1:
            raise ValueError("測試持續時間必須大於0秒")
        
        if self.rate_limit < 0:
            raise ValueError("請求速率限制不能為負數")

    def load_params(self):
        """載入GET參數列表"""
        if self.params_file:
            try:
                with open(self.params_file, 'r', encoding='utf-8') as f:
                    self._params = json.load(f)
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
            except Exception as e:
                raise ValueError(f"無法載入Headers文件：{str(e)}")
        else:
            self._headers = {} 