# Publishing V5 code without leaking private data

No GitHub repository has been created or updated by this V5 build. FinVeritas must select a team-owned repo and license; publishing is a separate authorized action.

Before `git add`, run `git status --short` and inspect ignored files for `runtime/`, `.env`, secrets, raw bank IDs, passports and student cards. **Never commit those.** `.env.example` must remain placeholders only.

Suggested commands after unpacking and confirming the intended repository and consent:

```bash
git init
git add .
git status --short
git commit -m "FinVeritas BorderProof AI V5 synthetic submission"
git branch -M main
git remote add origin https://github.com/<YOUR-TEAM>/<YOUR-REPO>.git
git push -u origin main
```

Replace placeholders with a repo the team owns. Confirm pages render on GitHub; upload/host the actual approved demo video separately if file limits demand. Do not say code or submission was uploaded before actual confirmation.
