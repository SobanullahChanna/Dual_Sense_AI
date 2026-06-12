# Run this script to push the project to GitHub
# First, replace YOUR_GITHUB_USERNAME and REPO_NAME below

$username = "YOUR_GITHUB_USERNAME"
$repo = "Dual_Sense_AI"

# 1. Initialize git repo
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit - Dual Sense AI"

# 4. Add remote (create repo on GitHub first!)
git remote add origin "https://github.com/$username/$repo.git"

# 5. Push
git push -u origin main

Write-Host "Done! Make sure you created the repo at https://github.com/$username/$repo first" -ForegroundColor Green
