# Codespaces Beta 1 Workflow

## Purpose
This guide defines how to continue Beta 1 stabilization using GitHub Codespaces instead of a local machine.

## Open Codespaces

1. Open the repository in GitHub.
2. Switch to the `phase-1-cli-tooling` branch.
3. Select **Code**.
4. Select **Codespaces**.
5. Create a new Codespace on `phase-1-cli-tooling`.

The devcontainer will install ConstraintOS in editable mode and install the core test/runtime dependencies.

## First Commands

Run these from the Codespaces terminal:

```bash
python --version
pip install -e . pytest pyyaml jsonschema fastapi uvicorn
pytest
constraintos registry-check
constraintos id-audit
constraintos repo-health
constraintos validate
```

## Stabilization Loop

1. Run the failing command.
2. Copy the exact terminal output.
3. Paste it into ChatGPT.
4. Apply the recommended patch in Codespaces.
5. Re-run the command.
6. Commit only once the command passes.

## Recommended Commit Style

Use small but coherent commits:

```bash
git status
git add .
git commit -m "Beta 1: fix repository validation issues"
git push
```

## Beta 1 Goal

The working branch should eventually pass:

```bash
pytest
constraintos registry-check
constraintos id-audit
constraintos repo-health
constraintos validate
```

## Notes

Codespaces is now the preferred workflow for broad refactors, test-driven fixes, generated documentation, and CI stabilization.
