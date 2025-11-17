# Git Workflow for Multi-Agent Development

## Branch Strategy

This project uses a **Feature Branch Workflow** with multiple agents working in parallel on separate feature branches.

---

## Branch Structure

```
main (production-ready code)
│
├── claude/testing-suite-implementation (Agent 1)
│
├── claude/cloudinary-file-storage (Agent 2)
│
├── claude/security-hardening (Agent 3)
│
├── claude/cicd-pipeline-setup (Agent 4)
│
└── claude/performance-optimization (Agent 5)
```

---

## Branch Naming Convention

All agent branches follow this pattern:
```
claude/<feature-name>
```

Examples:
- `claude/testing-suite-implementation`
- `claude/cloudinary-file-storage`
- `claude/security-hardening`

---

## Workflow for Each Agent

### 1. Starting Work

```bash
# Ensure you're on main and up-to-date
git checkout main
git pull origin main

# Create your feature branch (use exact name from your prompt)
git checkout -b claude/your-feature-name

# Verify you're on the correct branch
git branch --show-current
```

### 2. During Development

**Commit frequently with clear messages:**

```bash
# Stage your changes
git add <file1> <file2>

# Or stage all changes
git add .

# Commit with descriptive message
git commit -m "feat(module): Add feature description"
```

**Commit Message Format:**
```
<type>(<scope>): <description>

Types:
  - feat: New feature
  - fix: Bug fix
  - docs: Documentation changes
  - style: Code formatting (no logic changes)
  - refactor: Code restructuring
  - test: Adding tests
  - chore: Maintenance tasks

Examples:
  feat(testing): Add unit tests for WorkItem model
  fix(security): Resolve CSRF token validation issue
  docs(readme): Update installation instructions
  refactor(utils): Optimize image resize function
```

**Check your status regularly:**
```bash
git status
git diff
```

### 3. Pushing to Remote

```bash
# Push your branch to remote
git push -u origin claude/your-feature-name

# Subsequent pushes (after first one)
git push
```

### 4. Before Merging

**Ensure everything works:**
```bash
# Run tests (if available)
pytest tests/

# Run linting (if configured)
make lint

# Test the app locally
python run.py
# Test in browser: http://localhost:5001
```

**Rebase on main to get latest changes:**
```bash
# Fetch latest main
git fetch origin main

# Rebase your branch on main
git rebase origin/main

# If conflicts occur, resolve them:
git status  # See conflicted files
# Edit files to resolve conflicts
git add <resolved-files>
git rebase --continue

# Push rebased branch (use --force-with-lease)
git push --force-with-lease
```

---

## Merge Order

**IMPORTANT:** Follow this sequential order to minimize conflicts:

1. **First:** `claude/testing-suite-implementation` (Agent 1)
2. **Second:** `claude/cloudinary-file-storage` (Agent 2)
3. **Third:** `claude/performance-optimization` (Agent 5)
4. **Fourth:** `claude/security-hardening` (Agent 3)
5. **Last:** `claude/cicd-pipeline-setup` (Agent 4)

---

## Merging Process

### For the Agent Completing Work

1. **Ensure branch is up-to-date:**
   ```bash
   git checkout claude/your-feature-name
   git fetch origin main
   git rebase origin/main
   ```

2. **Run final checks:**
   ```bash
   # Test everything works
   python run.py

   # Run tests if available
   pytest

   # Check for uncommitted changes
   git status
   ```

3. **Push final version:**
   ```bash
   git push origin claude/your-feature-name
   ```

4. **Notify team:**
   - Post message: "Agent X: `claude/your-feature-name` ready for merge"
   - Wait for approval from project lead

### For the Project Lead

1. **Review the branch:**
   ```bash
   git fetch origin
   git checkout claude/feature-name
   git log --oneline
   git diff main
   ```

2. **Test locally:**
   ```bash
   python run.py
   # Test in browser
   pytest  # If tests exist
   ```

3. **Merge to main:**
   ```bash
   git checkout main
   git merge --no-ff claude/feature-name -m "Merge Agent X: Feature description"
   git push origin main
   ```

4. **Tag the merge (optional):**
   ```bash
   git tag -a v1.1.0-agent1 -m "Agent 1: Testing suite implementation"
   git push origin v1.1.0-agent1
   ```

5. **Notify team:**
   - Post message: "Agent X merged successfully to main"
   - Other agents should now rebase on updated main

---

## Handling Merge Conflicts

### When Conflicts Occur

```bash
# During rebase, if conflicts occur:
git status
# Will show conflicted files

# Edit conflicted files, look for:
<<<<<<< HEAD
Your changes
=======
Incoming changes
>>>>>>> branch-name

# Resolve conflicts, then:
git add <resolved-file>
git rebase --continue

# Or abort and try later:
git rebase --abort
```

### Common Conflict Files

