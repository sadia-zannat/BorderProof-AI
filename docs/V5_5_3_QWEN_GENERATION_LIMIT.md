# V5.5.3 - Qwen generation-limit candidate

The user's real Windows Qwen3:4b validation on V5.5.2 returned HTTP 200 for L01, L03, L05, L07 and L09, but HTTP 502 for L02, L04, L06 and L08 with `Model reached generation limit; incomplete answer withheld`. No financial side effects were observed.

Changes:
- Increase Ollama num_predict from 900 to 1600 and transport timeout from 65 to 115 seconds. This can increase runtime and memory use.
- Deterministically project read-only tool data for model context while preserving the complete tenant-scoped tool result and SHA256 in audit trace. Preserve fee currency and evidence provenance.
- Use a short, isolated evidence-first answer prompt rather than accumulated history.
- On model length or unusable response, retry once with a clean, concise prompt; continue failing closed if still incomplete.
- Add 3 mocked regression tests.

No real Ollama test has been run in the packaging environment. 9/9 HTTP 200 is NOT claimed. The 7 explicit inspected tools in the harness are server routed, not autonomous model tool-selection. No execution capability is introduced.

To test: stop the previous backend, run the usual `scripts/run_preview.ps1` in this new extracted folder, and run `scripts/run_live_ollama_validation.ps1` from a second terminal. Only use the final JSON and actual answer quality to judge readiness.
