# Gerrit Setup and Push Instructions

This guide explains how to push the AI Kubernetes Agent code to Gerrit.

## Prerequisites

- Gerrit account with appropriate permissions
- Git installed
- SSH keys configured for Gerrit
- Project repository URL from Gerrit

## Step 1: Install and Configure Git

```bash
# Install git (if not already installed)
sudo apt-get update
sudo apt-get install git

# Configure git user
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 2: Set Up SSH Keys for Gerrit

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add SSH key
ssh-add ~/.ssh/id_rsa

# Copy public key
cat ~/.ssh/id_rsa.pub
```

**Add SSH Key to Gerrit:**
1. Log in to your Gerrit instance
2. Go to Settings → SSH Public Keys
3. Paste your public key
4. Click "Add"

**Test SSH Connection:**
```bash
ssh -p 29418 your-gerrit-user@your-gerrit-host
```

## Step 3: Clone the Repository

```bash
# Clone from Gerrit (replace with your actual Gerrit URL)
git clone ssh://your-gerrit-user@your-gerrit-host:29418/ai-kubernetes-agent
cd ai-kubernetes-agent
```

## Step 4: Configure Gerrit Remote

```bash
# Add Gerrit remote (if not already configured)
git remote add gerrit ssh://your-gerrit-user@your-gerrit-host:29418/ai-kubernetes-agent

# Verify remote
git remote -v
```

## Step 5: Install Gerrit Commit Hook (Optional but Recommended)

```bash
# Install commit-msg hook for Change-Id generation
scp -p -P 29418 your-gerrit-user@your-gerrit-host:hooks/commit-msg .git/hooks/
chmod +x .git/hooks/commit-msg
```

## Step 6: Prepare Your Code for Push

### Option A: Push Existing Code

If you already have the code locally:

```bash
# Copy your code to the cloned repository
# Or work directly in the cloned repository

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: AI Kubernetes Agent

- Add FastAPI backend with Kubernetes investigation
- Add Next.js frontend with cluster selection
- Implement Groq LLM integration for AI reasoning
- Add AWS EKS cluster discovery
- Add comprehensive error handling
- Add investigation history with localStorage
- Add test failure scenarios documentation"

# Verify commit
git log -1
```

### Option B: Push from Existing Local Repository

If you have an existing local git repository:

```bash
# Navigate to your local repository
cd /path/to/your/local/ai-tagent

# Add Gerrit remote
git remote add gerrit ssh://your-gerrit-user@your-gerrit-host:29418/ai-kubernetes-agent

# Push to Gerrit
git push gerrit HEAD:refs/for/master
```

## Step 7: Push to Gerrit

### Create a Change for Review

```bash
# Push to Gerrit for review
git push gerrit HEAD:refs/for/master

# Or push to a specific branch
git push gerrit HEAD:refs/for/develop
```

### Push with Specific Options

```bash
# Push with specific reviewers
git push gerrit HEAD:refs/for/master%r=reviewer1@example.com,r=reviewer2@example.com

# Push with topic
git push gerrit HEAD:refs/for/master%topic=ai-kubernetes-agent-initial

# Push with draft status (WIP)
git push gerrit HEAD:refs/for/master%wip
```

## Step 8: Review in Gerrit

1. Open your Gerrit web interface
2. Navigate to "Changes" → "Outgoing Reviews"
3. Click on your change
4. Review the diff
5. Add reviewers if needed
6. Add comments if needed
7. Submit for review

## Step 9: Handle Review Feedback

### Update Your Change

```bash
# Make changes to your code
# ...

# Stage changes
git add .

# Amend the commit (keeps same Change-Id)
git commit --amend

# Push update to Gerrit
git push gerrit HEAD:refs/for/master
```

### Create a New Change

```bash
# Make changes
# ...

# Stage and commit as new
git add .
git commit -m "Add feature X"

# Push as new change
git push gerrit HEAD:refs/for/master
```

## Step 10: Merge Your Change

Once approved:

1. In Gerrit, click "Submit" button
2. Or use command line:
```bash
# Submit via SSH (if you have permissions)
ssh -p 29418 your-gerrit-user@your-gerrit-host gerrit review <change-id>,1 --submit
```

## Common Gerrit Commands

### List Your Changes
```bash
# Via SSH
ssh -p 29418 your-gerrit-user@your-gerrit-host gerrit query --format=JSON status:open owner:self

# Via web interface
# Navigate to Changes → Outgoing Reviews
```

### Abandon a Change
```bash
# Via SSH
ssh -p 29418 your-gerrit-user@your-gerrit-host gerrit review <change-id>,1 --abandon

# Via web interface
# Click "Abandon" button on change page
```

### Restore an Abandoned Change
```bash
# Via SSH
ssh -p 29418 your-gerrit-user@your-gerrit-host gerrit review <change-id>,1 --restore

# Via web interface
# Click "Restore" button on change page
```

## Troubleshooting

### SSH Connection Issues

```bash
# Test SSH connection
ssh -p 29418 your-gerrit-user@your-gerrit-host

# Check SSH key
ssh-add -l

# Debug SSH connection
ssh -vvv -p 29418 your-gerrit-user@your-gerrit-host
```

### Permission Denied

```bash
# Verify your Gerrit permissions
# Check with Gerrit administrator

# Ensure you're using correct username
git remote -v
```

### Missing Change-Id

```bash
# Install commit-msg hook
scp -p -P 29418 your-gerrit-user@your-gerrit-host:hooks/commit-msg .git/hooks/

# Amend commit to add Change-Id
git commit --amend --no-edit
```

### Push Rejected

```bash
# Pull latest changes first
git pull gerrit master

# Resolve conflicts if any
# ...

# Push again
git push gerrit HEAD:refs/for/master
```

## Best Practices

1. **Write Clear Commit Messages**
   - Use imperative mood
   - Include summary and detailed description
   - Reference related issues if applicable

2. **Keep Changes Focused**
   - One logical change per commit
   - Small, reviewable chunks
   - Related changes in same commit

3. **Test Before Pushing**
   - Run tests locally
   - Verify functionality
   - Check for syntax errors

4. **Add Reviewers Early**
   - Add appropriate reviewers
   - Provide context in change description
   - Respond to feedback promptly

5. **Use Topics**
   - Group related changes with topics
   - Makes tracking easier
   - Helps with batch reviews

## Project-Specific Notes

For the AI Kubernetes Agent project:

### Branch Structure
- `master` - Main production branch
- `develop` - Development branch (if using Gitflow)

### Code Review Checklist
- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No hardcoded credentials
- [ ] Error handling implemented
- [ ] Logging added where appropriate

### Required Documentation
- README.md updated
- UBUNTU_SETUP.md included
- DEMO_PRESENTATION_GUIDE.md included
- TEST_FAILURE_SCENARIOS.md included
- API documentation if applicable

## Additional Resources

- [Gerrit Documentation](https://gerrit-review.googlesource.com/Documentation/)
- [Gerrit Code Review](https://gerrit-review.googlesource.com/Documentation/cmd-index.html)
- [Gerrit SSH Access](https://gerrit-review.googlesource.com/Documentation/access-control.html)

## Support

For Gerrit-specific issues:
- Contact your Gerrit administrator
- Check Gerrit server logs
- Review Gerrit documentation

For project-specific issues:
- Contact project maintainers
- Check project documentation
- Review issue tracker
