# Actual execution evidence

Final native workflow status: **PASS**. The runner starts real Uvicorn and production Next.js servers, uses native Chromium navigation/fetch, and performs no fetch interception, exposed Python browser bridge or prerecorded answers.

`evidence/native_final/report.json` records ten newly authored privacy-safe invoice files, four API simulator completions, duplicate readback, actual model-unavailable 503, a real public-reference response or truthful 503, and database/receipt/balance readback after an actual server process restart. `evidence/clean/native_execution/` is the separate clean-extraction run when present.

Both UI variants create a new local student account, log in, create a case, upload a new invoice, extract/investigate, calculate a synthetic quote, explicitly approve and execute the internal simulator. Next.js also shows a conflicting invoice with quote controls disabled and an unavailable live agent. Desktop and 390-pixel mobile layouts switch en/zh-CN/bn-BD. API network logs record only paths and statuses, never cookies/passwords.

Screenshots show the actual running software with synthetic inputs. `next_transfer_status.png`, `next_conflict_details.png`, `next_agent_unavailable.png` and locale screenshots are derived from those interactions. They support, but do not independently replace, network and persisted-state assertions.

Legacy browser regression: six tests use an explicit Python HTTP bridge and are classified separately. Earlier native attempts failed because of selector assumptions and actual /demo deep-link/mobile defects. Their failure reports remain under `native_execution_attempt*`; only PASS reports count as acceptance.

No real transaction, real bank statement, real provider response ID or Qwen response was manufactured. Internal references start `SIM-` and are local simulator identifiers.

Resumed clean verification (2026-10-20): see [current acceptance](RESUMED_ACCEPTANCE_20261020.md) and `evidence/recovery_20261020/`. Earlier measurements above are preserved with their original scope.
