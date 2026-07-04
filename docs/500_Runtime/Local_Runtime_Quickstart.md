# Local Runtime Quickstart

Status: Draft
Version: 1.0.0-alpha.22

## Purpose
This guide describes how to run ConstraintOS locally as a development runtime. This is not a production deployment guide.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest uvicorn
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e . pytest uvicorn
```

## Run Tests

```bash
pytest
```

## Run API Server

```bash
uvicorn constraintos.api_server:app --host 127.0.0.1 --port 8000
```

## Verify Health

```bash
curl http://127.0.0.1:8000/health
```

Expected status:

```json
{"status":"ok","service":"constraintos-api"}
```

## Boundaries

The local runtime is for development and dry-run execution. It does not provide authentication, tenancy, billing, durable queue storage, production worker scheduling, or SaaS hosting.
