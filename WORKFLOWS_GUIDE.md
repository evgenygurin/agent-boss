# 🔄 GitHub Actions Workflows Guide

## Overview

This project uses **5 comprehensive GitHub Actions workflows** inspired by industry best practices, providing a complete CI/CD pipeline with automated testing, security scanning, and multi-environment deployments.

## Workflow Files

### 1. **Development CI/CD** (`dev.yml`)
**Trigger**: Push or PR to `dev` branch

#### Features:
- ✅ **Multi-version testing**: Python 3.10, 3.11, 3.12
- ✅ **Automated builds**: Syntax validation and compile checks
- ✅ **Artifact management**: Preserves build artifacts (7 days)
- ✅ **Auto-deploy preview**: Immediate development environment deployment

#### Jobs:
```yaml
lint → build (matrix) → deploy-preview → notify
```

#### When to use:
- Every commit to dev branch
- Feature branch PRs to dev
- Development testing

---

### 2. **Staging Deploy** (`stage.yml`)
**Trigger**: Push to `stage` branch

#### Features:
- 🔒 **Security scanning**: Automated security checks
- 🧪 **Integration tests**: Cross-version compatibility testing
- 📦 **Test artifacts**: Preserved for 14 days
- 💨 **Smoke tests**: Post-deployment validation

#### Jobs:
```yaml
security-scan → integration-tests (matrix) → deploy-staging → notify-ready
```

#### When to use:
- Promoting from dev to staging
- Pre-production validation
- UAT environment deployment

---

### 3. **Production Deploy** (`deploy.yml`)
**Trigger**: Push to `prod` branch

#### Features:
- 🚀 **GitHub Pages deployment**: Automatic production deployment
- 📊 **Deployment summaries**: Detailed success reports
- 🔐 **Production environment**: Protected with approvals

#### Jobs:
```yaml
deploy (GitHub Pages)
```

#### When to use:
- Production releases
- Final deployment after staging validation
- Public site updates

---

### 4. **PR Checks** (`pr-checks.yml`)
**Trigger**: PRs to `dev`, `stage`, or `prod`

#### Features:
- 🏷️ **Branch naming validation**: Enforces naming conventions
- 🔀 **Branch flow validation**: Ensures correct promotion paths
- ✅ **Automated checks**: Lint, security, build validation
- 💬 **PR comments**: Automated feedback on checks

#### Allowed Branch Patterns:
```
feature/*   - New features
bugfix/*    - Bug fixes
hotfix/*    - Emergency fixes
release/*   - Release branches
promote/*   - Promotion branches
```

#### Branch Flow Rules:
```
feature/* → dev
dev/promote/* → stage
stage/promote/hotfix/* → prod
```

#### Jobs:
```yaml
validate (naming + flow) → comment-summary
```

---

### 5. **Hotfix Pipeline** (`hotfix.yml`)
**Trigger**: Push to `hotfix/**` branches or PRs to `prod`

#### Features:
- 🔥 **Emergency response**: Fast-track critical fixes
- ✅ **Multi-version testing**: Ensures compatibility
- 🔒 **Security validation**: Required for production
- 🤖 **Automated PR creation**: Creates PRs with templates
- 🏷️ **Auto-labeling**: Tags with `hotfix`, `urgent`, `priority:critical`

#### Jobs:
```yaml
validate-hotfix → test-hotfix (matrix) → security-scan → create-promotion-prs → notify-team
```

#### When to use:
- Critical production bugs
- Security vulnerabilities
- Emergency patches

#### Example workflow:
```bash
# Create hotfix branch
git checkout prod
git checkout -b hotfix/critical-login-bug

# Fix the issue
git add .
git commit -m "fix: resolve critical login authentication bug"

# Push (triggers workflow)
git push origin hotfix/critical-login-bug

# Workflow will:
# 1. Validate branch name
# 2. Run tests (Python 3.10, 3.11, 3.12)
# 3. Run security scan
# 4. Auto-create PR to prod with hotfix template
# 5. Notify team
```

---

