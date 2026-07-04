# Phase 15: Minimal API Server Scaffolding

Status: Complete Baseline
Version: 1.0.0-alpha.15

## Purpose
Phase 15 introduces the first minimal API server scaffold. The API server exposes selected kernel and runtime operations through a FastAPI application while preserving the principle that the API is a boundary, not the authority over correctness.

## Implemented Scope

- Minimal API server module
- FastAPI app factory
- Health endpoint
- Compile endpoint scaffold
- Validation endpoint stub
- Volume build dry-run endpoint
- API health response schema
- API validation stub response schema
- API server tests
- API examples
- FastAPI dependency
- Package version bumped to `1.0.0-alpha.15`

## Endpoint Baseline

- `GET /health`
- `POST /compile`
- `POST /validate`
- `POST /builds/volume`

## API Server Philosophy

The API server calls the kernel. It does not replace the kernel and does not redefine kernel semantics.

## Design Rules

1. API endpoints should delegate to existing kernel functions.
2. API endpoints should avoid duplicating correctness logic.
3. Validation remains stubbed until API payload persistence is formalized.
4. API server tests must avoid external services.
5. Authentication, authorization, tenancy, billing, and subscriptions remain out of scope.
6. This is a scaffold, not a production server.

## Recommended Phase 16

Phase 16 should introduce API persistence and job queue scaffolding:

1. In-memory job queue
2. Runtime job creation endpoint
3. Job status endpoint
4. Volume build queued job path
5. API-level job tests
6. Persistence boundary documentation