Based on agent assignments, expect conflicts in:

- `requirements.txt` - **All agents add dependencies**
  - Resolution: Merge all, sort alphabetically, remove duplicates

- `config.py` - **Agents 2, 3, 5 add config**
  - Resolution: Group by agent with comments:
  ```python
  # Agent 2: Cloudinary Configuration
  CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
  # ...

  # Agent 3: Security Configuration
  SESSION_COOKIE_SECURE = True
  # ...

  # Agent 5: Performance Configuration
  ITEMS_PER_PAGE = 25
  # ...
  ```

- `app/models.py` - **Agents 2, 5 modify Photo model**
  - Resolution: Combine changes carefully
  ```python
  class Photo(db.Model):
      # Existing fields
      filename = db.Column(...)

      # Agent 2: Cloud storage fields
      cloud_url = db.Column(db.String(500))
      storage_type = db.Column(db.String(20), default='local')

      # Agent 5: Thumbnail field
      thumbnail_path = db.Column(db.String(500))

      # Agent 5: Index
      __table_args__ = (
          Index('idx_work_item_id', 'work_item_id'),
      )
  ```

- `app/admin.py`, `app/utils.py` - **Multiple agents modify**
  - Resolution: Manual merge, test thoroughly after

---

## Parallel Development Tips

### Minimizing Conflicts

1. **Stay in your lane:** Only modify files listed in your agent prompt
2. **Commit frequently:** Small commits are easier to merge
3. **Pull main regularly:** Stay updated with other agents' work
4. **Communicate:** Notify team before modifying shared files
5. **Test before pushing:** Ensure your code doesn't break existing functionality

### When Another Agent Merges Before You

```bash
# Fetch the updated main
git fetch origin main

# Rebase your work on top of new main
git checkout claude/your-feature-name
git rebase origin/main

# Resolve any conflicts
# Test your code still works
# Push updated branch
git push --force-with-lease
```

---

## Emergency Procedures

### Rollback a Merge

If a merge breaks something critical:

```bash
# Find the merge commit
git log --oneline --graph

# Revert the merge
git revert -m 1 <merge-commit-hash>

# Push the revert
git push origin main

# Notify team
```

### Recover Deleted Work

```bash
# Find lost commit
git reflog

# Recover it
git checkout <commit-hash>
git checkout -b recovery-branch

# Cherry-pick specific commits
git cherry-pick <commit-hash>
```

### Force Push Safety

**NEVER force push to main:**
```bash
# DON'T DO THIS:
git push --force origin main  # ❌ NEVER!

# Only force push your own feature branch:
git push --force-with-lease origin claude/your-feature-name  # ✅ OK
```

---

## Git Best Practices

### DO:
- ✅ Commit frequently with clear messages
- ✅ Pull/rebase on main regularly
- ✅ Test before pushing
- ✅ Use descriptive branch names
- ✅ Keep commits focused (one feature per commit)
- ✅ Review your own changes before committing (`git diff`)

### DON'T:
- ❌ Commit sensitive data (.env files, secrets)
- ❌ Force push to main
- ❌ Commit broken code
- ❌ Make giant commits (harder to review)
- ❌ Modify files outside your agent scope
- ❌ Forget to test after rebasing

---

## Useful Git Commands

### Status & Information
```bash
git status                    # Show modified files
git log --oneline -10         # Show last 10 commits
git log --graph --all         # Show branch graph
git diff                      # Show unstaged changes
git diff --staged             # Show staged changes
git blame <file>              # See who changed what
```

### Undoing Changes
```bash
git checkout -- <file>        # Discard changes in file
git reset HEAD <file>         # Unstage file
git reset --soft HEAD~1       # Undo last commit, keep changes
git reset --hard HEAD~1       # Undo last commit, discard changes
```

### Branching
```bash
git branch                    # List local branches
git branch -a                 # List all branches (including remote)
git branch -d <branch>        # Delete local branch
git push origin --delete <branch>  # Delete remote branch
```

### Stashing (temporary save)
```bash
git stash                     # Save changes temporarily
git stash list                # List stashed changes
git stash pop                 # Apply and remove stash
git stash apply               # Apply but keep stash
```

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ Agent starts work                                           │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ git checkout -b claude/feature-name                         │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ Make changes → git add → git commit                         │
│ (repeat many times)                                         │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ git push origin claude/feature-name                         │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ Notify team: "Ready for merge"                              │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ Project Lead reviews → Tests → Merges to main               │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ Other agents rebase on updated main                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Questions?

- **Can I merge my own branch?** No, wait for project lead approval
- **What if I made a mistake?** Don't panic, git can recover almost anything
- **Should I squash commits?** No, keep commit history for review
- **Can I work on multiple branches?** No, focus on your assigned agent role

---

**Last Updated:** 2025-11-17
**Version:** 1.0
