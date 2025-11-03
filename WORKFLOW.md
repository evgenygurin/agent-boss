# 🔄 Git Workflow & Deployment Strategy

## Branch Strategy

This project uses a **three-environment branching strategy** optimized for CI/CD:

```
feature/* → dev → stage → prod
```

### Branch Overview

| Branch | Environment | Purpose | Auto-Deploy | Protection |
|--------|-------------|---------|-------------|------------|
| `dev` | Development | Active development & feature integration | ✅ Yes | Medium |
| `stage` | Staging | Pre-production testing & validation | ✅ Yes | High |
| `prod` | Production | Live production site | ✅ Yes | Critical |

## 🔀 Development Workflow

### 1. Feature Development

```bash
# Start from dev
git checkout dev
git pull origin dev

# Create feature branch
git checkout -b feature/my-awesome-feature

# Make your changes
git add .
git commit -m "feat: add awesome feature"

# Push feature branch
git push origin feature/my-awesome-feature
```

### 2. Create PR to Dev

- Open PR from `feature/my-awesome-feature` → `dev`
- Use the development PR template
- Wait for CI checks to pass
- Get code review approval
- Merge to dev

### 3. Automatic Dev Deployment

Once merged to `dev`:
- ✅ Lint & validation runs
- ✅ Build & tests execute
- ✅ Auto-deploys to development environment

## 🎭 Staging Promotion

When dev is stable and ready for testing:

```bash
# Create PR from dev to stage
git checkout stage
git pull origin stage
git checkout -b promote/dev-to-stage
git merge dev
git push origin promote/dev-to-stage
```

- Open PR from `promote/dev-to-stage` → `stage`
- Use the staging PR template
- Include all changes since last staging deployment
- Wait for approvals

### Automatic Staging Deployment

Once merged to `stage`:
- ✅ Security scan runs
- ✅ Integration tests execute
- ✅ Deploys to staging environment
- ✅ Smoke tests run
- 📋 Manual validation required before prod

## 🚀 Production Release

After staging validation is complete:

```bash
# Create PR from stage to prod
git checkout prod
git pull origin prod
git checkout -b release/v1.2.3
git merge stage
git push origin release/v1.2.3
```

- Open PR from `release/v1.2.3` → `prod`
- Use the production PR template
- **Requires multiple approvals**
- Include release notes

### Automatic Production Deployment

Once merged to `prod`:
- ✅ Deploys to GitHub Pages (production)
- 🌐 Live at: https://evgenygurin.github.io/agent-boss/
- 📊 Deployment summary created

## 🔥 Hotfix Process

For urgent production fixes:

```bash
# Create hotfix from prod
git checkout prod
git pull origin prod
git checkout -b hotfix/critical-bug-fix

# Fix the issue
git add .
git commit -m "fix: critical bug in production"

# Push and create PR to prod
git push origin hotfix/critical-bug-fix
```

After merging to prod:
```bash
# Backport to stage
git checkout stage
git merge prod
git push origin stage

# Backport to dev
git checkout dev
git merge stage
git push origin dev
```

## 🚫 Branch Protection Rules

### Dev Branch
- ✅ Require PR before merging
- ✅ Require status checks to pass
- ✅ Require conversation resolution
- ❌ No direct pushes

### Stage Branch
- ✅ Require PR before merging
- ✅ Require 1+ approval
- ✅ Require status checks to pass
- ✅ Dismiss stale reviews
- ❌ No direct pushes

### Prod Branch
- ✅ Require PR before merging
- ✅ Require 2+ approvals
- ✅ Require status checks to pass
- ✅ Require linear history
- ✅ Include administrators
- ❌ No direct pushes
- ⚠️ Signed commits required

## 🔄 CI/CD Pipeline

### Development (`dev` branch)
```yaml
Trigger: Push to dev
├── Lint & Validation
├── Build & Test
└── Deploy Preview → Development environment
```

### Staging (`stage` branch)
```yaml
Trigger: Push to stage
├── Security Scan
├── Integration Tests
├── Deploy → Staging environment
└── Smoke Tests
```

### Production (`prod` branch)
```yaml
Trigger: Push to prod
├── Deploy → Production (GitHub Pages)
└── Create deployment summary
```

## 📋 PR Templates

Different PR templates for each target branch:

- **Dev PR**: Focus on code quality and feature completeness
- **Stage PR**: Focus on testing plan and validation
- **Prod PR**: Focus on release notes and deployment safety

## 🎯 Best Practices

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: resolve bug
docs: update documentation
style: format code
refactor: restructure code
test: add tests
chore: update dependencies
```

### PR Guidelines

1. **Keep PRs small** - Easier to review and test
2. **Write descriptive titles** - Clear purpose
3. **Fill out PR template** - Complete all sections
4. **Link issues** - Reference related issues
5. **Test locally first** - Don't rely on CI only

### Deployment Schedule

- **Dev**: Continuous (multiple times per day)
- **Stage**: Daily or as needed
- **Prod**: Scheduled releases (e.g., weekly/bi-weekly)

### Emergency Procedures

If production is broken:

1. **Immediate rollback**:
   ```bash
   git checkout prod
   git reset --hard <last-good-commit>
   git push --force origin prod
   ```

2. **Create hotfix** following hotfix process above

3. **Post-mortem** after resolution

## 🔍 Monitoring & Validation

### Development
- Check CI/CD logs
- Manual testing optional

### Staging
- ✅ Full test suite
- ✅ Manual validation required
- ✅ Performance testing
- ✅ Security scan review

### Production
- ✅ Health checks immediately after deploy
- ✅ Monitor error rates
- ✅ Check core functionality
- ✅ Watch for 24 hours

## 📞 Getting Help

- **CI/CD issues**: Check GitHub Actions logs
- **Workflow questions**: See this document
- **Emergency**: Follow hotfix process

## 📚 Additional Resources

- [Git Flow Guide](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**Last Updated**: 2024  
**Maintained by**: DevOps Team
