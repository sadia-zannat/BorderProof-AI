# BorderProof AI V5.5 — Windows laptop-এ যাচাই

**V5.4 ZIP এবং আগের database/uploads নিরাপদে রেখে V5.5 ZIP অন্য নতুন folder-এ extract করো।** Project-এ synthetic demo data ব্যবহার করবে; আসল bank account/ID/password আপলোড করবে না।

## ১. Backend, migration, tests

VS Code → Terminal → CMD (project root):

```cmd
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r services\api\requirements-lock.txt
python -m pytest -q services\api\tests
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_preview.ps1
```

যদি optional Hypothesis tests run করতে চাও: `python -m pip install -r services\api\requirements-dev.txt`। Local preview: `http://127.0.0.1:8000/demo`। নতুন synthetic/local account খুলো। পুরোনো database migrate করার আগে backup নাও।

## ২. Network security checks

Payment corridors → China → Bangladesh → Reverse → Create case। Fictional invoice upload করে extraction চালাও, তারপর Run evidence check। একই invoice-এ দুইটি ভিন্ন `Amount:` থাকলে assessment `BLOCKED_CONFLICT` হওয়া উচিত। Old invoice file মুছে ফেললে/alter করলে `DOCUMENT_SET_INTEGRITY_FAILED` হওয়া উচিত; filesystem hand-editing কেবল isolated test database-এ করবে। ৫৬টি route হলো planning coverage, bank-verified transfer নয়।

## ৩. Next.js UI (এখানে build verification pending)

নতুন terminal:

```cmd
cd apps\web
npm ci
npm run typecheck
npm run lint
npm run build
npm run start
```

Browser: `http://127.0.0.1:3000/corridors`। Desktop/mobile, 3D globe, 2D fallback, both directions, fresh case, evidence history যাচাই করো। যেকোনো command fail হলে **PASS বলবে না**, error report দেবে। Node >=22 এবং backend port 8000 চালু থাকতে হবে।

## ৪. Real external checks (এই build-এ যাচাই হয়নি)

Local Ollama `qwen3:4b` চালিয়ে project root থেকে:

```cmd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run_live_ollama_validation.ps1
```

Network FX panel-এ CNY/BDT ও CNY/GBP request চালাও; provider unavailable হলে unavailable-ই রাখবে। FX reference কোনো payment quote নয়। Live Qwen/FX failure, negative outcomes, missing data—সব সত্যভাবে log করো।

**এই V5.5 local demo ready; production financial release নয়। Render deploy, public Git publication, bank/API credentials, বা real transfer শুরু করার আগে আলাদা approval ও security validation প্রয়োজন।**
