# Live versus mock evidence

| Check | Classification | Observed status |
|---|---|---|
| Twelve inherited agent tests | Mocked model/HTTP transport contracts | Executed as part of backend pytest |
| Two new malformed model tests | Mocked contracts | 502/explicit rejection, no payment action |
| Database tools and conversation persistence in those tests | Actual application/database with mock model selection | Executed, not a live Qwen result |
| Native /agent/chat with unreachable local endpoint | Actual HTTP/network failure, no mocked answer | 503 observed in API and browser |
| Work localhost:11434 /api/tags | Genuine local connection probe | Connection refused; zero inference results |
| Eight new Qwen local validation scenarios | Real-model-only harness | PENDING USER-LOCAL VERIFICATION |
| Standard LLM, live tool-agent, live full-system benchmark | Requires actual model and fair shared inputs | NOT MEASURED |

`evidence/live_model_preflight.json` has an empty results array and BLOCKED status. The user's Windows Ollama is not reachable through Work localhost. No tunnel or remote paid inference was attempted.

Run `scripts/run_live_ollama_validation.ps1` locally with API and Ollama running. It checks the installed model/version/digest, creates a new synthetic local student/case/invoice/quote, measures eight real requests and actual tool expectations, records response/trace latency, and verifies no transfer or balance change. Expected-tool failures return a failing classification. Answer quality and evidence attribution still require human review. It saves only synthetic test content, no cookies or passwords, to `runtime/local_validation/sanitized_ollama_results.json`.

The Python harness was executed in Work and correctly classified the unavailable model. PowerShell is unavailable here, so the PS wrapper was inspected, not executed in a Windows shell. The old `benchmarks/run_real_ollama_eval.py` is retained for compatibility; the fresh-case harness is the recommended entry point.
