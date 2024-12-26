# WAF 測試工具

這是一個用於測試 Web 應用防火牆（WAF）的壓力測試工具，支持命令行和圖形界面兩種使用方式。

## 功能特點

- **雙重操作界面**
  - 命令行界面 (CLI)：適合自動化測試和腳本集成
  - 圖形用戶界面 (GUI)：提供友好的可視化操作環境

- **核心功能**
  - 支持 HTTP/HTTPS GET 請求測試
  - 可配置並發線程數（1-100線程）
  - 可設置測試持續時間（1-3600秒）
  - 支持請求速率限制（0-1000次/秒）
  - 支持自定義 GET 參數和 Headers
  - 實時顯示測試進度

- **參數配置**
  - URL：支持 HTTP 和 HTTPS 協議
  - 並發線程數：控制同時發送請求的數量
  - 持續時間：設置測試運行的時長
  - 速率限制：控制每秒請求數量
  - GET 參數文件：支持 .json 和 .txt 格式
  - Headers 文件：支持 .json 格式

- **結果分析**
  - 生成詳細的測試報告（waf_test_report.txt）
  - 生成響應時間分佈圖（response_time_distribution.png）
  - 生成請求狀態分佈圖（status_distribution.png）
  - 導出詳細測試數據（detailed_results.csv）

## 安裝要求

```bash
pip install -r requirements.txt
```

必要的依賴包括：
- requests>=2.31.0
- aiohttp>=3.9.1
- asyncio>=3.4.3
- click>=8.1.7
- rich>=13.7.0
- pandas>=2.1.4
- matplotlib>=3.8.2
- tk>=0.1.0（GUI模式需要）

## 使用方法

### GUI 模式

運行以下命令啟動圖形界面：

```bash
python gui.py
```

在圖形界面中：
1. 輸入目標 URL（必須以 http:// 或 https:// 開頭）
2. 設置並發線程數（1-100）
3. 設置測試持續時間（1-3600秒）
4. 設置請求速率限制（0-1000，0表示無限制）
5. 可選：選擇 GET 參數文件（.json 或 .txt）
6. 可選：選擇 Headers 文件（.json）
7. 點擊"開始測試"按鈕開始測試

### 命令行模式

```bash
python main.py --url TARGET_URL [OPTIONS]

選項：
  --url TEXT          目標URL（必需）
  --threads INTEGER   並發線程數（默認：10）
  --duration INTEGER  測試持續時間（秒）（默認：10）
  --rate-limit INTEGER  請求速率限制（默認：0，無限制）
  --params TEXT       GET參數列表文件路徑
  --headers TEXT      自定義Headers文件路徑
  --help             顯示幫助信息
```

## 輸入文件格式

### GET 參數文件
- JSON 格式示例：
```json
[
    {"param1": "value1"},
    {"param2": "value2"}
]
```
- TXT 格式示例：
```text
param1=value1
param2=value2
```

### Headers 文件
- JSON 格式示例：
```json
{
    "User-Agent": "Custom-Agent",
    "Accept": "application/json"
}
```

## 輸出文件

1. **waf_test_report.txt**：包含測試摘要信息
   - 測試時間
   - 持續時間
   - 並發線程數
   - 請求統計（總數、成功、被阻擋、錯誤）
   - 平均響應時間

2. **response_time_distribution.png**：響應時間分佈圖

3. **status_distribution.png**：請求狀態碼分佈圖

4. **detailed_results.csv**：詳細的請求記錄
   - 時間戳
   - 狀態碼
   - 響應時間
   - 請求參數
   - Headers 信息

## 注意事項

1. 使用前請確保有適當的測試授權
2. 建議先在測試環境中進行測試
3. 合理設置並發數和速率限制，避免對目標服務器造成過大壓力
4. 確保測試時間和線程數在合理範圍內

## 開發信息

- 語言：Python 3
- 主要依賴：aiohttp（異步HTTP客戶端）
- GUI框架：tkinter
- 圖表生成：matplotlib
- 數據處理：pandas

## 許可證

[MIT License](LICENSE)

## 貢獻

歡迎提交 Issue 和 Pull Request。