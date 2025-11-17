# Multi-Agent Workflow System

## Quick Start Guide

This directory contains everything you need to run a multi-agent workflow for bringing the Ship Maintenance Tracker to production readiness.

---

## 📁 Directory Contents

- **`1_Testing_Engineer.md`** - Complete prompt for implementing test suite
- **`2_Cloud_Infrastructure_Engineer.md`** - Cloudinary integration prompt
- **`3_Security_Engineer.md`** - Security hardening prompt
- **`4_DevOps_Engineer.md`** - CI/CD pipeline setup prompt
- **`5_Performance_Engineer.md`** - Performance optimization prompt
- **`COORDINATION.md`** - Master coordination plan and tracking
- **`GIT_WORKFLOW.md`** - Git workflow and branch strategy
- **`README.md`** - This file

---

## 🚀 How to Use This System

### Option 1: Run All Agents in Parallel (Recommended)

If you have access to multiple Claude Code sessions (web or desktop):

1. **Open 5 separate Claude Code sessions**
2. **Navigate to your project directory in each session**
3. **Copy-paste the relevant prompt file into each session:**
   - Session 1 → Contents of `1_Testing_Engineer.md`
   - Session 2 → Contents of `2_Cloud_Infrastructure_Engineer.md`
   - Session 3 → Contents of `3_Security_Engineer.md`
   - Session 4 → Wait for Session 1 to finish, then use `4_DevOps_Engineer.md`
   - Session 5 → Contents of `5_Performance_Engineer.md`
4. **Monitor progress** using `COORDINATION.md`
5. **Merge branches** in the order specified in `GIT_WORKFLOW.md`

### Option 2: Run Agents Sequentially

If you only have one Claude Code session:

1. **Start with Agent 1** (Testing Engineer) - Most critical
2. **Run Agent 2** (Cloud Infrastructure) - Prevents data loss
3. **Run Agent 5** (Performance) - Improves scalability
4. **Run Agent 3** (Security) - Hardens application
5. **Run Agent 4** (DevOps) - Automates everything

---

## 📊 Agent Priority Matrix

| Agent | Priority | Duration | Can Start Now? | Depends On |
|-------|----------|----------|----------------|------------|
| 1. Testing Engineer | 🔴 CRITICAL | 1-2 days | ✅ Yes | None |
| 2. Cloud Infrastructure | 🔴 CRITICAL | 3-5 hours | ✅ Yes | None |
| 3. Security Engineer | 🔴 CRITICAL | 3-5 hours | ✅ Yes | None |
| 4. DevOps Engineer | 🟡 HIGH | 3-5 hours | ❌ No | Agent 1 |
| 5. Performance Engineer | 🟡 HIGH | 3-5 hours | ✅ Yes | None |

---

## 🎯 Expected Outcomes

### After Completing All Agents

Your application will have:

✅ **80%+ test coverage** with comprehensive test suite
✅ **Persistent cloud storage** for photos and documents
✅ **Security hardening** (CSRF, rate limiting, input validation)
✅ **Automated CI/CD pipeline** with GitHub Actions
✅ **Optimized performance** (database indexing, caching, pagination)

### Production Readiness Checklist

- [ ] All tests passing
- [ ] Photos persist across Railway restarts
- [ ] Security audit completed
- [ ] CI/CD pipeline operational
- [ ] Performance benchmarks met (page load < 2s)
- [ ] All environment variables configured
- [ ] Documentation updated

---

## 📝 Quick Copy-Paste Prompts

### Agent 1: Testing Engineer
```
Read the file AGENT_PROMPTS/1_Testing_Engineer.md and execute all tasks in that prompt. Create a comprehensive test suite for this Flask application with 80%+ code coverage.
```

### Agent 2: Cloud Infrastructure Engineer
```
Read the file AGENT_PROMPTS/2_Cloud_Infrastructure_Engineer.md and execute all tasks in that prompt. Migrate file storage from local filesystem to Cloudinary to solve Railway's ephemeral filesystem issue.
```

### Agent 3: Security Engineer
```
Read the file AGENT_PROMPTS/3_Security_Engineer.md and execute all tasks in that prompt. Perform a security audit and implement CSRF protection, input validation, rate limiting, and secure headers.
```

### Agent 4: DevOps Engineer (WAIT FOR AGENT 1 FIRST)
```
Read the file AGENT_PROMPTS/4_DevOps_Engineer.md and execute all tasks in that prompt. Set up a complete CI/CD pipeline with GitHub Actions, code quality tools, and pre-commit hooks.
```

### Agent 5: Performance Engineer
```
Read the file AGENT_PROMPTS/5_Performance_Engineer.md and execute all tasks in that prompt. Optimize database queries, add pagination, implement caching, and add performance monitoring.
```

---

## 🔄 Workflow Process

### 1. Start Agents
- Launch agents according to dependency order
- Each agent works on their designated branch
- Track progress in `COORDINATION.md`

### 2. Monitor Progress
- Check each agent's branch for commits
- Ensure no file conflicts (see `COORDINATION.md` conflict matrix)
- Communicate blockers immediately