### 6. **Manual Deployment** (`manual-deploy.yml`)
**Trigger**: Manual workflow dispatch via GitHub UI

#### Features:
- 🎮 **Manual control**: Deploy to any environment on demand
- ⚙️ **Configurable options**:
  - Target environment (dev/staging/production)
  - Version/commit SHA
  - Deployment reason (required)
  - Skip tests (emergency only)
- 📝 **Deployment records**: Creates audit trail
- 🔒 **Security checks**: Required for production

#### How to use:
1. Go to **Actions** → **Manual Deployment**
2. Click **Run workflow**
3. Select:
   - **Environment**: development/staging/production
   - **Version**: (optional) specific commit SHA
   - **Reason**: Required deployment justification
   - **Skip tests**: Only for emergencies
4. Click **Run workflow**

#### Jobs:
```yaml
validate-deployment → run-tests (optional) → security-check (prod only) → deploy → create-summary → notify
```

---

## Custom Actions

### **Setup Python Environment** (`.github/actions/setup-python`)

Reusable action for consistent Python environment setup across all workflows.

#### Features:
- 🐍 Configurable Python version
- 💾 Automatic pip caching
- ⚡ Fast dependency installation
- ✅ Installation verification

#### Usage:
```yaml
- name: Setup Python Environment
  uses: ./.github/actions/setup-python
  with:
    python-version: '3.11'
```

#### Outputs:
- `python-version`: Installed Python version
- `cache-hit`: Whether cache was used

---

## Workflow Patterns

### Multi-Version Testing Matrix

All test jobs use a matrix strategy to ensure cross-version compatibility:

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
```

**Benefits:**
- ✅ Catches version-specific bugs early
- ✅ Ensures broad compatibility
- ✅ Future-proofs against Python updates

### Artifact Management

Workflows preserve important artifacts with retention policies:

**Development artifacts** (7 days):
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-artifacts-${{ github.sha }}
    retention-days: 7
```

**Test results** (14 days):
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: test-results-staging
    retention-days: 14
```

### Conditional Execution

Workflows use smart conditionals to optimize resource usage:

```yaml
# Only on push events
if: github.event_name == 'push'

# Only for specific branches
if: github.ref == 'refs/heads/prod'

# Only for PRs
if: github.event_name == 'pull_request'

