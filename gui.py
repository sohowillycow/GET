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

class WAFTesterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WAF測試工具")
        self.root.geometry("600x500")
        self.console = Console()
        self.create_widgets()
        
    def create_widgets(self):
        # 創建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # URL輸入
        ttk.Label(main_frame, text="目標URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 線程數
        ttk.Label(main_frame, text="並發線程數:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.threads_var = tk.StringVar(value="10")
        self.threads_entry = ttk.Entry(main_frame, textvariable=self.threads_var, width=10)
        self.threads_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 持續時間
        ttk.Label(main_frame, text="測試持續時間(秒):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.duration_var = tk.StringVar(value="10")
        self.duration_entry = ttk.Entry(main_frame, textvariable=self.duration_var, width=10)
        self.duration_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 速率限制
        ttk.Label(main_frame, text="請求速率限制:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.rate_var = tk.StringVar(value="0")
        self.rate_entry = ttk.Entry(main_frame, textvariable=self.rate_var, width=10)
        self.rate_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # 參數文件
        ttk.Label(main_frame, text="GET參數文件:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.params_var = tk.StringVar()
        self.params_entry = ttk.Entry(main_frame, textvariable=self.params_var, width=40)
        self.params_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="瀏覽", command=lambda: self.browse_file(self.params_var)).grid(row=4, column=2, padx=5)
        
        # Headers文件
        ttk.Label(main_frame, text="Headers文件:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.headers_var = tk.StringVar()
        self.headers_entry = ttk.Entry(main_frame, textvariable=self.headers_var, width=40)
        self.headers_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="瀏覽", command=lambda: self.browse_file(self.headers_var)).grid(row=5, column=2, padx=5)
        
        # 進度條框架
        progress_frame = ttk.LabelFrame(main_frame, text="測試進度", padding="5")
        progress_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 進度條
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate', variable=self.progress_var)
        self.progress.grid(row=0, column=0, pady=5)
        
        # 進度百分比標籤
        self.progress_label = ttk.Label(progress_frame, text="0%")
        self.progress_label.grid(row=0, column=1, padx=5)
        
        # 開始按鈕
        self.start_button = ttk.Button(main_frame, text="開始測試", command=self.start_test)
        self.start_button.grid(row=7, column=0, columnspan=3, pady=10)
        
        # 狀態標籤
        self.status_label = ttk.Label(main_frame, text="就緒")
        self.status_label.grid(row=8, column=0, columnspan=3, pady=5)

    def update_progress(self, current_time, total_time):
        progress = (current_time / total_time) * 100
        self.progress_var.set(progress)
        self.progress_label.config(text=f"{progress:.1f}%")
        self.root.update_idletasks()
        
    def start_test(self):
        # 獲取輸入值
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("錯誤", "請輸入目標URL")
            return
            
        try:
            threads = int(self.threads_var.get())
            duration = int(self.duration_var.get())
            rate_limit = int(self.rate_var.get())
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")
            return
            
        # 禁用開始按鈕
        self.start_button.state(['disabled'])
        self.status_label.config(text="測試進行中...")
        
        # 重置進度條
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        
        # 創建配置
        config = Config(
            url=url,
            threads=threads,
            duration=duration,
            rate_limit=rate_limit,
            params_file=self.params_var.get() or None,
            headers_file=self.headers_var.get() or None
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
        
    def test_completed(self):
        self.start_button.state(['!disabled'])
        self.status_label.config(text="測試完成！請查看報告文件。")
        messagebox.showinfo("完成", "測試已完成，報告已生成")
        
    def test_failed(self, error_message):
        self.start_button.state(['!disabled'])
        self.status_label.config(text="測試失敗")
        messagebox.showerror("錯誤", f"測試過程中發生錯誤：{error_message}")
        
    def browse_file(self, var):
        filename = filedialog.askopenfilename()
        if filename:
            var.set(filename)

def main():
    root = tk.Tk()
    app = WAFTesterGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main() 