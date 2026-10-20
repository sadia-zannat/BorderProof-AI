# BorderProof AI V5.1 থেকে V5.2-তে যাওয়া — VS Code-এ (বাংলা)

**এই version-এ UI বদলেছে, payment/agent/backend safety controls বাদ যায়নি। Ollama আবার download করার দরকার নেই।**

## Part 1: পুরোনো server বন্ধ করো

1. এখন যে VS Code terminal-এ `Uvicorn running on http://127.0.0.1:8000` আছে, সেখানে একবার **Ctrl+C** দাও।
2. Terminal server বন্ধ হওয়ার পরও পুরোনো source folder delete করবে না।
3. পুরোনো project folder তোমার: `C:\BorderProof_AI\BorderProof_AI_V5_1_Free_Agent`।

## Part 2: ZIP Extract এবং Data backup

1. `BorderProof_AI_V5_2_Premium_UI.zip` download করো।
2. `C:\BorderProof_AI\`-এর ভেতরে extract করো; নতুন root: `C:\BorderProof_AI\BorderProof_AI_V5_2_Premium_UI` (যে folder-এ `README.md`, `apps`, `services`, `scripts` আছে)। ZIP-এর extra nested folder থাকলে সেটি খুলো।
3. পুরোনো project-এ তোমার created payment cases/receipts থাকলে, **server বন্ধ থাকা অবস্থায়** পুরোনো `runtime` folder-এর backup নাও। তারপর পুরোনো `runtime` folder **copy** করে নতুন project-এর root-এ paste করো। এতে `runtime/borderproof.sqlite3` database ও `runtime/uploads` থাকবে।
4. `runtime` না থাকলে বা পুরোনো demo case সংরক্ষণ না করতে চাইলে copy করা লাগবে না।
5. **নিজের তৈরি data সহ পুরোনো folder/DB delete করবে না।** নতুন version কাজ করছে নিশ্চিত হয়ে তারপর backup রাখবে।

## Part 3: VS Code-এ নতুন project

1. **File → Open Folder** → `C:\BorderProof_AI\BorderProof_AI_V5_2_Premium_UI`।
2. **Terminal → New Terminal**। নিচের commands CMD terminal-এর জন্য; PowerShell হলে আলাদা activate command লাগবে।
3. Terminal-এ একে একে:

```cmd
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r services\api\requirements.txt
```

এগুলো প্রথমবার নতুন directory-তে install করবে, Ollama model আবার download হবে না।

## Part 4: Local demo environment ও server

**CMD Terminal-এ** প্রত্যেকটি command Enter দাও:

```cmd
set "APP_ENV=development"
set "ENABLE_DEMO_SEED=1"
set "OLLAMA_MODEL=qwen3:4b"
set "OLLAMA_BASE_URL=http://127.0.0.1:11434"
set "DEMO_SEED_PASSWORD=YOUR_OWN_PRIVATE_PASSWORD"
python -m uvicorn app.main:app --app-dir services\api --host 127.0.0.1 --port 8000
```

`YOUR_OWN_PRIVATE_PASSWORD` দিয়ে **নিজের** একটি শক্তিশালী password দাও, screenshot-এ password দেখাবে না। **পুরোনো runtime DB copy করলে আগের seeded account-এর আগের password-ই লাগবে**; `DEMO_SEED_PASSWORD` বদলালেই পুরোনো account password reset হয় না।

## Part 5: Chrome-এ যাচাই

1. যাও `http://127.0.0.1:8000/demo`।
2. পুরোনো page cache দেখালে `Ctrl+F5` চাপো।
3. Landing-এ আগের লম্বা description আর full sidebar থাকবে না।
4. **Sign in** → `student@borderproof.test` এবং নিজের original seeded password।
5. Dashboard, AI Agent এবং Payment Lab তিনটি page ঘুরে দেখো।
6. AI Agent-এ synthetic case নিয়ে প্রশ্ন করতে পারো: `Which evidence is missing for this case?` Ollama background server চালু থাকতে হবে।

কোনো error এলে **private password বাদ দিয়ে** VS Code terminal-এর error text / screenshot পাঠাও।

### সতর্কতা

এটি local **synthetic financial sandbox**। Real invoice, NID, passport, real bank details upload করবে না। Real money movement হয় না। Next.js production build আলাদাভাবে test করতে হবে।
