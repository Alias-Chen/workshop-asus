# ASUS AI Coding Agent Workshop

這是一個可直接執行的 Python + FastAPI Workshop repository，用來練習完整的
Agentic Software Development Workflow：

投影片：[ASUS AI Coding Agent Workshop](slides/ASUS-AI-Coding-Agent-Workshop.pptx)

```text
Issue → Copilot coding agent → Pull Request → CI
      → CodeQL + Copilot Code Review → Agent 修復
      → Repository Instructions + Agent Skill + Hook
      → Repository Ruleset → Governed Merge
```

## Workshop Labs

| Lab | 時間 | 學習產出 |
|---|---:|---|
| [Lab 1：Issue to PR](docs/lab-1-agentic-workflow.md) | 35 分鐘 | 透過 Coding Agent PR 完成產品搜尋、排序與分頁功能 |
| [Lab 2：Secure Review](docs/lab-2-secure-review.md) | 30 分鐘 | 分析 CodeQL / Code Review findings，修復不安全的 API endpoint |
| [Lab 3：End-to-End Agent Guardrails](docs/lab-3-agent-guardrails.md) | 35 分鐘 | 串接 Agent context、deterministic validation、CI / CodeQL 與 Repository Ruleset |

講師準備與時間配置請參考
[講師操作手冊](docs/instructor-runbook.md)。

## 本機環境設定

需要 Python 3.10 或更新版本。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate.py
uvicorn app.main:app --reload
```

Windows PowerShell 請使用以下指令啟用 virtual environment：

```powershell
.\.venv\Scripts\Activate.ps1
```

開啟：

- API：<http://127.0.0.1:8000/products>
- Swagger UI：<http://127.0.0.1:8000/docs>
- Health check：<http://127.0.0.1:8000/health>

## 驗證指令

```bash
python scripts/validate.py
pytest -q -m lab1
ruff check .
```

一般測試指令會排除初始狀態下刻意失敗的 Lab 1 acceptance tests。
執行 Lab 1 時，請使用 `pytest -q -m lab1` 驗證實作。

## Workshop 重要設定

- 使用 repository 內建的 CodeQL advanced setup workflow；請勿同時啟用
  CodeQL default setup。
- Repository 與學員帳號必須已啟用 Copilot coding agent。
- Workshop organization 必須允許 GitHub Actions 與 Copilot Code Review。
- Repository 必須啟用 Code Scanning，Lab 3 學員需具備 repository admin 權限。
- 本 repository 不使用真實 credentials 或 production data。

