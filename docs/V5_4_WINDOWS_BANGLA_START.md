# V5.4 — Windows + VS Code (বাংলা)

**পুরোনো V5.3 folder ও তার database delete বা overwrite করবে না।** নতুন ZIP আলাদা folder-এ Extract করে VS Code → File → Open Folder করো।

## ধাপ ১: Backend চালাও

VS Code-এ Terminal → New Terminal (CMD):

```cmd
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r services\api\requirements-lock.txt
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_preview.ps1
```

Script default-এ local signup চালু করে, কোনো default password দেয় না। Browser: http://127.0.0.1:8000/demo → Create account। Server terminal বন্ধ করবে না। পুরোনো V5.3 server যদি port 8000 ব্যবহার করে আগে Ctrl+C চাপবে।

## ধাপ ২: New bidirectional corridor পরীক্ষা

Left menu → **Payment corridors** → Bangladesh/China বা China/Bangladesh select → Reverse direction → **New case**। নতুন case নিজের synthetic/fictional university name, amount ও invoice currency দিয়ে Save করো। এরপর Document vault-এ তোমার আগের ফাইল থেকে আলাদা একটি unseeded TXT/PDF upload করো।

Network → Case select → Run backend evidence check। Uploaded document proof না থাকলে `REVIEW_REQUIRED`, mismatch বা malicious instructions থাকলে `BLOCKED_CONFLICT` দেখানো উচিত। `NOT_VERIFIED` কোনো bug নয়; bank attestation নেই।

## ধাপ ৩: Actual public FX rate

Network → amount → Load actual FX reference। Internet available থাকলে backend Frankfurter v2-এর public data থেকে rate/date/URL/hash দেখাতে পারে। Provider unavailable হলে UNAVAILABLE থাকবে—উদ্দেশ্যপ্রণোদিত fail-safe। **Reference FX bank quote নয়।**

## ধাপ ৪: Real Qwen3 tool calling

নতুন Terminal খুলে `ollama list`, `ollama --version`, এবং `powershell.exe -ExecutionPolicy Bypass -File scripts\check_ollama.ps1` চালাও। Actual inference/trace test:

```cmd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_live_ollama_validation.ps1
```

এটি আগে থেকে চালু FastAPI backend ও Ollama `qwen3:4b` ব্যবহার করবে। Output `runtime\local_validation\sanitized_ollama_results.json`—প্রকাশের আগে ব্যক্তিগত data নেই নিশ্চিত করো। Script FAIL দেখালে screenshot দাও; successful দাবি কোরো না।

## ধাপ ৫: Next.js production test (Node 22+)

আরেক Terminal:

```cmd
cd apps\web
npm ci
npm run typecheck
npm run lint
npm run build
npm run start
```

Browser http://127.0.0.1:3000/corridors → selectable 3D globe, mouse drag, reverse, CNY/BDT support দেখো। WebGL না থাকলে SVG fallback দেখাবে। Backend port 8000 চালু রাখতে হবে। `npm run build` fail করলে Render deploy করবে না।

## খুব জরুরি

56 pairs = 56 directional **research/planning** routes, **not 56 usable bank transfer channels**. No real payments. External beneficiary authenticity, country-specific laws, and authorized provider credentials missing. Existing labeled internal simulator remains separate from this route-planning network.
