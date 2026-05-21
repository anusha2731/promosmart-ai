# How to Push PromoSmart AI to Your GitHub

## Option 1: Create a new repo on GitHub first

1. Go to https://github.com/new
2. Repository name: `promosmart-ai`
3. Description: `AI-Powered Retail Promotion Optimization Platform with Gemini 3 Flash`
4. Choose: **Public** or **Private**
5. **DO NOT** check "Initialize with README" (we already have one)
6. Click "Create repository"

## Option 2: Push the existing code

After creating the empty repo on GitHub, run these commands locally:

```bash
# 1. Clone this entire /app folder to your local machine (or download as zip)
# 2. Navigate to the project folder
cd promosmart-ai

# 3. Add your GitHub remote
git remote add origin https://github.com/anusha2731/promosmart-ai.git

# 4. Verify remote
git remote -v

# 5. Push to GitHub
git push -u origin main
```

You may need to authenticate with a GitHub Personal Access Token (PAT):
- Go to https://github.com/settings/tokens
- Generate a new token with `repo` scope
- When prompted for password during `git push`, paste the token

## Option 3: Using GitHub CLI (gh)

```bash
gh auth login
gh repo create anusha2731/promosmart-ai --public --source=. --remote=origin --push
```

## Important Files Included
- ✅ Full source code (backend + frontend)
- ✅ README.md with setup instructions
- ✅ ARCHITECTURE.md with system design
- ✅ API.md with endpoint reference
- ✅ docker-compose.yml + Dockerfiles
- ✅ .env.example files (no real secrets)
- ✅ Seed data script

## Files Excluded (via .gitignore)
- ❌ `backend/.env` (contains real EMERGENT_LLM_KEY)
- ❌ `frontend/.env` (contains preview URL)
- ❌ `node_modules/`, `__pycache__/`, etc.
- ❌ Internal Emergent files (`memory/`, `design_guidelines.json`)

## After Pushing

Share the repo URL: `https://github.com/anusha2731/promosmart-ai`

Anyone can clone and run:
```bash
git clone https://github.com/anusha2731/promosmart-ai.git
cd promosmart-ai
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Edit backend/.env to add EMERGENT_LLM_KEY
docker-compose up --build
docker-compose exec backend python seed_data.py
```

Then visit: http://localhost:3000
Login: admin@promosmart.com / Admin@123
