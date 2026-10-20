# Windows-এ V5.3 চালাও

আগের V5.2 folder বদলাবে না। নতুন ZIP আলাদা `C:\BorderProof_AI\FinVeritas_BorderProof_AI_V5_3_Work_Audited` folder-এ extract করো। VS Code → Open Folder দিয়ে সেই folder খোলো। পুরোনো runtime database এই নতুন folder-এ সরাসরি copy কোরো না: আগে DB ও upload files backup করো, absolute document paths-ও আলাদাভাবে পরীক্ষা করতে হবে। নতুন account দিয়ে শুরু করাই সহজ।

## ১. Backend terminal

VS Code → Terminal → New Terminal → PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r services\api\requirements-lock.txt
powershell -ExecutionPolicy Bypass -File scripts\run_preview.ps1
```

এই `ExecutionPolicy Bypass` শুধু ওই script process-এর জন্য; পুরো কম্পিউটারের policy বদলায় না। Server terminal চালু রাখো। Browser-এ `http://127.0.0.1:8000/demo` খোলো। Sign in → Create local account → নিজের নাম/email/password দিয়ে account বানাও, তারপর sign in করো। এটি শুধু local demo account; email/পরিচয় যাচাই হয় না। আসল passport/bank document দেবে না।

আগের মতো চারটি seeded role দরকার হলে প্রথমে নিজের ১২+ অক্ষরের DEMO_SEED_PASSWORD set করে `scripts\run_preview.ps1 -SeedDemo` চালাও। কোনো default password নেই। Development server internet-এ expose কোরো না।

## ২. Next.js premium UI

Backend চালু রেখে নতুন terminal:

```powershell
cd apps\web
npm ci
npm run typecheck
npm run lint
npm run build
npm run start
```

`http://127.0.0.1:3000` খোলো। একই account দিয়ে sign in করো। API address আলাদাভাবে browser-এ set করতে হবে না; same-origin proxy আছে। Lint-এ কিছু performance warning থাকতে পারে। Production build-এ error হলে সেটি উপেক্ষা করবে না।

## ৩. সত্যিকারের local Qwen পরীক্ষা

আরেকটি terminal-এ:

```powershell
ollama list
ollama run qwen3:4b
```

Model prompt থেকে `/bye` দিয়ে বের হও; Ollama background service চালু থাকবে। Backend-এ model নাম `qwen3:4b` থাকতে হবে। এখন project root-এর নতুন terminal-এ:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_live_ollama_validation.ps1
```

Script নতুন synthetic account/case/invoice বানিয়ে আটটি actual model request চালাবে। কোনো payment/approval করবে না। ফল থাকবে `runtime\local_validation\sanitized_ollama_results.json`। ফাইলটা নিজে একবার দেখে এই chat-এ দেবে। Cookie, password, API key বা আসল financial document দেবে না। BLOCKED/FAILED হলে model connected/validated বলবে না। Work থেকে তোমার laptop-এর localhost দেখা যায় না।

## ৪. নিজের invoice demo

`AUDIT\evidence\native_final\inputs\fresh_GBP.txt` দেখে supported labelled format বোঝো। Payment case-এর institution/currency/amount-এর সঙ্গে invoice মিলতে হবে। শুধু SYNTHETIC fixture payee-গুলো internal simulator-এ যেতে পারে। অন্য university হলে fields বের হবে, কিন্তু real beneficiary যাচাই নেই বলে execution block হতে পারে। Missing/conflicting field হলে নতুন corrected invoice এবং নতুন investigation/quote/approval লাগবে।

Flow: case তৈরি → Payment lab → file upload → extract → investigate → synthetic quote → নির্দিষ্ট consent → simulated execution → receipt। টাকা আসলে কোথাও যায় না। PUBLIC FX REFERENCE এবং simulator-এর synthetic rate আলাদা।

## ৫. Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r services\api\requirements-dev.txt -c services\api\constraints-python312.txt
.\.venv\Scripts\python.exe -m pytest -q services\api\tests
.\.venv\Scripts\python.exe -m playwright install chromium
```

Native full check চালানোর আগে চলমান 8000/3000 server বন্ধ করো; script নিজে temporary server চালায়। Next build আগে থাকতে হবে:

```powershell
.\.venv\Scripts\python.exe scripts\run_real_execution.py --browser
```

Render/GitHub-এ এখনো কিছু publish করা হয়নি। Cloud deployment-এর আগে AUDIT\RENDER_READINESS.md পড়তে হবে। এই release local demo-ready; বাস্তব financial production-ready নয়।
