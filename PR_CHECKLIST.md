# PR_CHECKLIST.md

# Pull Request Checklist

Before merging your Pull Request, please ensure the following:

- [ ] Run tests: `pytest -q`
- [ ] Run smoke tests: `bash scripts/smoke_test.sh`
- [ ] Ensure no secrets in diffs
- [ ] Keep commits small and descriptive
- [ ] Assign reviewer and merge when green

# Merge commands

```bash
git checkout main
git pull origin main
git checkout feature/orchestrator-small-steps
git rebase main
git push --force-with-lease origin feature/orchestrator-small-steps
# Create PR via GitHub UI and merge after review
```