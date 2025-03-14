# Enhanced Cursor Pro Activator

An enhanced version of the Cursor Pro Activator with additional features and improvements.

## 🌟 New Features

- Unified Google & GitHub OAuth Authentication
- Automatic Chrome Profile Detection
- Enhanced Browser Management
- Improved User Interface with Unique Menu Styling
- Automatic Browser Handling
- Smart Profile Selection
- Lifetime Access Support

## 🔄 Original Project

This project is based on the work by [mALIk-sHAHId](https://github.com/mALIk-sHAHId/cursor-free-vip). The original project provided the foundation for Cursor Pro activation.

## ✨ Enhancements Added

1. **Authentication System**
   - Added Google OAuth integration
   - Added GitHub OAuth integration
   - Automatic profile detection and management
   - Seamless authentication flow

2. **User Experience**
   - Enhanced menu interface
   - Clear user guidance
   - Improved error handling
   - Progress indicators
   - Automatic browser management

3. **Technical Improvements**
   - Unified authentication handling
   - Smart Chrome profile detection
   - Automatic cleanup
   - Better error recovery
   - Enhanced session management

## 🚀 Usage

1. Choose your preferred authentication method:
   - Google Account (Lifetime ACCESS)
   - GitHub Account (Lifetime ACCESS)
2. Follow the automatic authentication process
3. Enjoy Cursor Pro features!

## 📝 License

This project maintains the original license terms while adding new features and improvements.

## 🙏 Credits

- Original Project: [cursor-free-vip](https://github.com/mALIk-sHAHId/cursor-free-vip) by mALIk-sHAHId
- Enhanced by: [Your GitHub Username]

# ➤ Cursor Free VIP
<div align="center">
<p align="center">
  <img src="./images/logo.png" alt="Cursor Pro Logo" width="200" style="border-radius: 6px;"/>
</p>

<p align="center">

[![Release](https://img.shields.io/github/v/release/mALIk-sHAHId/cursor-free-vip?style=flat-square&logo=github&color=blue)](https://github.com/mALIk-sHAHId/cursor-free-vip/releases/latest)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC_BY--NC--ND_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
[![Stars](https://img.shields.io/github/stars/mALIk-sHAHId/cursor-free-vip?style=flat-square&logo=github)](https://github.com/mALIk-sHAHId/cursor-free-vip/stargazers)
[![Download](https://img.shields.io/github/downloads/mALIk-sHAHId/cursor-free-vip/total?style=flat-square&logo=github&color=52c41a)](https://github.com/mALIk-sHAHId/cursor-free-vip/releases/latest)

</p>
<h4>Support Latest 0.47.x Version | 支持最新0.47.x版本</h4>

This is a tool to automatically register , support Windows and macOS systems, complete Auth verification, and reset Cursor's configuration.

這是一個自動化工具，自動註冊 ，支持 Windows 和 macOS 系統，完成Auth驗證，重置Cursor的配置。

<p align="center">
  <img src="./images/new_2025-02-27_10-42-44.png" alt="new" width="400" style="border-radius: 6px;"/><br>
</p>

##### If you dont have google chrome , you can download it from [here](https://www.google.com/intl/en_pk/chrome/)

##### 如果沒有Google Chrome，可以從[這裡](https://www.google.com/intl/en_pk/chrome/)下載

</p>
</div>


## 🔄 Change Log | 更新日志
[Watch Change Log | 查看更新日志](CHANGELOG.md)

## ✨ Features | 功能特點

* Automatically register Cursor membership<br>自動註冊Cursor會員<br>

* Support Windows and macOS systems<br>支持 Windows 和 macOS 系統<br>

* Complete Auth verification<br>完成Auth驗證<br>

* Reset Cursor's configuration<br>重置Cursor的配置<br>


## 💻 System Support | 系統支持

|Windows|x64|✅|macOS|Intel|✅|
|:---:|:---:|:---:|:---:|:---:|:---:|
|Windows|x86|✅|macOS|Apple Silicon|✅|
|Linux|x64|✅|Linux|x86|✅|
|Linux|ARM64|✅|Linux|ARM64|✅|

## 👀 How to use | 如何使用

<details open>
<summary><b>⭐ Auto Run Script | 腳本自動化運行</b></summary>

**Linux/macOS**
```bash
curl -fsSL https://raw.githubusercontent.com/mALIk-sHAHId/cursor-free-vip/main/scripts/install.sh -o install.sh && chmod +x install.sh && ./install.sh
```

**Windows**
```powershell
irm https://raw.githubusercontent.com/mALIk-sHAHId/cursor-free-vip/main/scripts/install.ps1 | iex
```
</details>

<details>
<summary><b>⭐ Manual Reset Machine | 手動運行重置機器</b></summary>

**Linux/macOS**
```bash
curl -fsSL https://raw.githubusercontent.com/mALIk-sHAHId/cursor-free-vip/main/scripts/reset.sh | sudo bash
```

**Windows**
```powershell
irm https://raw.githubusercontent.com/mALIk-sHAHId/cursor-free-vip/main/scripts/reset.ps1 | iex
```
</details>

2. If you want to stop the script, please press Ctrl+C<br>要停止腳本，請按 Ctrl+C

## ❗ Note | 注意事項

📝 Config | 文件配置
`Win / Macos / Linux Path | 路徑 [Documents/.cursor-free-vip/config.ini]`
<details>
<summary><b>⭐ Config | 文件配置</b></summary>

```
[Chrome]
# Default Google Chrome Path | 默認Google Chrome 遊覽器路徑
chromepath = C:\Program Files\Google/Chrome/Application/chrome.exe

[Turnstile]
# Handle Tuenstile Wait Time | 等待人機驗證時間
handle_turnstile_time = 2
# Handle Tuenstile Wait Random Time (must merge 1-3 or 1,3) | 等待人機驗證隨機時間（必須是 1-3 或者 1,3 這樣的組合）
handle_turnstile_random_time = 1-3

[OSPaths]
# Storage Path | 存儲路徑
storage_path = /Users/username/Library/Application Support/Cursor/User/globalStorage/storage.json
# SQLite Path | SQLite路徑
sqlite_path = /Users/username/Library/Application Support/Cursor/User/globalStorage/state.vscdb
# Machine ID Path | 機器ID路徑
machine_id_path = /Users/username/Library/Application Support/Cursor/machineId

[Timing]
# Min Random Time | 最小隨機時間
min_random_time = 0.1
# Max Random Time | 最大隨機時間
max_random_time = 0.8
# Page Load Wait | 頁面加載等待時間
page_load_wait = 0.1-0.8
# Input Wait | 輸入等待時間
input_wait = 0.3-0.8
# Submit Wait | 提交等待時間
submit_wait = 0.5-1.5
# Verification Code Input | 驗證碼輸入等待時間
verification_code_input = 0.1-0.3
# Verification Success Wait | 驗證成功等待時間
verification_success_wait = 2-3
# Verification Retry Wait | 驗證重試等待時間
verification_retry_wait = 2-3
# Email Check Initial Wait | 郵件檢查初始等待時間
email_check_initial_wait = 4-6
# Email Refresh Wait | 郵件刷新等待時間
email_refresh_wait = 2-4
# Settings Page Load Wait | 設置頁面加載等待時間
settings_page_load_wait = 1-2
# Failed Retry Time | 失敗重試時間
failed_retry_time = 0.5-1
# Retry Interval | 重試間隔
retry_interval = 8-12
# Max Timeout | 最大超時時間
max_timeout = 160
```
</details>

* Use administrator to run the script <br>請使用管理員身份運行腳本

* Confirm that Cursor is closed before running the script <br>請確保在運行腳本前已經關閉 Cursor<br>

* This tool is only for learning and research purposes <br>此工具僅供學習和研究使用<br>

* Please comply with the relevant software usage terms when using this tool <br>使用本工具時請遵守相關軟件使用條款



## 🚨 Common Issues | 常見問題

|如果遇到權限問題，請確保：| 此腳本以管理員身份運行 |
|:---:|:---:|
|If you encounter permission issues, please ensure: | This script is run with administrator privileges |



## 🤩 Contribution | 貢獻

歡迎提交 Issue 和 Pull Request！


<a href="https://github.com/mALIk-sHAHId/cursor-free-vip/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=mALIk-sHAHId/cursor-free-vip" />
</a>
<br /><br />


## 📩 Disclaimer | 免責聲明

本工具僅供學習和研究使用，使用本工具所產生的任何後果由使用者自行承擔。 <br>

This tool is only for learning and research purposes, and any consequences arising from the use of this tool are borne by the user.

## 💰 Buy Me a Coffee | 請我喝杯咖啡

<div align="center">
  <table>
    <tr>
      <td>
        <img src="./images/provi-code.jpg" alt="buy_me_a_coffee" width="280"/><br>
      </td>
      <td>
        <img src="./images/paypal.png" alt="buy_me_a_coffee" width="280"/><br>
      </td>
    </tr>
  </table>
</div>

## ⭐ Star History | 星星數

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=mALIk-sHAHId/cursor-free-vip&type=Date)](https://star-history.com/#mALIk-sHAHId/cursor-free-vip&Date)

</div>

## 📝 License | 授權

本項目採用 [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) 授權。 
Please refer to the [LICENSE](LICENSE.md) file for details.




