#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from rich.console import Console
import threading
import queue
from waf_tester import WAFTester
from config import Config
import time
import os

# 翻譯字典
TRANSLATIONS = {
    'zh_TW': {
        'title': "WAF測試工具",
        'target_url': "目標URL:",
        'threads': "並發線程數:",
        'duration': "測試持續時間(秒):",
        'rate_limit': "請求速率限制:",
        'params_file': "GET參數文件:",
        'headers_file': "Headers文件:",
        'browse': "瀏覽",
        'progress': "測試進度",
        'start_test': "開始測試",
        'ready': "就緒",
        'testing': "測試進行中...",
        'test_complete': "測試完成！請查看報告文件。",
        'test_failed': "測試失敗",
        'complete': "完成",
        'error': "錯誤",
        'complete_msg': "測試已完成，報告已生成",
        'current_lang': "當前語言：中文",
        'switch_lang': "Switch to English"
    },
    'en_US': {
        'title': "WAF Testing Tool",
        'target_url': "Target URL:",
        'threads': "Concurrent Threads:",
        'duration': "Test Duration (sec):",
        'rate_limit': "Request Rate Limit:",
        'params_file': "GET Parameters File:",
        'headers_file': "Headers File:",
        'browse': "Browse",
        'progress': "Test Progress",
        'start_test': "Start Test",
        'ready': "Ready",
        'testing': "Testing...",
        'test_complete': "Test completed! Please check the report files.",
        'test_failed': "Test Failed",
        'complete': "Complete",
        'error': "Error",
        'complete_msg': "Test completed, reports generated",
        'current_lang': "Current Language: English",
        'switch_lang': "切換到中文"
    }
}

