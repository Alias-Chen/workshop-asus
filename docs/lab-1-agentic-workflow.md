# Lab 1｜使用 Copilot Coding Agent 完成 Issue to PR

**時間：**35 分鐘
**目標：**將資訊不足的需求改寫成可驗證的 Issue，監督 Coding Agent 產生可供
Review 的 Pull Request。

## 1. 確認 Starter 狀態正常

```bash
python scripts/preflight.py
python scripts/validate.py
```

在 Swagger UI 開啟 `/products`，確認目前 API response。

## 2. 建立並改善 Issue

使用 **Lab 1: Product search** template 建立 Issue。Template 的初始描述刻意不完整，
請補上以下需求：

### API 行為

`GET /products` 接受以下 optional query parameters：

| Parameter | 規則 |
|---|---|
| `q` | 對產品名稱或分類執行不區分大小寫的 partial match |
| `sort` | 僅允許 `name` 或 `price`；無效值回傳 HTTP 422 |
| `order` | 僅允許 `asc` 或 `desc`；預設 `asc`；無效值回傳 HTTP 422 |
| `page` | 大於或等於 1 的整數；預設 1 |
| `page_size` | 1 到 20 的整數；預設 20 |

Response 必須維持既有的 `items`、`total`、`page`、`page_size` shape。
`total` 代表分頁前的符合筆數。搜尋、排序與分頁必須能組合使用。
既有的 `GET /products/{product_id}` 行為不得改變。

### 必須通過的驗證

```bash
python scripts/validate.py
pytest -q -m lab1
```

將上述規則改寫成逐項可驗證的 acceptance criteria。

## 3. 指派 Coding Agent

1. 將 Issue 指派給 Copilot coding agent。
2. 開啟 Agent session log。
3. 確認 plan 是否包含 input validation、filter / sort / pagination 的執行順序、
   相容性與測試。
4. 不要因實作方式與預期不同就立即介入；只有在 acceptance criteria 或
   safety constraint 遺漏時才要求修正。

## 4. Review Pull Request

- [ ] Diff 僅包含需求必要的修改。
- [ ] Query parameters 使用 FastAPI / Pydantic constraints，而非手動字串判斷。
- [ ] `total` 在 pagination slicing 前計算。
- [ ] 既有 tests 通過。
- [ ] `pytest -q -m lab1` 通過。
- [ ] CI 偵測到 product router 修改並執行 Lab 1 acceptance tests。
- [ ] CI 為 green。
- [ ] PR summary 說明 assumptions 與執行過的 commands。

若結果不完整，請使用 evidence 與明確預期回饋 Agent，例如：

```text
Combined search + sorting + pagination acceptance test still fails.
Keep total as the pre-pagination match count and add a regression test before updating the PR.
```

## 完成條件

- [ ] Issue 包含完整 context、constraints、acceptance criteria 與 validation commands。
- [ ] Coding Agent 建立 Pull Request。
- [ ] 所有 baseline 與 Lab 1 tests 通過。
- [ ] PR 已由學員完成 diff 與 assumption review。

## 討論

比較原始的一行 Issue 與最終 Issue：哪一項新增資訊最明顯改變 Agent 的 plan 或實作？

若 Issue 遺漏 category search 等規則，對應的 acceptance test 應該失敗。請將失敗視為
改善需求的 evidence，而不是降低測試標準。
