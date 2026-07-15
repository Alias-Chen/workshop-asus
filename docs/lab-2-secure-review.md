# Lab 2｜CodeQL 與 Copilot Code Review

**時間：**30 分鐘
**目標：**建立刻意含有弱點的 Pull Request，區分工具 finding 與人工決策，再指派
Coding Agent 修復確認的問題。

> 本 Lab 包含刻意設計的不安全程式碼，僅限在此 sample repository 中操作。

## 1. 建立獨立的弱點 Branch

從乾淨且最新的 `main` 開始：

```bash
git switch main
git pull
git switch -c lab2-insecure-report
python scripts/prepare_lab2.py
git diff
python scripts/validate.py
```

Review diff 後 commit、push，並建立合併至 `main` 的 Pull Request。
Script 不會自動 commit 或 push。

產生的 endpoint：

```text
GET /reports/sales?category=Laptop&formula=total
```

## 2. 等待不同來源的 Review 訊號

1. 開啟 PR 的 **Checks** 頁籤，等待 CodeQL 完成。
2. 若權限允許，開啟 repository 的 **Security > Code scanning**。
3. 從 PR reviewer 選單要求 Copilot Code Review。
4. 在要求 Agent 修復前，先自行閱讀程式碼。

預期 CodeQL 可偵測 user-controlled SQL construction 與 dynamic code execution。
Code Review 也應討論 validation、exception handling、stack trace disclosure、
test coverage 與 maintainability。不是每一則 review comment 都是 CodeQL finding。

## 3. 修復前先進行 Triage

在 PR description 或 comment 記錄每一項結果：

| Finding | 來源 | 分類 | Evidence / 決策 |
|---|---|---|---|
| 範例：SQL injection | CodeQL | Confirmed - must fix | Request input 進入 interpolated SQL query |

僅使用以下分類：

- **Confirmed - must fix**
- **Needs human decision**
- **Not applicable / false positive**

## 4. 建立 Remediation Issue

使用 **Lab 2: Security remediation** template 建立 Issue，並連結弱點 PR。
將 Issue 指派給 Copilot coding agent，或要求 Agent 更新既有 PR。

Review Agent 是否：

- 使用 SQLite parameter binding，而非過濾危險字元。
- 完全移除 dynamic Python execution，而非建立 expression blacklist。
- 回傳穩定且不包含 stack trace 的 public error。
- 新增針對 exploit 的 regression tests。
- 沒有關閉 CodeQL 或忽略 review comments。

## 5. 驗證修復

```bash
python scripts/validate.py
```

透過 Swagger UI 測試正常行為與代表性 attack inputs。確認更新後的 CodeQL 與 CI
皆為 green，再根據實際程式碼結果 resolve review threads。

## 完成條件

- [ ] Findings 已附上 evidence 並完成分類。
- [ ] SQL injection、dynamic execution 與 error disclosure 已修復。
- [ ] Regression tests 能證明原始攻擊無法再次成功。
- [ ] CI 與 CodeQL 皆通過。
- [ ] PR summary 說明修復內容與 residual risk。

## Hosted Feature 無法使用時

- CodeQL 無法使用：改用講師提供的 expected findings，繼續完成 triage。
- Copilot Code Review 沒有產生 comment：在 Copilot Chat 使用：

```text
Review app/routers/reports.py for exploitable security issues, correctness problems,
error disclosure, and missing regression tests. Cite the affected lines and do not edit yet.
```

若尚未 commit，可使用以下指令還原 Lab 2 preparation：

```bash
python scripts/prepare_lab2.py --reset
```
