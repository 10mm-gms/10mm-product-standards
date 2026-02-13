# 12. App Execution Standards

Date: 2025-12-21

## Status

Accepted

## Context

Our production containers currently carry unnecessary weight and security risks. Standard base images (like `python:3.12-slim`) include a full shell, package managers (`apt`, `pip`), and system utilities that are not required at runtime. This increases the attack surface (CVEs) and makes compliance auditing more difficult.

We need a standard for containerizing applications that prioritizes security and minimalism.

## Decision

We will standardize on **Distroless** container images for all production deployments.

### 1. Base Image
*   **Principle**: Production images should contain *only* the application and its direct runtime dependencies.
*   **Implementation**: Use `gcr.io/distroless/cc-debian12` (or the appropriate language variant) as the final stage in a multi-stage build.
    *   **Forbidden**: Do not use `alpine` (musl libc compatibility issues) or `slim` images (contains shell/apt) for the final stage.

### 2. Execution Strategy
*   **Principle**: Applications must execute directly, without a shell wrapper.
*   **Implementation**: Use `ENTRYPOINT` with the `vector` (JSON array) syntax pointing directly to the interpreter.
    *   Example: `ENTRYPOINT ["/usr/local/bin/python3.12", "-m", "uvicorn", ...]`
    *   **Implication**: Environment variable expansion (`$PORT`) in the command line **will not work** because there is no shell. Variables must be handled by the application code or the platform.

### 3. Build Process
*   **Principle**: decouple build-time tools from run-time artifacts.
*   **Implementation**: Heavy use of **Multi-Stage Builds**.
    *   **Builder Stage**: Install compilers, build tools (`uv`, `npm`), and headers.
    *   **Final Stage**: Copy *only* the compiled artifacts, virtual environment, and necessary shared libraries from the builder.

## Consequences

*   **Positive**: **Security**. drastically reduced attack surface. No shell means remote code execution (RCE) vulnerabilities are significantly harder to exploit.
*   **Positive**: **Compliance**. Fewer installed packages mean fewer CVE noise in security scans.
*   **Positive**: **Size**. Smaller images reduce storage costs and pull times.
*   **Negative**: **Debugging**. You cannot `kubectl exec` or `docker run -it` into the container with a shell. Debugging requires using "debug" variants of the image or ephemeral debug containers provided by the orchestration platform.
