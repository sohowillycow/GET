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

By using this WAF Testing Tool (hereinafter referred to as "the Tool"), you must read, understand, and agree to the following disclaimer. If you do not agree with any part of this disclaimer, please do not use this Tool.

1. **Authorized Use Only**
   - This Tool is intended solely for legitimate security testing and research purposes
   - Testing must only be conducted with explicit authorization from system owners
   - Unauthorized testing is illegal and may result in severe legal consequences
   - Users must obtain and maintain proper documentation of authorization

2. **Risk Warning**
   - This Tool may cause adverse effects on target systems, including but not limited to:
     * Service interruption
     * Performance degradation
     * System instability
   - Users must evaluate and accept all risks associated with using this Tool
   - Testing should be conducted in appropriate test environments when possible

3. **Liability Limitations**
   - The developers and contributors of this Tool shall not be liable for:
     * Any direct or indirect damages
     * Data loss or corruption
     * Service interruptions
     * Legal consequences
     * Any other damages or losses arising from the use of this Tool

4. **Legal Compliance**
   - Users must comply with all applicable local, national, and international laws
   - The Tool must not be used for any illegal purposes
   - Users are responsible for understanding and following relevant regulations
   - Any illegal use is strictly prohibited and automatically voids any rights to use the Tool

5. **Prohibited Uses**
   - Attacking unauthorized systems
   - Malicious destruction or disruption
   - Any form of illegal activities
   - Testing systems without proper authorization
   - Using the Tool to cause intentional harm

6. **No Warranty**
   - The Tool is provided "AS IS" without any warranty of any kind
   - No guarantee of:
     * Merchantability
     * Fitness for a particular purpose
     * Accuracy of results
     * Error-free operation
     * Meeting specific requirements

7. **User Responsibility**
   - Users are solely responsible for:
     * All actions taken using this Tool
     * Consequences of their testing activities
     * Maintaining proper authorization
     * Protecting test data and results
     * Reporting security issues responsibly

Using this Tool indicates your acceptance of all terms in this disclaimer. If you disagree with any terms, you must not use this Tool.

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

使用本 WAF 測試工具（以下簡稱"本工具"）前，您必須仔細閱讀、理解並同意以下免責聲明。如果您不同意本聲明的任何部分，請勿使用本工具。

1. **授權使用要求**
   - 本工具僅供合法的安全測試和研究使用
   - 必須在獲得系統所有者的明確授權後才能進行測試
   - 未經授權的測試行為屬於非法，可能導致嚴重的法律後果
   - 使用者必須獲得並保存適當的授權文件

2. **風險警示**
   - 本工具可能對目標系統造成的負面影響包括但不限於：
     * 服務中斷
     * 性能下降
     * 系統不穩定
   - 使用者必須評估並接受使用本工具的所有風險
   - 建議在適當的測試環境中進行測試

3. **責任限制**
   - 本工具的開發者和貢獻者不對以下情況承擔責任：
     * 任何直接或間接損害
     * 數據丟失或損壞
     * 服務中斷
     * 法律後果
     * 因使用本工具導致的任何其他損害或損失

4. **法律合規**
   - 使用者必須遵守所有適用的地方、國家和國際法律
   - 本工具不得用於任何非法目的
   - 使用者有責任理解並遵守相關法規
   - 任何非法使用都將自動喪失使用本工具的權利

5. **禁止的用途**
   - 攻擊未經授權的系統
   - 惡意破壞或干擾
   - 任何形式的違法活動
   - 未經適當授權的測試
   - 使用本工具造成蓄意傷害

6. **無擔保聲明**
   - 本工具按"原樣"提供，不提供任何形式的擔保
   - 不保證：
     * 適銷性
     * 特定用途的適用性
     * 結果的準確性
     * 無錯誤運行
     * 滿足特定需求

7. **使用者責任**
   - 使用者對以下方面負有完全責任：
     * 使用本工具進行的所有行為
     * 測試活動的後果
     * 維護適當的授權
     * 保護測試數據和結果
     * 負責任地報告安全問題

使用本工具即表示您接受本免責聲明的所有條款。如果您不同意任何條款，則必須停止使用本工具。

## 許可證

[MIT License](LICENSE)

## 貢獻

歡迎提交 Issue 和 Pull Request。