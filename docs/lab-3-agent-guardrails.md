# Lab 3｜End-to-End Agent Guardrails

**時間：**35 分鐘
**目標：**將 Agent context、environment setup、deterministic validation、
CI / CodeQL 與 Repository Ruleset 串成從 prompt 到 governed merge 的完整控制鏈。

## 前置條件

- 具備 repository admin 權限
- CI `validate` job 至少成功執行一次
- CodeQL `analyze` job 至少成功執行一次
- Repository 已啟用 Code Scanning

請使用學員自己的 workshop repository。未經核准，不得在 production repository
或共用 organization 修改規則。

## 1. 理解完整 Guardrail Chain

| 階段 | Repository artifact | 用途 |
|---|---|---|
| Context | `.github/copilot-instructions.md` | Always-on project rules 與 validation commands |
| Domain workflow | `.github/skills/secure-fastapi-endpoint/SKILL.md` | 可重複使用的 secure endpoint procedure |
| Environment | `.github/workflows/copilot-setup-steps.yml` | 固定 cloud-agent runtime 與 dependencies |
| Agent validation | `.github/hooks/validate-on-stop.json` | Agent 嘗試停止時，阻擋含有本機驗證失敗的結果 |
| Pull Request checks | `.github/workflows/ci.yml`、`codeql.yml` | 產生獨立的 CI 與 security evidence |
| Merge governance | Repository Ruleset | 防止 contributor 或 Agent 繞過 required checks |

內層 guardrails 改善 Agent 行為；外層 guardrails 即使在 Agent 忽略指引或產生錯誤
修改時，仍能強制執行 repository policy。

## 2. 新增一條 ASUS Team Rule

選擇一個具體且可驗證的改善：

1. 在 `.github/copilot-instructions.md` 新增 repository rule。
2. 在 secure endpoint skill 新增必要的 review step。
3. 在 `scripts/validate.py` 加入既有且快速的檢查。

避免使用「請寫高品質程式碼」等空泛指引。有效規則應描述可觀察的 invariant 或
精確的 validation command。

## 3. 驗證 Agent-Level Guardrail

執行：

```bash
python scripts/validate.py --fast
echo '{}' | python scripts/agent_stop_hook.py
```

Repository 狀態正常時應回傳：

```json
{"decision": "allow"}
```

暫時將 `app/main.py` 的 health response 改壞，再次執行 hook，確認它回傳
`block` 與 test evidence。繼續下一步前，請先還原正常實作。

## 4. 建立 Repository Merge Gate

開啟：

```text
Repository Settings > Rules > Rulesets > New ruleset > New branch ruleset
```

設定：

| Setting | Value |
|---|---|
| Ruleset name | `ai-agent-main-guardrail` |
| Enforcement status | `Active` |
| Target branches | Include default branch |
| Require a pull request before merging | Enabled |
| Required approvals | 個人操作設為 `0`；兩人一組設為 `1` |
| Require status checks to pass | Enabled |
| Required checks | `validate`、`analyze` |
| Block force pushes | Enabled |
| Restrict deletions | Enabled |

不要將自己或 Coding Agent 加入 bypass list。

## 5. 執行 Agent to Governed Merge 流程

1. 建立 branch `lab3/end-to-end-guardrails`。
2. 將 health response 從 `"ok"` 改為 `"ruleset-demo"`，建立 Pull Request。
3. 確認 `validate` 失敗，且 Ruleset 阻止 merge。
4. 要求 Coding Agent：

```text
Restore the documented health-check behavior. Add no new feature.
Run the targeted test and repository validation before updating this PR.
```

5. 自行驗證 diff，不要直接接受 Agent 結果。
6. 僅在 `validate` 與 `analyze` 通過後 merge；兩人一組時需先取得 approval。

## 完成條件

- [ ] Team rule 具體且可驗證。
- [ ] Healthy code 時 hook 回傳 `allow`，test failure 時回傳 `block`。
- [ ] Direct change 或 failing PR 無法繞過 Repository Ruleset。
- [ ] Coding Agent 修復 PR，所有 required checks 通過。
- [ ] 最終 merge 遵循 governed path。

## 討論

```text
Instructions / Skills
        ↓
Setup Steps → Agent Change → Stop Hook
        ↓
Pull Request → CI + CodeQL
        ↓
Repository Ruleset → Human Approval → Merge
```

- Instructions 與 Skills 影響 model judgment。
- Setup steps 與 hooks 讓執行結果可重複。
- CI 與 CodeQL 提供獨立 evidence。
- Ruleset 對 Agent 與人工 contributor 一視同仁。
- Human owner 仍負責架構、產品行為、風險接受與最終 approval。