### 3. Merge Branches
Follow this **exact order**:
1. `claude/testing-suite-implementation` (Agent 1)
2. `claude/cloudinary-file-storage` (Agent 2)
3. `claude/performance-optimization` (Agent 5)
4. `claude/security-hardening` (Agent 3)
5. `claude/cicd-pipeline-setup` (Agent 4)

### 4. Test Integration
After each merge:
```bash
git checkout main
git pull origin main
python run.py
# Test in browser: http://localhost:5001
pytest  # Run tests
```

### 5. Deploy to Production
```bash
# Set environment variables in Railway
railway variables set CLOUDINARY_CLOUD_NAME=...
railway variables set CLOUDINARY_API_KEY=...
# ... (see agent prompts for full list)

# Deploy
git push origin main
# Railway auto-deploys
```

---

## 📚 Documentation

### For Each Agent

Each agent prompt includes:
- **Mission Objective** - Clear goal
- **Step-by-Step Tasks** - Detailed instructions
- **Files to Modify** - Exact file list
- **Quality Checklist** - Completion criteria
- **Success Criteria** - Definition of done
- **Resources** - Links to documentation

### For Coordination

- **`COORDINATION.md`** - Track overall progress, manage conflicts
- **`GIT_WORKFLOW.md`** - Git commands and branch management
- **Parent `README.md`** - Project overview and deployment

---

## 🚨 Troubleshooting

### Agent Can't Start
- **Problem:** Unclear what to do
- **Solution:** Read the agent's prompt file completely
- **Tip:** Each prompt has step-by-step phases

### Git Conflicts
- **Problem:** Merge conflicts when pushing/merging
- **Solution:** See `GIT_WORKFLOW.md` conflict resolution section
- **Tip:** Follow the recommended merge order

### Tests Failing
- **Problem:** CI pipeline shows test failures
- **Solution:** Agent 1 needs to complete first
- **Tip:** Run `pytest` locally before pushing

### Railway Deployment Issues
- **Problem:** App won't start on Railway
- **Solution:** Check environment variables
- **Tip:** See `DEPLOYMENT.md` for full checklist

---

## 💡 Tips for Success

1. **Read the full prompt** before starting
2. **Follow the phases** in order
3. **Test frequently** as you work
4. **Commit often** with clear messages
5. **Don't modify files** outside your scope
6. **Ask questions** if anything is unclear
7. **Update progress** in `COORDINATION.md`

---

## 📈 Estimated Timeline

**Parallel Execution (5 sessions):**
- Day 1: Agents 1, 2, 3, 5 start
- Day 2: Agent 1 completes, Agent 4 starts
- Day 3: All agents complete, begin merging
- Day 4: Integration testing and deployment
- **Total: 4 days**

**Sequential Execution (1 session):**
- Week 1: Agents 1 + 2 (2-3 days)
- Week 2: Agents 3 + 5 (1-2 days)
- Week 3: Agent 4 + Integration (2-3 days)
- **Total: 1-2 weeks**

---

## 💰 Cost Estimate

Based on $931 available credits:

**Parallel Execution:**
- 5 agents × 3-5 hours avg = 15-25 hours total
- Estimated cost: $150-250
- **Remaining credits: $681-781**

**Sequential Execution:**
- Same work done serially
- Estimated cost: $150-250
- **Remaining credits: $681-781**

*Note: Parallel is faster, same cost*

---

## ✅ Success Criteria

The multi-agent workflow is successful when:

- [ ] All 5 agent prompts completed
- [ ] All branches merged to main
- [ ] All tests passing (80%+ coverage)
- [ ] Photos persist on Railway
- [ ] Security audit complete
- [ ] CI/CD pipeline running
- [ ] Performance benchmarks met
- [ ] Application deployed to production
- [ ] No critical bugs or regressions

---

## 🆘 Getting Help

### If You Get Stuck

1. **Re-read the agent prompt** - Most questions are answered there
2. **Check `COORDINATION.md`** - See if other agents have dependencies
3. **Review `GIT_WORKFLOW.md`** - Git issues have solutions there
4. **Ask Claude** - "I'm stuck on [specific step], what should I do?"

### Common Issues

**"I don't understand the task"**
- Read the "Mission Objective" section in your prompt
- Review the "Step-by-Step Tasks"
- Look at the code examples provided

**"Tests are failing"**
- Agent 1 creates the tests, others run them
- Make sure Agent 1 completed before running CI (Agent 4)
- Run `pytest -v` to see specific failures

**"Git conflicts"**
- See `GIT_WORKFLOW.md` → Handling Merge Conflicts
- Follow the recommended merge order
- When in doubt, ask for help before force-pushing

---

## 📞 Contact

**Project Lead:** [Your name/contact]
**Repository:** https://github.com/Dparent97/ship-MTA-draft
**Documentation:** See parent README.md and ENGINEER_TASKS.md

---

**Last Updated:** 2025-11-17
**Version:** 1.0
**Status:** Ready for use
