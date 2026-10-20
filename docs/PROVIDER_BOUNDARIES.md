# Provider connectivity and agent authority

## Actual integrations in V2

- `CAMPUS_SIM_A` and `CAMPUS_SIM_B`: locally defined, **fake** provider profiles, fixed synthetic FX rates, synthetic fee schedules and deterministic execution outcomes. No provider network call and no external account credit.
- `GET /finance/reference-fx`: optionally queries public Frankfurter read-only reference endpoint if internet access exists. That timestamped rate does not price an executable quote or authorize transfer.
- `POST /cases/{id}/copilot`: if all server-side `LLM_API_URL`, `LLM_MODEL`, and `LLM_API_KEY` are set, it can call an OpenAI-compatible JSON chat-completions endpoint to explain *structured* invoice fields. This adapter is not externally tested. LLM output is never passed to `approve()` or `execute()`.

## Not connected

Wise, Airwallex, Flywire, Convera, TransferMate, any bank and any blockchain wallet. No real sandbox credential has been used; no real transaction receipt, test hash or integration successful result is claimed.

## Required to safely extend

Use official current V2 (not deprecated V1) Wise sandbox documentation or Airwallex documentation, obtain developer authorization and credentials, implement typed adapter interfaces, verify official recipient registration capability and jurisdiction rules, bind credentials to server-only secret store, define timeout/duplicate/race/reconciliation behavior, test in staging with explicit owner permission and mark every response as sandbox/prod correctly. A passing internal simulator does not prove compatibility with a partner API.
