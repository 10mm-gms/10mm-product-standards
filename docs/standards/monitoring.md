# Monitoring & Health Standard

To ensure an application is not just "running" but "functioning", we implement **Deep Health Checks** and standardized **Functioning Signals**.

## 1. Health Endpoints (The Probes)
Applications must expose the following HTTP endpoints. This standard is derived from the **Kubernetes (K8s) Probe Architecture**, but applies to any orchestrator (AWS Target Groups, GCP Health Checks).

### `/health/live` (Liveness)
*   **Question**: "Is the process running?"
*   **Check**: Simple 200 OK. No logic.
*   **Failure**: The process is deadlocked or crash-looping. **Action**: Restart Container.

### `/health/ready` (Readiness)
*   **Question**: "Are you ready to do work?"
*   **Check**: Deep check of critical dependencies.
    *   Can I query the *Primary Database*?
    *   Can I reach *Redis*?
    *   (Optional) Are critical downstream services reachable?
*   **Failure**: Dependency is down. **Action**: Stop sending traffic (remove from Load Balancer). Do NOT restart (restarting won't fix the database).
*   **UX**: This is the answer to "Is the app functioning?".

### `/health/startup` (Startup)
*   **Question**: "Has initialization finished?"
*   **Check**: Migrations run, caches warmed, models loaded.

## 2. The RED Method (Metrics)
To know *how well* it is functioning, every service must emit these three metrics (automatically via middleware):
1.  **Rate**: Request per second.
2.  **Errors**: % of 5xx responses. (This is your primary "Is it broken?" signal).
3.  **Duration**: P95/P99 Latency.

## 3. Semantic Monitoring (Synthetic Tests)
For critical flows (e.g., "User can checkout"), we do not rely solely on passive monitoring.
*   **Definition**: A "Synthetic Canter" runs a real script against the production environment every X minutes.
*   **Standard**: Use the same E2E tests (Playwright) defined in [Testing Traceability](testing_traceability.md).
*   **Alert**: If the "Login" synthetic fails, the app is down, even if `/health/ready` says the DB is up.

## Implementation Example (FastAPI)

```python
from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/health/live")
def live():
    return {"status": "ok"}

@app.get("/health/ready")
def ready(db = Depends(get_db)):
    try:
        # SELECT 1
        db.execute("SELECT 1")
    except Exception:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return {"status": "ready"}
## 4. Dynamic Observability
To debug production issues without service interruption or redeployment, applications SHOULD support dynamic configuration updates.

### Dynamic Log Control
Applications SHOULD expose an administrative endpoint to update the `LOG_LEVEL` at runtime for the entire process. This is particularly useful for setting a service to `DEBUG` for a short period to trace a single request.

*   **Security**: These endpoints MUST be restricted to administrative users or internal network access only.
*   **Consistency**: Updating the root logger should also update any silenced third-party loggers (like HTTP clients) to ensure the requested detail level is achieved.
