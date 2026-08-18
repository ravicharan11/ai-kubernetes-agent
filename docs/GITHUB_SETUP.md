# GitHub Setup and Push Instructions

This guide explains how to push the AI Kubernetes Agent code to GitHub.

## Prerequisites

- GitHub account
- Git installed
- SSH keys configured for GitHub (recommended) or personal access token

## Step 1: Create GitHub Repository

1. Log in to GitHub
2. Click "+" → "New repository"
3. Repository name: `ai-kubernetes-agent`
4. Description: "AI-powered Kubernetes troubleshooting agent"
5. Choose Public or Private
6. Click "Create repository"
7. Copy the repository URL

## Step 2: Initialize Git (if not already done)

```bash
cd ai-tagent

# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: AI Kubernetes Agent

- Add FastAPI backend with Kubernetes investigation
- Add Next.js frontend with cluster selection
- Implement Groq LLM integration for AI reasoning
- Add AWS EKS cluster discovery via AWS CLI
- Add kubeconfig cluster discovery
- Add comprehensive error handling
- Add investigation history with localStorage
- Add multi-cluster support
- Add Ubuntu setup documentation
- Add 1-hour demo presentation guide
- Add test failure scenarios documentation"
```

## Step 3: Add GitHub Remote

### Option A: SSH (Recommended)

```bash
# Add SSH remote
git remote add origin git@github.com:your-username/ai-kubernetes-agent.git

# Verify remote
git remote -v
```

### Option B: HTTPS

```bash
# Add HTTPS remote
git remote add origin https://github.com/your-username/ai-kubernetes-agent.git

# Verify remote
git remote -v
```

## Step 4: Push to GitHub

### First Push (Main Branch)

```bash
# Push to main branch
git push -u origin main
```

Or if your default branch is `master`:

```bash
# Push to master branch
git push -u origin master
```

### If Branch Name Issues

```bash
# Rename branch to main (if needed)
git branch -M main

# Push to main
git push -u origin main
```

## Step 5: Verify on GitHub

1. Go to your GitHub repository
2. Verify all files are present
3. Check commit history
4. Verify README.md displays correctly

## Step 6: Set Up GitHub SSH (if using SSH)

### Generate SSH Key

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add SSH key
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
```

### Add SSH Key to GitHub

1. Go to GitHub Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste your public key
4. Click "Add SSH key"

### Test SSH Connection

```bash
ssh -T git@github.com
```

## Step 7: Configure Git for GitHub (Optional)

```bash
# Configure git user
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Configure GitHub credentials (if using HTTPS)
git config --global credential.helper store
```

## Step 8: Create .gitignore (if not present)

```bash
# Create .gitignore in project root
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.next/
out/
build/
dist/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Docker
.dockerignore

# InsForge
.insforge/
EOF

# Add .gitignore
git add .gitignore
git commit -m "Add .gitignore"
git push
```

## Step 9: Pushing Updates

### After Making Changes

```bash
# Check status
git status

# Add changed files
git add .

# Commit changes
git commit -m "Add feature: description of changes"

# Push to GitHub
git push
```

### Pull Before Pushing

```bash
# Pull latest changes first
git pull origin main

# Resolve conflicts if any
# ...

# Push your changes
git push
```

## Step 10: Branching and Pull Requests (Optional)

### Create a New Branch

```bash
# Create and switch to new branch
git checkout -b feature/add-new-feature

# Make changes
# ...

# Commit changes
git add .
git commit -m "Add new feature"

# Push branch to GitHub
git push -u origin feature/add-new-feature
```

### Create Pull Request

1. Go to GitHub repository
2. Click "Pull requests" → "New pull request"
3. Select your branch
4. Add description
5. Click "Create pull request"

### Merge Pull Request

1. Review the pull request
2. Click "Merge pull request"
3. Delete branch if desired

## Common GitHub Commands

### Clone Repository

```bash
git clone git@github.com:your-username/ai-kubernetes-agent.git
cd ai-kubernetes-agent
```

### Check Remote

```bash
git remote -v
```

### Change Remote URL

```bash
git remote set-url origin git@github.com:new-username/ai-kubernetes-agent.git
```

### View Commit History

```bash
git log --oneline
```

### View Branches

```bash
git branch -a
```

### Switch Branches

```bash
git checkout main
```

### Delete Branch

```bash
# Delete local branch
git branch -d feature-branch

# Delete remote branch
git push origin --delete feature-branch
```

## Troubleshooting

### Authentication Failed

**For HTTPS:**
```bash
# Use personal access token instead of password
# Generate token at: GitHub Settings → Developer settings → Personal access tokens
```

**For SSH:**
```bash
# Test SSH connection
ssh -T git@github.com

# Check SSH key
ssh-add -l

# Add SSH key if needed
ssh-add ~/.ssh/id_ed25519
```

### Push Rejected

```bash
# Pull first
git pull origin main --rebase

# Resolve conflicts
# ...

# Push again
git push
```

### Remote Already Exists

```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin git@github.com:your-username/ai-kubernetes-agent.git
```

### Large Files

```bash
# Install Git LFS for large files
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.zip"

# Commit and push
git add .gitattributes
git commit -m "Add Git LFS"
git push
```

## GitHub Actions (Optional)

To add CI/CD with GitHub Actions:

1. Create `.github/workflows/ci.yml`
2. Add your CI/CD configuration
3. Commit and push
4. GitHub will automatically run the workflow

Example workflow:
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest
```

## GitHub Pages (Optional)

To deploy frontend to GitHub Pages:

1. Go to repository Settings → Pages
2. Select source: `gh-pages` branch
3. Create and push `gh-pages` branch:
```bash
# Build frontend
cd frontend
npm run build

# Deploy to gh-pages
npm install -g gh-pages
gh-pages -d .next
```

## Best Practices

1. **Write clear commit messages**
   - Use imperative mood
   - Be concise but descriptive
   - Reference issues if applicable

2. **Branch often**
   - Use feature branches
   - Keep main stable
   - Use pull requests for review

3. **Pull before push**
   - Always pull latest changes
   - Resolve conflicts locally
   - Keep history clean

4. **Use .gitignore**
   - Exclude sensitive files
   - Ignore build artifacts
   - Keep repository clean

5. **Protect main branch**
   - Enable branch protection
   - Require pull requests
   - Add status checks

## Additional Resources

- [GitHub Documentation](https://docs.github.com/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub CLI](https://cli.github.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
