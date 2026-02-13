# Security Testing Standards

This document outlines the mandatory security testing strategy for our product suite. It is designed to be modular; teams should select the modules relevant to their specific application context (e.g., Mobile, Payments, Public-Facing).

## Philosophy

We adopt a "Shift Left" approach to security. Security testing is not a final gate but a continuous process integrated into the CI/CD pipeline.

**Standards Alignment:**
*   **Web**: [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
*   **Mobile**: [OWASP Mobile Application Security Verification Standard (MASVS)](https://owasp.org/www-project-mobile-app-security/)
*   **Container**: [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)

---

## 1. Automated Pipeline Testing (Mandatory for All)

These tests must run automatically on every Pull Request.

### 1.1 Software Composition Analysis (SCA)
*   **Objective**: Detect known vulnerabilities in third-party dependencies.
*   **Tools**:
    *   **Frontend/Mobile**: `npm audit` / `yarn audit` (Basic), or `OWASP Dependency-Check` (Comprehensive).
    *   **Backend**: `pip-audit` (Recommended) or `safety`.
    *   **Platform** (Optional): `Snyk` or `GitHub Dependabot`.
    *   **Comparison**: `npm audit` is fast and checks `package-lock.json` against the registry. `OWASP Dependency-Check` is heavier but analyzes actual archives for a deeper scan.
*   **Failure Condition**: Any vulnerability with severity `HIGH` or `CRITICAL` must block the build.

### 1.2 Static Application Security Testing (SAST)
*   **Objective**: Analyze source code for insecure patterns (e.g., hardcoded secrets, injection flaws) without executing it.
*   **Tools**:
    *   **Secrets Detection**: `trufflehog` (Deep history scan) or `Gitleaks` (Fast/Pre-commit).
    *   **Code Scanning**: `semgrep` (Recommended for CI speed), `SonarQube` (Quality + Security), or `CodeQL`.
    *   **Backend Specific**: `Bandit` (Python).
    *   **Frontend Specific**: `ESLint` (with `eslint-plugin-security`).
    *   **Comparison**: `semgrep` is fast and rule-based (great for linting). `CodeQL` performs deep semantic analysis to find complex data-flow issues (e.g., input -> function -> SQL) that `semgrep` might miss.
*   **Key Checks**:
    *   No hardcoded credentials.
    *   No usage of `dangerouslySetInnerHTML` (React) without sanitization.
    *   No raw SQL queries (use ORM).
*   **Failure Condition**: Any findings from SAST scanners (Semgrep, Bandit) must block the build.

### 1.3 Container Security
*   **Objective**: Ensure the Docker image and runtime are secure.
*   **Tools**: `trivy` (Recommended - covers OS + Config), or `grype` (OS only) + `hadolint` (Config).
    *   **Comparison**: `trivy` is a "Swiss Army Knife" that checks OS packages AND misconfigurations (like running as root). `grype` is excellent for CVEs but cannot detect config issues, requiring `hadolint` to fill the gap.
*   **Policy**:
    *   **Execution Order**: This scan **MUST** run after the image is built to verify the current filesystem.
    *   Base images must be minimal (Distroless/Alpine).
    *   Containers must NOT run as `root`.
    *   Scan results must be clean of `CRITICAL` OS vulnerabilities.
*   **Vulnerability Management**: 
    *   **Actionable Feedback**: The scan **MUST** use the `--ignore-unfixed` flag. This filters out vulnerabilities that the team cannot fix (because no patch exists) but ensures that the build fails **immediately** as soon as an upstream fix is available.
    *   **Manual Exclusions**: In exceptional cases where a fix *is* available but cannot be applied (e.g., breaking changes), the CVE must be documented in a `.trivyignore` file with a justification.
    *   The build **MUST** fail if any unignored, fixed vulnerabilities are detected (use `--exit-code 1`).

---

## 2. Dynamic & Manual Testing Modules

Select the modules applicable to your application features.

### Module A: Web Applications (React)
*Applicable to: All browser-based interfaces.*

- [ ] **Cross-Site Scripting (XSS)**:
    - Verify that user input reflected in the UI is properly escaped.
    - Test: Attempt to inject `<script>alert(1)</script>` in all input fields.
- [ ] **Content Security Policy (CSP)**:
    - Verify `Content-Security-Policy` header is present and restricts script sources.
    - Test: Ensure inline scripts are blocked unless explicitly allowed (avoid `unsafe-inline`).
- [ ] **State Management**:
    - Verify sensitive data (tokens, PII) is NOT stored in `localStorage` or `sessionStorage` (use HttpOnly cookies or in-memory storage).
    - Test: Inspect Application Storage after login.

### Module B: API Security (FastAPI)
*Applicable to: All backend services.*

- [ ] **Broken Object Level Authorization (BOLA/IDOR)**:
    - Verify users cannot access resources belonging to others by changing the ID in the URL.
    - Test: Login as User A, attempt to `GET /api/orders/{User_B_Order_ID}`.
- [ ] **Mass Assignment**:
    - Verify users cannot update restricted fields (e.g., `is_admin`, `balance`) by including them in the payload.
    - Test: `POST /profile` with `{"role": "admin"}`.
- [ ] **Rate Limiting**:
    - Verify APIs have rate limits to prevent abuse.
    - Test: Send 100 requests in 1 second; expect `429 Too Many Requests`.

### Module C: Mobile Applications (React Native)
*Applicable to: Android and iOS apps.*

- [ ] **Insecure Data Storage**:
    - Verify no sensitive data is stored in `AsyncStorage` or unencrypted Plist/SharedPreferences.
    - Test: Dump the app sandbox on a rooted/jailbroken device.
- [ ] **Deep Links**:
    - Verify deep link handlers validate input to prevent malicious navigation or state changes.
- [ ] **Biometrics**:
    - If used, verify biometric auth falls back securely to PIN/Password and does not bypass server-side auth.
- [ ] **Tooling**:
    - Run **MobSF** (Mobile Security Framework) against the compiled binary (APK/IPA).

### Module D: Public Internet Exposure
*Applicable to: Apps accessible via the public internet.*

- [ ] **TLS Configuration**:
    - Verify SSL/TLS is enforced (no plain HTTP).
    - Test: SSLLabs grade should be A or A+.
- [ ] **Security Headers**:
    - Verify `Strict-Transport-Security` (HSTS), `X-Frame-Options`, and `X-Content-Type-Options` are present.

### Module E: Payments & Financial Data
*Applicable to: Apps processing payments or handling financial records.*

- [ ] **PCI-DSS Scope**:
    - Verify no credit card numbers (PAN) are stored or logged by the application.
    - Test: Search logs for regex matching credit card patterns.
- [ ] **Transaction Integrity**:
    - Verify payment amounts cannot be tampered with client-side.
    - Test: Intercept request and change `amount: 100` to `amount: 1`.

### Module F: User Content & Uploads
*Applicable to: Apps allowing file uploads.*

- [ ] **Malware Scanning**:
    - Verify all uploaded files are scanned for malware before being made accessible.
- [ ] **File Type Validation**:
    - Verify strict allow-listing of file extensions and MIME types.
    - Test: Upload `image.php` or `script.sh` disguised as an image.
- [ ] **Storage**:
    - Verify uploaded files are served from a separate domain (e.g., S3 bucket) to prevent same-origin XSS.

---

## 3. Penetration Testing Schedule

*   **Internal Apps**: Annual automated scan + manual review of critical flows.
*   **Public/Financial Apps**: External Penetration Test required:
    *   Annually.
    *   Before major releases (v1.0, v2.0).