class WAFTesterGUI:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'zh_TW'  # 默認使用中文
        self.root.title(TRANSLATIONS[self.current_lang]['title'])
        self.root.geometry("600x550")  # 增加高度以容納語言切換按鈕
        
        # 設置最小視窗尺寸
        self.root.minsize(500, 450)
        
        # 配置根窗口的網格權重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.console = Console()
        self.create_widgets()
        
    def create_widgets(self):
        # 創建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置主框架的網格權重
        for i in range(10):  # 增加一行用於語言切換
            main_frame.grid_rowconfigure(i, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # 語言切換框架
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # 當前語言標籤
        self.current_lang_label = ttk.Label(lang_frame, text=TRANSLATIONS[self.current_lang]['current_lang'])
        self.current_lang_label.pack(side=tk.LEFT, padx=5)
        
        # 語言切換按鈕
        self.lang_button = ttk.Button(lang_frame, text=TRANSLATIONS[self.current_lang]['switch_lang'],
                                    command=self.switch_language)
        self.lang_button.pack(side=tk.RIGHT, padx=5)
        
        # URL輸入
        ttk.Label(main_frame, text=TRANSLATIONS[self.current_lang]['target_url']).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame)
        self.url_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # 線程數
        ttk.Label(main_frame, text=TRANSLATIONS[self.current_lang]['threads']).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.threads_var = tk.StringVar(value="10")
        self.threads_entry = ttk.Entry(main_frame, textvariable=self.threads_var, width=10)
        self.threads_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # 持續時間
        ttk.Label(main_frame, text=TRANSLATIONS[self.current_lang]['duration']).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.duration_var = tk.StringVar(value="10")
        self.duration_entry = ttk.Entry(main_frame, textvariable=self.duration_var, width=10)
        self.duration_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # 速率限制
        ttk.Label(main_frame, text=TRANSLATIONS[self.current_lang]['rate_limit']).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.rate_var = tk.StringVar(value="0")
        self.rate_entry = ttk.Entry(main_frame, textvariable=self.rate_var, width=10)
        self.rate_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        # 參數文件
        ttk.Label(main_frame, text=TRANSLATIONS[self.current_lang]['params_file']).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.params_var = tk.StringVar()
        self.params_entry = ttk.Entry(main_frame, textvariable=self.params_var)
        self.params_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        ttk.Button(main_frame, text=TRANSLATIONS[self.current_lang]['browse'],
                  command=lambda: self.browse_file(self.params_var)).grid(row=5, column=2, padx=5)
        
        # Headers文件
        ttk.Label(main_frame, text=TRANSLATIONS[self.current_lang]['headers_file']).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.headers_var = tk.StringVar()
        self.headers_entry = ttk.Entry(main_frame, textvariable=self.headers_var)
        self.headers_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        ttk.Button(main_frame, text=TRANSLATIONS[self.current_lang]['browse'],
                  command=lambda: self.browse_file(self.headers_var)).grid(row=6, column=2, padx=5)
        
        # 進度條框架
        progress_frame = ttk.LabelFrame(main_frame, text=TRANSLATIONS[self.current_lang]['progress'], padding="5")
        progress_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 配置進度條框架的網格權重
        progress_frame.grid_columnconfigure(0, weight=1)
        
        # 進度條
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', variable=self.progress_var)
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5, padx=(5, 5))
        
        # 進度百分比標籤
        self.progress_label = ttk.Label(progress_frame, text="0%", width=6)
        self.progress_label.grid(row=0, column=1, padx=5)
        
        # 開始按鈕
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        
        self.start_button = ttk.Button(button_frame, text=TRANSLATIONS[self.current_lang]['start_test'],
                                     command=self.start_test)
        self.start_button.grid(row=0, column=0)
        
        # 狀態標籤框架
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        status_frame.grid_columnconfigure(0, weight=1)
        
        # 狀態標籤（置中）
        self.status_label = ttk.Label(status_frame, text=TRANSLATIONS[self.current_lang]['ready'], anchor="center")
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

    def switch_language(self):
        """切換界面語言"""
        self.current_lang = 'en_US' if self.current_lang == 'zh_TW' else 'zh_TW'
        self.update_interface_language()
        
    def update_interface_language(self):
        """更新界面上的所有文字"""
        # 更新窗口標題
        self.root.title(TRANSLATIONS[self.current_lang]['title'])
        
        # 更新當前語言標籤
        self.current_lang_label.config(text=TRANSLATIONS[self.current_lang]['current_lang'])
        
        # 更新語言切換按鈕
        self.lang_button.config(text=TRANSLATIONS[self.current_lang]['switch_lang'])
        
        # 更新所有標籤文字
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label):
                        grid_info = child.grid_info()
                        if grid_info:  # 確保部件在網格中
                            row = grid_info['row']
                            if row == 1:
                                child.config(text=TRANSLATIONS[self.current_lang]['target_url'])
                            elif row == 2:
                                child.config(text=TRANSLATIONS[self.current_lang]['threads'])
                            elif row == 3:
                                child.config(text=TRANSLATIONS[self.current_lang]['duration'])
                            elif row == 4:
                                child.config(text=TRANSLATIONS[self.current_lang]['rate_limit'])
                            elif row == 5:
                                child.config(text=TRANSLATIONS[self.current_lang]['params_file'])
                            elif row == 6:
                                child.config(text=TRANSLATIONS[self.current_lang]['headers_file'])
                    elif isinstance(child, ttk.Button) and child != self.lang_button:
                        child.config(text=TRANSLATIONS[self.current_lang]['browse'])
                    elif isinstance(child, ttk.LabelFrame):
                        child.config(text=TRANSLATIONS[self.current_lang]['progress'])
        
        # 更新開始按鈕文字
        self.start_button.config(text=TRANSLATIONS[self.current_lang]['start_test'])
        
        # 更新狀態標籤文字
        current_status = self.status_label.cget("text")
        if current_status == TRANSLATIONS['zh_TW']['ready'] or current_status == TRANSLATIONS['en_US']['ready']:
            self.status_label.config(text=TRANSLATIONS[self.current_lang]['ready'])
        elif current_status == TRANSLATIONS['zh_TW']['testing'] or current_status == TRANSLATIONS['en_US']['testing']:
            self.status_label.config(text=TRANSLATIONS[self.current_lang]['testing'])
        elif current_status == TRANSLATIONS['zh_TW']['test_complete'] or current_status == TRANSLATIONS['en_US']['test_complete']:
            self.status_label.config(text=TRANSLATIONS[self.current_lang]['test_complete'])
        elif current_status == TRANSLATIONS['zh_TW']['test_failed'] or current_status == TRANSLATIONS['en_US']['test_failed']:
            self.status_label.config(text=TRANSLATIONS[self.current_lang]['test_failed'])

    def update_progress(self, current_time, total_time):
        progress = (current_time / total_time) * 100
        self.progress_var.set(progress)
        self.progress_label.config(text=f"{progress:.1f}%")
        self.root.update_idletasks()
        
    def validate_inputs(self):
        """驗證所有輸入"""
        # 驗證URL
        url = self.url_entry.get().strip()
        if not url:
            raise ValueError("請輸入目標URL" if self.current_lang == 'zh_TW' else "Please enter target URL")
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL必須以http://或https://開頭" if self.current_lang == 'zh_TW' else "URL must start with http:// or https://")

        # 驗證線程數
        try:
            threads = int(self.threads_var.get())
            if threads < 1:
                raise ValueError("並發線程數必須大於0" if self.current_lang == 'zh_TW' else "Thread count must be greater than 0")
            if threads > 100:
                raise ValueError("並發線程數不能超過100" if self.current_lang == 'zh_TW' else "Thread count cannot exceed 100")
        except ValueError:
            raise ValueError("並發線程數必須是有效的整數" if self.current_lang == 'zh_TW' else "Thread count must be a valid integer")

        # 驗證持續時間
        try:
            duration = int(self.duration_var.get())
            if duration < 1:
                raise ValueError("測試持續時間必須大於0秒" if self.current_lang == 'zh_TW' else "Test duration must be greater than 0 seconds")
            if duration > 3600:
                raise ValueError("測試持續時間不能超過3600秒（1小時）" if self.current_lang == 'zh_TW' else "Test duration cannot exceed 3600 seconds (1 hour)")
        except ValueError:
            raise ValueError("測試持續時間必須是有效的整數" if self.current_lang == 'zh_TW' else "Test duration must be a valid integer")

        # 驗證速率限制
        try:
            rate_limit = int(self.rate_var.get())
            if rate_limit < 0:
                raise ValueError("請求速率限制不能為負數" if self.current_lang == 'zh_TW' else "Request rate limit cannot be negative")
            if rate_limit > 1000:
                raise ValueError("請求速率限制不能超過1000次/秒" if self.current_lang == 'zh_TW' else "Request rate limit cannot exceed 1000 requests/second")
        except ValueError:
            raise ValueError("請求速率限制必須是有效的整數" if self.current_lang == 'zh_TW' else "Request rate limit must be a valid integer")

        # 驗證文件
        params_file = self.params_var.get()
        if params_file:
            if not os.path.exists(params_file):
                raise ValueError(f"無法找到參數文件：{params_file}" if self.current_lang == 'zh_TW' else f"Cannot find parameters file: {params_file}")
            if not params_file.endswith(('.json', '.txt')):
                raise ValueError("參數文件必須是.json或.txt格式" if self.current_lang == 'zh_TW' else "Parameters file must be in .json or .txt format")

        headers_file = self.headers_var.get()
        if headers_file:
            if not os.path.exists(headers_file):
                raise ValueError(f"無法找到Headers文件：{headers_file}" if self.current_lang == 'zh_TW' else f"Cannot find headers file: {headers_file}")
            if not headers_file.endswith('.json'):
                raise ValueError("Headers文件必須是.json格式" if self.current_lang == 'zh_TW' else "Headers file must be in .json format")

        return url, threads, duration, rate_limit, params_file, headers_file

    def start_test(self):
        """開始測試"""
        try:
            # 驗證輸入
            url, threads, duration, rate_limit, params_file, headers_file = self.validate_inputs()
            
            # 禁用開始按鈕
            self.start_button.state(['disabled'])
            self.status_label.config(text=TRANSLATIONS[self.current_lang]['testing'], anchor="center")
            
            # 重置進度條
            self.progress_var.set(0)
            self.progress_label.config(text="0%")
            
            # 創建配置
            config = Config(
                url=url,
                threads=threads,
                duration=duration,
                rate_limit=rate_limit,
                params_file=params_file or None,
                headers_file=headers_file or None
            )
            
            # 在新線程中運行測試
            def run_test():
                try:
                    tester = WAFTester(config)
                    start_time = time.time()
                    
                    def progress_callback():
                        current_time = min(time.time() - start_time, duration)
                        self.root.after(0, lambda: self.update_progress(current_time, duration))
                        return current_time >= duration
                    
                    results = tester.run(progress_callback)
                    tester.generate_report(results)
                    self.root.after(0, lambda: self.test_completed())
                except Exception as e:
                    self.root.after(0, lambda: self.test_failed(str(e)))
                    
            threading.Thread(target=run_test, daemon=True).start()
            
        except ValueError as e:
            messagebox.showerror(TRANSLATIONS[self.current_lang]['error'], str(e))
            self.reset_test_state()
        except Exception as e:
            messagebox.showerror(TRANSLATIONS[self.current_lang]['error'],
                               f"{'發生未知錯誤' if self.current_lang == 'zh_TW' else 'An unknown error occurred'}：{str(e)}")
            self.reset_test_state()

    def reset_test_state(self):
        """重置測試狀態"""
        self.start_button.state(['!disabled'])  # 啟用開始按鈕
        self.status_label.config(text=TRANSLATIONS[self.current_lang]['ready'], anchor="center")
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        
    def test_completed(self):
        """測試完成處理"""
        self.reset_test_state()
        self.status_label.config(text=TRANSLATIONS[self.current_lang]['test_complete'], anchor="center")
        messagebox.showinfo(TRANSLATIONS[self.current_lang]['complete'],
                          TRANSLATIONS[self.current_lang]['complete_msg'])
        
    def test_failed(self, error_message):
        """測試失敗處理"""
        self.reset_test_state()
        self.status_label.config(text=TRANSLATIONS[self.current_lang]['test_failed'], anchor="center")
        messagebox.showerror(TRANSLATIONS[self.current_lang]['error'],
                           f"{'測試過程中發生錯誤' if self.current_lang == 'zh_TW' else 'An error occurred during testing'}：{error_message}")
        
    def browse_file(self, var):
        filename = filedialog.askopenfilename()
        if filename:
            var.set(filename)

def main():
    root = tk.Tk()
    app = WAFTesterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 