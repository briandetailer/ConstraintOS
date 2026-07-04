# Deployment Boundaries

Status: Draft
Version: 1.0.0-alpha.22

## Purpose
This document defines what belongs to the local runtime, production runtime, enterprise deployment, and future SaaS platform.

## Local Runtime

Owns:

- local API process
- dry-run endpoint testing
- in-memory queue scaffolding
- local artifact store
- local test execution

Does not own:

- authentication
- billing
- tenancy
- production queue durability
- customer management
- SaaS subscription lifecycle

## Production Runtime

Owns:

- API process deployment
- durable job queue
- worker processes
- observability
- operational health
- persistent artifact storage

Does not own:

- kernel correctness semantics
- CSL meaning
- approval rules
- validation truth
- SaaS commercial policy

## Kernel

Owns:

- specification semantics
- compiler behavior
- validation behavior
- lifecycle rules
- review gates
- patch generation
- artifact traceability

## Future Platform

Owns:

- users
- organizations
- roles and permissions
- subscriptions
- billing
- tenant isolation
- encryption/tokenization policy
- hosted UI

## Principle
Deployment layers may invoke ConstraintOS, but they must not redefine what a valid artifact means.
