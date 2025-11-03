# 🔧 Repository Setup Guide

## Initial Setup Complete ✅

The following has been configured:

- ✅ Branch structure: `dev`, `stage`, `prod`
- ✅ GitHub Actions workflows for each environment
- ✅ PR templates for each branch
- ✅ Deployment documentation

## Manual Configuration Required

### 1. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Build and deployment**:
   - Source: Select **GitHub Actions**
3. Save

Your site will be available at: **https://evgenygurin.github.io/agent-boss/**

### 2. Configure Branch Protection Rules

#### For `dev` branch:

1. Go to **Settings** → **Branches** → **Add branch protection rule**
2. Branch name pattern: `dev`
3. Enable:
   - ✅ Require a pull request before merging
     - Required approvals: 1
     - Dismiss stale PR reviews
   - ✅ Require status checks to pass
     - Add: `Lint & Validation`, `Build & Test`
   - ✅ Require conversation resolution
   - ✅ Do not allow bypassing the above settings
4. Save

#### For `stage` branch:

1. **Settings** → **Branches** → **Add branch protection rule**
2. Branch name pattern: `stage`
3. Enable:
   - ✅ Require a pull request before merging
     - Required approvals: 1
     - Dismiss stale PR reviews
   - ✅ Require status checks to pass
     - Add: `Security Scan`, `Integration Tests`
   - ✅ Require conversation resolution
   - ✅ Require linear history
   - ✅ Do not allow bypassing the above settings
4. Save

#### For `prod` branch:

1. **Settings** → **Branches** → **Add branch protection rule**
2. Branch name pattern: `prod`
3. Enable:
   - ✅ Require a pull request before merging
     - Required approvals: 2
     - Dismiss stale PR reviews
     - Require review from Code Owners (optional)
   - ✅ Require status checks to pass
   - ✅ Require conversation resolution
   - ✅ Require linear history
   - ✅ Require signed commits (recommended)
   - ✅ Include administrators
   - ✅ Do not allow bypassing the above settings
4. Save

### 3. Set Up Environments (Optional but Recommended)

#### Development Environment

1. Go to **Settings** → **Environments** → **New environment**
2. Name: `development`
3. No protection rules needed
4. Save

#### Staging Environment

1. **Settings** → **Environments** → **New environment**
2. Name: `staging`
3. Protection rules:
   - ✅ Required reviewers: Add team members
   - Wait timer: 0 minutes
4. Save

#### Production Environment

1. **Settings** → **Environments** → **New environment**
2. Name: `production`
3. Protection rules:
   - ✅ Required reviewers: Add 2+ team members
   - Wait timer: 5 minutes (optional cooling-off period)
   - Deployment branches: Only `prod` branch
4. Save

### 4. Configure Repository Secrets (if needed)

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add any required secrets for your workflows

### 5. Enable Actions Permissions

1. Go to **Settings** → **Actions** → **General**
2. Workflow permissions:
   - Select: **Read and write permissions**
   - ✅ Allow GitHub Actions to create and approve pull requests
3. Save

## Quick Start

### For Developers

```bash
# Clone repository
git clone https://github.com/evgenygurin/agent-boss.git
cd agent-boss

# Start working on a feature
git checkout dev
git pull origin dev
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add my feature"
git push origin feature/my-feature

# Create PR to dev via GitHub UI
```

### For Deploying to Staging

```bash
# Merge dev to stage via PR
git checkout stage
git pull origin stage
git checkout -b promote/dev-to-stage
git merge dev
git push origin promote/dev-to-stage

# Create PR to stage via GitHub UI
```

### For Production Release

```bash
# Merge stage to prod via PR
git checkout prod
git pull origin prod
git checkout -b release/v1.0.0
git merge stage
git push origin release/v1.0.0

# Create PR to prod via GitHub UI
```

## Verification Checklist

After completing setup, verify:

- [ ] GitHub Pages is enabled and accessible
- [ ] Branch protection rules are active for dev, stage, prod
- [ ] Environments are configured
- [ ] GitHub Actions workflows can run successfully
- [ ] PR templates appear when creating PRs

## Troubleshooting

### GitHub Actions not running?

- Check **Settings** → **Actions** → **General**
- Ensure "Allow all actions and reusable workflows" is selected

### Can't push to branches?

- This is expected! All changes must go through PRs
- Create a feature branch and open a PR

### Workflows failing?

- Check the Actions tab for detailed logs
- Ensure all required status checks are properly named

## Next Steps

1. Complete the manual configuration above
2. Read [WORKFLOW.md](./WORKFLOW.md) for detailed workflow documentation
3. Create your first feature branch and test the process
4. Set up monitoring and alerts (optional)

## Support

- 📖 [Workflow Documentation](./WORKFLOW.md)
- 🐛 [Report Issues](https://github.com/evgenygurin/agent-boss/issues)
- 💬 Contact the DevOps team

---

**Setup Date**: 2024  
**Last Updated**: 2024