# Skip if tests passed
if: inputs.skip_tests != true
```

---

## Workflow Triggers Summary

| Workflow | Trigger | When | Auto/Manual |
|----------|---------|------|-------------|
| **Development CI/CD** | Push/PR to `dev` | Every dev commit | Auto |
| **Staging Deploy** | Push to `stage` | Stage promotions | Auto |
| **Production Deploy** | Push to `prod` | Prod releases | Auto |
| **PR Checks** | PRs to any protected branch | All pull requests | Auto |
| **Hotfix Pipeline** | Push to `hotfix/**` | Emergency fixes | Auto |
| **Manual Deployment** | `workflow_dispatch` | On demand | Manual |

---

## Security & Best Practices

### Branch Protection
- ✅ All workflows validate branch flows
- ✅ Naming conventions enforced
- ✅ PR approval required for promotions

### Testing Strategy
- ✅ Multi-version compatibility testing
- ✅ Security scans before production
- ✅ Integration tests in staging
- ✅ Smoke tests post-deployment

### Artifact Management
- ✅ Build artifacts preserved
- ✅ Test results archived
- ✅ Retention policies configured
- ✅ Version-specific naming

### Deployment Safety
- ✅ Environment-specific deployments
- ✅ Manual approval gates (via branch protection)
- ✅ Deployment records
- ✅ Rollback procedures documented

---

## Common Scenarios

### Scenario 1: Regular Feature Development
```bash
git checkout dev
git checkout -b feature/new-dashboard
# ... make changes ...
git push origin feature/new-dashboard
# Create PR to dev → CI runs → Merge → Auto-deploy to dev
```

**Workflows triggered:**
1. PR Checks (on PR creation)
2. Development CI/CD (after merge)

---

### Scenario 2: Promoting to Staging
```bash
git checkout stage
git checkout -b promote/dev-to-stage-2024-11-03
git merge dev
git push origin promote/dev-to-stage-2024-11-03
# Create PR to stage → Tests run → Merge → Auto-deploy to staging
```

**Workflows triggered:**
1. PR Checks (validation)
2. Staging Deploy (after merge)

---

### Scenario 3: Production Release
```bash
git checkout prod
git checkout -b release/v1.2.0
git merge stage
git push origin release/v1.2.0
# Create PR to prod → Approvals required → Merge → Deploy to production
```

**Workflows triggered:**
1. PR Checks (validation)
2. Production Deploy (after merge)

---

### Scenario 4: Emergency Hotfix
```bash
git checkout prod
git checkout -b hotfix/critical-security-patch
# ... fix the issue ...
git commit -m "fix: patch critical security vulnerability"
git push origin hotfix/critical-security-patch
# Workflow auto-creates PR with hotfix template
```

**Workflows triggered:**
1. Hotfix Pipeline (auto-creates PR)
2. PR Checks (validation)
3. Production Deploy (after merge)
4. Manual backporting to stage and dev required

---

### Scenario 5: Manual Emergency Deployment
```
1. GitHub → Actions → Manual Deployment
2. Select environment: production
3. Reason: "Emergency rollback due to production issue"
4. Skip tests: ✅ (only if emergency)
5. Run workflow
```

**Workflows triggered:**
1. Manual Deployment (full pipeline with optional test skip)

---

## Monitoring & Debugging

### View Workflow Runs
```bash
# List recent runs
gh run list --limit 10

# View specific workflow
gh run view <run-id>

# Watch workflow in real-time
gh run watch <run-id>
```

### Check Workflow Status
```bash
# List all workflows
gh workflow list

# View workflow runs for specific branch
gh run list --branch dev --limit 5
```

### Download Artifacts
```bash
# List artifacts for a run
gh run view <run-id> --log

# Download artifact
gh run download <run-id> -n <artifact-name>
```

---

## Troubleshooting

### Workflow Not Triggering?

**Check:**
1. Branch name matches trigger patterns
2. Workflow file is in `.github/workflows/`
3. YAML syntax is valid
4. Actions are enabled in repository settings

### Tests Failing?

**Common causes:**
1. Missing dependencies in `requirements.txt`
2. Python version compatibility issues
3. Environment variables not set
4. Test files not found

**Solution:**
```bash
# Run tests locally first
python -m pip install -r requirements.txt
python test_boss.py
```

### PR Checks Failing?

**Common reasons:**
1. Invalid branch name (doesn't match patterns)
2. Wrong branch flow (e.g., merging directly to prod)
3. Missing required files
4. Syntax errors

**Fix:**
```bash
# Validate branch name
echo $BRANCH_NAME | grep -E "^(feature|bugfix|hotfix|release|promote)/"

# Check branch flow
git branch --contains HEAD
```

---

## Performance Optimization

### Caching Strategy
- ✅ Pip packages cached per requirements.txt hash
- ✅ Reduces installation time by ~60%
- ✅ Automatic cache invalidation on dependency changes

### Concurrency Control
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # for dev
  cancel-in-progress: false # for prod
```

### Matrix Parallelization
- ✅ Tests run in parallel across Python versions
- ✅ Reduces total pipeline time
- ✅ Early failure detection

---

## Next Steps

1. **Complete manual setup** from [SETUP.md](./SETUP.md)
2. **Configure branch protection** rules
3. **Set up environments** (development, staging, production)
4. **Test the complete flow** with a feature branch
5. **Customize workflows** for your specific needs

---

## References

- 📘 [WORKFLOW.md](./WORKFLOW.md) - Git workflow guide
- 🔧 [SETUP.md](./SETUP.md) - Repository setup
- 🌳 [BRANCHING_STRATEGY.md](./BRANCHING_STRATEGY.md) - Branch strategy
- 🚀 [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Quick command reference

---

**Last Updated**: 2024  
**Maintained by**: DevOps Team  
**Status**: 🟢 Active & Production-Ready
