---
title: "Windows 安裝 Hermes Agent 完整教學（WSL2 + Ubuntu + Hyper-V + Hermes 設定）"
date: 2026-05-27
category: hermes-agent
tags: ["Hermes", "Windows", "WSL2", "Ubuntu", "Hyper-V", "安裝教學"]
keywords: ["Hermes Agent", "WSL2 安裝", "Windows Ubuntu", "Hermes setup", "Hermes config"]
description: "從 BIOS 開啟虛擬化、Windows 啟用 Hyper-V 與 WSL2、安裝 Ubuntu，到 Hermes Agent 安裝、模型設定、Gateway 設定與常見故障排除的完整一步步教學。"
hackmd_url: ""
---

> 更新時間：2026-05-27 19:48 CST  
> 這篇是給 **Windows 使用者** 的從零教學，目標是把 Hermes Agent 穩定跑在 **WSL2 Ubuntu** 裡。

# 你會完成什麼

完成後你會有：

1. Windows 已啟用虛擬化（BIOS/UEFI）
2. Windows 已啟用 WSL2 / Hyper-V 相關元件
3. Ubuntu（WSL2）可正常使用
4. Hermes Agent 可在 Ubuntu 裡執行
5. 已完成 model/provider 設定（可對話、可用工具）
6. （可選）已完成 Discord/Telegram 等 Gateway 設定

---

# 0) 先確認需求

- 作業系統：Windows 10（建議 22H2）或 Windows 11
- 權限：需有系統管理員權限（部分步驟要 Administrator）
- 網路：可連 GitHub 與模型供應商 API

建議資源（最低可跑，建議更高）：
- RAM：16GB+
- SSD 可用空間：10GB+

---

# 1) 在 BIOS / UEFI 開啟虛擬化

WSL2 需要 CPU 虛擬化功能。

1. 重新開機進 BIOS / UEFI（常見按鍵：Del / F2 / F10 / Esc）
2. 找到以下選項並啟用：
   - Intel：**Intel Virtualization Technology (VT-x)**
   - AMD：**SVM Mode / AMD-V**
3. 儲存並重開機

> 若這步沒開，後續 WSL2 可能出現虛擬機平台錯誤。

---

# 2) 在 Windows 啟用必要元件（WSL2 / Hyper-V / VM Platform）

用 **系統管理員 PowerShell** 執行。

## 2.1 一鍵安裝 WSL（推薦）

```powershell
wsl --install
```

執行後通常會：
- 自動啟用必要元件
- 安裝 Linux 核心
- 安裝 Ubuntu

完成後請重開機。

## 2.2 若一鍵安裝失敗：手動啟用功能

```powershell
dism /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
dism /online /enable-feature /featurename:Microsoft-Hyper-V-All /all /norestart
```

然後重開機。

> Home 版通常重點是 WSL + VirtualMachinePlatform；Pro/Enterprise 常見會同時用到 Hyper-V。本文將 Hyper-V 一起納入，兼容多數企業環境。

---

# 3) 設定 WSL2 為預設版本並安裝 Ubuntu

在 PowerShell：

```powershell
wsl --set-default-version 2
wsl --install -d Ubuntu
```

查看狀態：

```powershell
wsl -l -v
```

你應該看到 Ubuntu，且 VERSION 為 2。

---

# 4) 初次進入 Ubuntu：建立 Linux 使用者 + 基礎更新

從開始功能表開啟 Ubuntu，第一次會要求建立 Linux 帳號與密碼。

接著在 Ubuntu 執行：

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git build-essential
```

---

# 5) 安裝 Hermes Agent

在 Ubuntu（WSL2）執行官方安裝腳本：

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

安裝後測試：

```bash
hermes --version
```

如果出現 `command not found`，先重新開一個 Ubuntu shell 再試一次。

---

# 6) 初始化 Hermes（重點設定）

## 6.1 互動式設定精靈

```bash
hermes setup
```

建議至少完成：
- model/provider
- terminal backend（一般保持 local）
- gateway（若要接 Discord/Telegram）

## 6.2 選模型

```bash
hermes model
```

依需求選擇 provider（例如 OpenRouter / Anthropic / OpenAI Codex / 其他）。

## 6.3 設定憑證（API Key / OAuth）

```bash
hermes auth
```

也可以用指令新增特定 provider：

```bash
hermes auth add <provider>
```

## 6.4 檢查健康狀態

```bash
hermes doctor
```

若有問題，先修到 doctor 不報紅字再往下。

---

# 7) 先做最小驗證（確認可用）

## 7.1 單句測試

```bash
hermes chat -q "請用一句話自我介紹"
```

## 7.2 互動模式

```bash
hermes
```

進入後可測：
- `/help`
- `/model`
- `/tools`

---

# 8) （可選）設定 Gateway（Discord / Telegram 等）

如果你要在聊天平台裡使用 Hermes：

```bash
hermes gateway setup
hermes gateway install
hermes gateway start
hermes gateway status
```

常用排錯：

```bash
tail -n 200 ~/.hermes/logs/gateway.log
```

---

# 9) 常見錯誤與排除

## 錯誤 A：WSL 啟不來 / 需要 Virtual Machine Platform

處理方式：
1. 確認 BIOS 已開虛擬化
2. 確認 `VirtualMachinePlatform` 已啟用
3. 重開機後再試 `wsl --status`

## 錯誤 B：`wsl -l -v` 不是 VERSION 2

```powershell
wsl --set-version Ubuntu 2
```

## 錯誤 C：Hermes 安裝後指令找不到

1. 關閉並重開 Ubuntu
2. 檢查 shell PATH
3. 重新跑安裝腳本一次

## 錯誤 D：模型 401 / 403 或無模型可用

1. 重新跑 `hermes auth`
2. `hermes model` 重新指定 provider / model
3. `hermes doctor` 檢查設定

## 錯誤 E：Gateway 沒反應

1. `hermes gateway status`
2. 看 `~/.hermes/logs/gateway.log`
3. 平台端權限（例如 Discord intents）要正確

---

# 10) 建議的日常操作

- 啟動互動：`hermes`
- 快速單問：`hermes chat -q "問題"`
- 更新設定：`hermes config edit`
- 查看工具：`hermes tools list`
- 更新 Hermes：`hermes update`

---

# 11) 安全建議（一定要做）

1. API Keys 只放在 `~/.hermes/.env` 或 `hermes auth` 管理，不要寫進程式碼倉庫
2. 若是公司電腦，請遵循內部資安規範
3. 啟用對高風險命令的審批（預設 manual）

---

# 12) 一條龍安裝流程（快速版）

## Windows PowerShell（管理員）

```powershell
wsl --install
wsl --set-default-version 2
wsl --install -d Ubuntu
```

## Ubuntu（WSL2）

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git build-essential
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
hermes model
hermes auth
hermes doctor
hermes
```

---

# 結語

以上完成後，你的 Hermes 會以「Windows + WSL2 Ubuntu」的最穩定路徑運行。  
如果你下一步要做的是「接 Discord、排程、技能化工作流程」，可以直接從 `hermes gateway setup`、`hermes cron`、`hermes skills` 開始。