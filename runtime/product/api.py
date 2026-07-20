from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, ConfigDict, Field

from .service import ConstraintOSProductService, ProductServiceError
from .store import FileJobStore, JobStoreError


class CreateJobBody(BaseModel):
    model_config = ConfigDict(extra="allow")

    request_text: str = Field(min_length=1)
    title: str | None = None
    job_id: str | None = None
    run_research: bool = False


class ClarificationBody(BaseModel):
    model_config = ConfigDict(extra="allow")

    run_research: bool = False


def create_service() -> ConstraintOSProductService:
    root = Path(os.environ.get("CONSTRAINTOS_JOB_ROOT", "runs/product-jobs")).resolve()
    return ConstraintOSProductService(FileJobStore(root))


app = FastAPI(
    title="ConstraintOS Image Jobs",
    version="0.1.0",
    description=(
        "Persistent request-to-research-to-generation orchestration for source-backed technical imagery."
    ),
)


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "constraintos-image-jobs",
        "job_root": str(create_service().store.root),
    }


@app.get("/api/jobs")
def list_jobs(limit: int = Query(default=100, ge=1, le=500)) -> list[dict[str, Any]]:
    return create_service().list_jobs(limit=limit)


@app.post("/api/jobs", status_code=201)
def create_job(body: CreateJobBody) -> dict[str, Any]:
    payload = body.model_dump(exclude_none=True)
    run_research = bool(payload.pop("run_research", False))
    service = create_service()
    try:
        job = service.create_job(payload, run_research=run_research)
        return service.get_job(job.job_id, include_events=True)
    except (ProductServiceError, JobStoreError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str, include_events: bool = True) -> dict[str, Any]:
    try:
        return create_service().get_job(job_id, include_events=include_events)
    except JobStoreError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/jobs/{job_id}/research")
def research_job(job_id: str) -> dict[str, Any]:
    service = create_service()
    try:
        job = service.run_research(job_id)
        return service.get_job(job.job_id, include_events=True)
    except JobStoreError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ProductServiceError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.post("/api/jobs/{job_id}/clarification")
def clarify_job(job_id: str, body: ClarificationBody) -> dict[str, Any]:
    payload = body.model_dump(exclude_none=True)
    run_research = bool(payload.pop("run_research", False))
    service = create_service()
    try:
        job = service.resume_after_clarification(
            job_id,
            payload,
            run_research=run_research,
        )
        return service.get_job(job.job_id, include_events=True)
    except JobStoreError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ProductServiceError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/api/jobs/{job_id}/artifacts/{artifact_key}")
def get_artifact(job_id: str, artifact_key: str) -> FileResponse:
    service = create_service()
    try:
        job = service.store.load(job_id)
    except JobStoreError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    configured = job.artifacts.get(artifact_key)
    if not configured:
        raise HTTPException(status_code=404, detail=f"Artifact not found: {artifact_key}")
    path = Path(configured).resolve()
    workspace = service.store.workspace_for(job_id).resolve()
    try:
        path.relative_to(workspace)
    except ValueError as exc:
        raise HTTPException(status_code=403, detail="Artifact path is outside the job workspace") from exc
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"Artifact file is missing: {artifact_key}")
    return FileResponse(path, filename=path.name)


INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ConstraintOS Image Jobs</title>
  <style>
    :root { color-scheme: light dark; font-family: Inter, system-ui, sans-serif; }
    body { margin: 0; background: Canvas; color: CanvasText; }
    main { max-width: 1120px; margin: 0 auto; padding: 32px 20px 80px; }
    h1 { margin-bottom: 6px; }
    .subtitle { opacity: .72; margin-top: 0; }
    .grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(320px, .8fr); gap: 20px; }
    .card { border: 1px solid color-mix(in srgb, CanvasText 18%, transparent); border-radius: 14px; padding: 18px; background: color-mix(in srgb, Canvas 95%, CanvasText 5%); }
    textarea { width: 100%; min-height: 210px; box-sizing: border-box; resize: vertical; padding: 12px; border-radius: 9px; border: 1px solid color-mix(in srgb, CanvasText 24%, transparent); font: inherit; }
    button { padding: 10px 14px; border-radius: 9px; border: 0; font-weight: 650; cursor: pointer; }
    button.primary { background: AccentColor; color: AccentColorText; }
    button.secondary { border: 1px solid color-mix(in srgb, CanvasText 24%, transparent); background: transparent; color: inherit; }
    .actions { display: flex; align-items: center; gap: 12px; margin-top: 12px; flex-wrap: wrap; }
    .job { padding: 12px 0; border-bottom: 1px solid color-mix(in srgb, CanvasText 12%, transparent); }
    .job:last-child { border-bottom: 0; }
    .job-title { font-weight: 700; }
    .meta { font-size: .86rem; opacity: .7; }
    pre { white-space: pre-wrap; overflow-wrap: anywhere; max-height: 560px; overflow: auto; padding: 14px; border-radius: 10px; background: color-mix(in srgb, Canvas 88%, CanvasText 12%); }
    .status { display: inline-block; padding: 3px 8px; border-radius: 99px; font-size: .78rem; border: 1px solid currentColor; }
    .error { color: #d44; }
    @media (max-width: 820px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
<main>
  <h1>ConstraintOS Image Jobs</h1>
  <p class="subtitle">Turn a new technical-image request into a persistent, research-backed production job.</p>
  <div class="grid">
    <section class="card">
      <h2>New image job</h2>
      <textarea id="request" placeholder="Describe the image, required visible features, viewpoint, style, prohibited elements, and publication needs."></textarea>
      <div class="actions">
        <label><input id="research" type="checkbox"> Run live research immediately</label>
        <button class="primary" id="create">Create job</button>
      </div>
      <p id="message" class="meta"></p>
    </section>
    <section class="card">
      <div class="actions" style="justify-content:space-between;margin-top:0">
        <h2 style="margin:0">Recent jobs</h2>
        <button class="secondary" id="refresh">Refresh</button>
      </div>
      <div id="jobs"></div>
    </section>
  </div>
  <section class="card" style="margin-top:20px">
    <div class="actions" style="justify-content:space-between;margin-top:0">
      <h2 style="margin:0">Selected job</h2>
      <button class="secondary" id="runResearch" hidden>Run research</button>
    </div>
    <pre id="detail">Select or create a job.</pre>
  </section>
</main>
<script>
let selectedJobId = null;
const detail = document.getElementById('detail');
const message = document.getElementById('message');
const runResearch = document.getElementById('runResearch');

async function api(path, options = {}) {
  const response = await fetch(path, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || JSON.stringify(data));
  return data;
}

async function loadJobs() {
  const jobs = await api('/api/jobs');
  const root = document.getElementById('jobs');
  root.innerHTML = '';
  if (!jobs.length) root.textContent = 'No jobs yet.';
  jobs.forEach(job => {
    const node = document.createElement('div');
    node.className = 'job';
    node.innerHTML = `<div class="job-title"></div><div class="meta"></div>`;
    node.querySelector('.job-title').textContent = job.title;
    node.querySelector('.meta').textContent = `${job.status} · ${job.subject || 'subject pending'} · ${job.job_id}`;
    node.onclick = () => showJob(job.job_id);
    root.appendChild(node);
  });
}

async function showJob(jobId) {
  selectedJobId = jobId;
  const job = await api(`/api/jobs/${encodeURIComponent(jobId)}?include_events=true`);
  detail.textContent = JSON.stringify(job, null, 2);
  runResearch.hidden = job.status !== 'research_ready';
}

document.getElementById('create').onclick = async () => {
  message.textContent = 'Creating job…';
  message.className = 'meta';
  try {
    const job = await api('/api/jobs', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        request_text: document.getElementById('request').value,
        run_research: document.getElementById('research').checked
      })
    });
    message.textContent = `Created ${job.job_id}`;
    await loadJobs();
    await showJob(job.job_id);
  } catch (error) {
    message.textContent = error.message;
    message.className = 'meta error';
  }
};

document.getElementById('refresh').onclick = loadJobs;
runResearch.onclick = async () => {
  if (!selectedJobId) return;
  runResearch.disabled = true;
  try {
    const job = await api(`/api/jobs/${encodeURIComponent(selectedJobId)}/research`, {method: 'POST'});
    detail.textContent = JSON.stringify(job, null, 2);
    await loadJobs();
  } catch (error) {
    detail.textContent = error.message;
  } finally {
    runResearch.disabled = false;
  }
};
loadJobs().catch(error => { detail.textContent = error.message; });
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML)
