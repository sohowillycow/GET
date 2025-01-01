# WAF Testing Tool / WAF 測試工具

[English](#english) | [中文](#中文)

# English

This is a stress testing tool for Web Application Firewall (WAF), supporting both command-line and graphical user interfaces.

## Features

- **Dual Interface**
  - Command Line Interface (CLI): Suitable for automated testing and script integration
  - Graphical User Interface (GUI): Provides a user-friendly visual environment

- **Core Functions**
  - Support for HTTP/HTTPS GET request testing
  - Configurable concurrent threads (1-100 threads)
  - Adjustable test duration (1-3600 seconds)
  - Request rate limiting (0-1000 requests/second)
  - Custom GET parameters and Headers support
  - Real-time test progress display

- **Parameter Configuration**
  - URL: Supports HTTP and HTTPS protocols
  - Thread Count: Controls the number of concurrent requests
  - Duration: Sets the test running time
  - Rate Limit: Controls requests per second
  - GET Parameters File: Supports .json and .txt formats
  - Headers File: Supports .json format

- **Result Analysis**
  - Generates detailed test reports (waf_test_report.txt)
  - Generates response time distribution graph (response_time_distribution.png)
  - Generates request status distribution graph (status_distribution.png)
  - Exports detailed test data (detailed_results.csv)

## Testing Ethics

- **Authorization Requirements**
  - Must obtain explicit authorization from the target system administrator before testing
  - Need to sign relevant testing agreements and non-disclosure agreements
  - Strictly comply with testing scope and limitations

- **Responsibilities**
  - Testers are responsible for all testing activities
  - Avoid causing any form of damage to the target system
  - Ensure normal system operation and other users' usage are not affected

- **Security Principles**
  - All test data must be properly managed and securely destroyed after testing
  - Do not disclose any sensitive information obtained during testing
  - Immediately notify relevant personnel when security vulnerabilities are discovered

## Recommended Testing Process

1. **Preparation Phase**
   - Set up testing environment
   - Confirm testing authorization and scope
   - Prepare test data and parameter configurations

2. **Initial Testing**
   - Conduct small-scale tests in the testing environment
   - Verify tool configuration correctness
   - Adjust basic parameter settings

3. **Performance Testing**
   - Gradually increase concurrency (recommended starting from 10)
   - Incrementally extend test duration
   - Observe and record WAF performance

4. **Attack Testing**
   - Simulate common Web attack scenarios
   - Test WAF detection and blocking capabilities
   - Evaluate false positives and false negatives

5. **Result Analysis**
   - Analyze test reports and charts
   - Evaluate overall WAF performance
   - Propose optimization suggestions

6. **Follow-up Improvements**
   - Adjust WAF configuration based on test results
   - Optimize rule settings
   - Conduct verification testing

## Requirements

```bash
pip install -r requirements.txt
```

Required dependencies:
- requests>=2.31.0
- aiohttp>=3.9.1
- asyncio>=3.4.3
- click>=8.1.7
- rich>=13.7.0
- pandas>=2.1.4
- matplotlib>=3.8.2
- tk>=0.1.0 (Required for GUI mode)

## Usage

### GUI Mode

Run the following command to start the graphical interface:

```bash
python gui.py
```

In the GUI:
1. Enter target URL (must start with http:// or https://)
2. Set concurrent threads (1-100)
3. Set test duration (1-3600 seconds)
4. Set request rate limit (0-1000, 0 means no limit)
5. Optional: Select GET parameters file (.json or .txt)
6. Optional: Select Headers file (.json)
7. Click "Start Test" button to begin testing

### Command Line Mode

```bash
python main.py --url TARGET_URL [OPTIONS]

Options:
  --url TEXT          Target URL (required)
  --threads INTEGER   Concurrent threads (default: 10)
  --duration INTEGER  Test duration (seconds) (default: 10)
  --rate-limit INTEGER  Request rate limit (default: 0, no limit)
  --params TEXT       GET parameters list file path
  --headers TEXT      Custom Headers file path
  --help             Show help information
```

## Input File Formats

### GET Parameters File
- JSON format example:
```json
[
    {"param1": "value1"},
    {"param2": "value2"}
]
```
- TXT format example:
```text
param1=value1
param2=value2
```

### Headers File
- JSON format example:
```json
{
    "User-Agent": "Custom-Agent",
    "Accept": "application/json"
}
```

## Output Files

1. **waf_test_report.txt**: Contains test summary information
   - Test time
   - Duration
   - Concurrent threads
   - Request statistics (total, successful, blocked, errors)
   - Average response time

2. **response_time_distribution.png**: Response time distribution graph

3. **status_distribution.png**: Request status code distribution graph

4. **detailed_results.csv**: Detailed request records
   - Timestamp
   - Status code
   - Response time
   - Request parameters
   - Headers information

## Notes

1. Ensure you have proper testing authorization before use
2. Recommended to test in a testing environment first
3. Set reasonable concurrent threads and rate limits to avoid overwhelming target servers
4. Ensure test duration and thread count are within reasonable ranges

## Development Information

- Language: Python 3
- Main Dependency: aiohttp (Async HTTP client)
- GUI Framework: tkinter
- Chart Generation: matplotlib
- Data Processing: pandas

## Disclaimer

This tool is provided "as is" without warranty of any kind, either expressed or implied. By using this tool, you agree that:

1. **Usage Responsibility**: You are solely responsible for how you use this tool and any consequences that may arise from its use.

2. **No Liability**: The developers and contributors of this tool shall not be liable for any damages, including but not limited to:
   - Direct or indirect damage to target systems
   - Data loss or corruption
   - Service interruption
   - Any other damages resulting from the use of this tool

3. **Legal Compliance**: Users must:
   - Comply with all applicable laws and regulations
   - Obtain necessary permissions before testing
   - Use this tool only for legitimate security testing purposes

4. **No Guarantee**: The developers do not guarantee that:
   - The tool will meet your specific requirements
   - The tool will be error-free
   - Results will be accurate or reliable

5. **Intended Use**: This tool is designed for security professionals and system administrators to test their own systems or systems they have permission to test.

## License

[MIT License](LICENSE)

## Contributing

Issues and Pull Requests are welcome.

---

# 中文

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

## 測試倫理

- **授權要求**
  - 必須在獲得目標系統管理員的明確授權後才能進行測試
  - 需簽署相關的測試協議和保密協議
  - 嚴格遵守測試範圍和限制條件

- **責任義務**
  - 測試者需對所有測試行為負責
  - 避免對目標系統造成任何形式的損害
  - 確保不影響系統的正常運行和其他用戶的使用

- **安全原則**
  - 所有測試數據必須妥善保管並在測試後安全銷毀
  - 不得洩露任何在測試過程中獲得的敏感信息
  - 發現安全漏洞時應立即通知相關負責人

## 建議測試流程

1. **準備階段**
   - 搭建測試環境
   - 確認測試授權和範圍
   - 準備測試數據和參數配置

2. **初步測試**
   - 在測試環境中進行小規模測試
   - 驗證工具配置是否正確
   - 調整基本參數設置

3. **性能測試**
   - 逐步增加並發數（建議從 10 開始）
   - 逐漸延長測試持續時間
   - 觀察並記錄 WAF 的性能表現

4. **攻擊測試**
   - 模擬常見的 Web 攻擊場景
   - 測試 WAF 的檢測和攔截能力
   - 評估誤報和漏報情況

5. **結果分析**
   - 分析測試報告和圖表
   - 評估 WAF 的整體表現
   - 提出優化建議

6. **後續改進**
   - 根據測試結果調整 WAF 配置
   - 優化規則設置
   - 進行驗證性測試

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

## 免責聲明

本工具按"原樣"提供，不提供任何形式的明示或暗示保證。使用本工具即表示您同意：

1. **使用責任**：您對使用本工具的方式及由此產生的任何後果承擔全部責任。

2. **免責條款**：本工具的開發者和貢獻者不對以下情況承擔任何責任：
   - 對目標系統的直接或間接損害
   - 數據丟失或損壞
   - 服務中斷
   - 因使用本工具導致的任何其他損害

3. **法律合規**：使用者必須：
   - 遵守所有適用的法律法規
   - 在測試前獲得必要的許可
   - 僅將本工具用於合法的安全測試目的

4. **無保證**：開發者不保證：
   - 本工具將滿足您的特定需求
   - 本工具完全無錯誤
   - 結果完全準確或可靠

5. **預期用途**：本工具專為安全專業人員和系統管理員設計，用於測試其自有系統或獲得授權的系統。

## 許可證

[MIT License](LICENSE)

## 貢獻

歡迎提交 Issue 和 Pull Request。