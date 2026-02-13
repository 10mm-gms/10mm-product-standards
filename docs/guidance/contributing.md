# Contributing Guidelines

## Viewing Documentation
To view these standards as a proper website with search and navigation:
```bash
./scripts/docs.py
```
This will start a local server at `http://localhost:8000`.

## Versioning

### Standards Versioning
All blueprints and standards are versioned (current: **v0.1**). 
*   When copying a blueprint into a new project, ensure the version comment (e.g., `<!-- Standard Version: 0.1 -->`) is preserved.
*   This allows us to track which version of the standards a project is following.

### Product Versioning
We use **Semantic Versioning (SemVer) 2.0.0** for all product codebases, libraries, and APIs. 
*   See [ADR 0016: Adopt Semantic Versioning](../decisions/0016-adopt-semantic-versioning.md) for detailed rules.
*   Version increments are driven by **Conventional Commits**.

## Philosophy
We treat documentation and standards as first-class citizens. AI Agents are considered core contributors and consumers of this documentation.

## Development Workflow
1.  **Read the Docs**: Check `ARCHITECTURE.md` and `docs/decisions/` before starting major work.
2.  **Plan**: Create a Plan/RFC (or use the Agent's `implementation_plan.md`) for significant changes.
3.  **Code**: Follow standards in `docs/standards/`.
4.  **Verify**: Ensure tests pass and the code matches the design.

## Development Environment Setup (Linux Mint 22 / Ubuntu 24.04)
To generate release images and run the full test suite, you must install the following tools.

### 1. System Dependencies
Install essential build tools.
```bash
sudo apt update
sudo apt install -y curl git build-essential
```

### 2. Python & `uv` (Standard)
We use `uv` for extremely fast Python package management. 
> [!NOTE]
> `uv` is NOT currently available in the official Debian/Ubuntu repositories. It must be installed via the standalone script or `pipx`.

*   **Install**: [Official Guide](https://docs.astral.sh/uv/getting-started/installation/)
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
*   **Verify**:
    ```bash
    uv --version
    # Output should include "uv x.x.x"
    ```
> [!TIP]
> If `uv` is not found after installation, ensure `~/.local/bin` is in your `PATH`. You can add it by adding `export PATH="$HOME/.local/bin:$PATH"` to your `~/.bashrc` or `~/.zshrc`.

### 3. Node.js (via `nvm`)
We use `nvm` to manage Node versions. Do not use `apt install nodejs` as the repository versions are often outdated.
> [!NOTE]
> `nvm` is NOT available in the official Debian/Ubuntu repositories. 
> 
> **Important**: The installation script requires a shell profile file (like `~/.bashrc`) to exist. If your system is missing one, create it first: `touch ~/.bashrc`.

*   **Install**: [Official Guide](https://github.com/nvm-sh/nvm#installing-and-updating)
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    # Restart terminal
    nvm install --lts
    nvm use --lts
    ```
*   **Verify**:
    ```bash
    node -v
    # Output: v20.x.x (or newer)
    ```

### 4. Docker Engine (Official)
We need Docker for building images and running `TestContainers` (integration tests).
*   **Install**: [Official Guide](https://docs.docker.com/engine/install/ubuntu/)
    ```bash
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      noble stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    
    # Install
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```
*   **Post-Install (Non-Root)**: [Linux Post-install](https://docs.docker.com/engine/install/linux-postinstall/)
    ```bash
    sudo groupadd docker
    sudo usermod -aG docker $USER
    # Log out and back in of the whole desktop session, not just the terminal
    ```
*   **Verify**:
    ```bash
    docker run hello-world
    ```

### 5. Playwright (Browsers)
After installing Node, install the browser binaries for E2E testing. 
```bash
npx playwright install --with-deps
```
> [!TIP]
> If your build fails during E2E testing because browsers are missing, ensure Chromium is installed:
> ```bash
> npx playwright install chromium
> ```

### 6. Security Scanning Tools
The local pipeline includes mandatory security scans. Some tools are managed by `uv` or `npm`, while others require Docker.

*   **Python (Managed by `uv`)**: `pip-audit` and `bandit` are included in the dev dependencies.
*   **Frontend (Managed by `npm`)**: `eslint-plugin-security` is included in dev dependencies.
*   **External (Requires Docker)**:
    *   **Semgrep**: Used for Static Analysis.
    *   **Trivy**: Used for Container and Dependency scanning.
    Ensure your user has permissions to run Docker commands (see Section 4).

### 7. Project Dependencies
Once the system tools are installed, you must install the dependencies for the specific project you are working on.

*   **Python (Backend)**:
    ```bash
    uv sync
    ```
*   **Node.js (Frontend & Mobile)**:
    ```bash
    # For Web
    cd src/frontend && npm install
    
    # For Mobile
    cd src/mobile && npm install
    ```

## Running the Application
Before you can run E2E tests or view the frontend, you must start the development servers.
```bash
make dev
```
This will start:
*   **Backend**: FastAPI at `http://localhost:8000`
*   **Frontend**: Vite at `http://localhost:5173`

## The Local Pipeline
Before committing code, you should run the local pipeline to ensure everything is functioning correctly. We use `make` as the standard interface.

*   **Build & Check**: `./build.sh` (or `make lint test build`)
*   **Scoped Pipeline**: `./build.sh [all|container|mobile]`
*   **Format code**: `make fmt` or `make fmt-mobile`
*   **Run tests**: `make test` (Full), `make test-web`, or `make test-mobile`
*   **Run E2E tests**: `make test-e2e` (for web)

## Mobile Development Setup (Android)
To develop and test mobile applications using **Expo** and **React Native**, additional tools are required for local emulation and building.

### 1. Java Development Kit (JDK)
We require **JDK 17**. Modern React Native/Expo builds are highly sensitive to the Java version.
```bash
sudo apt update
sudo apt install -y openjdk-17-jdk
# Ensure JAVA_HOME points to Java 17
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

### 2. Android SDK & Emulator
Required for local development and E2E testing.
1. **Android Studio**:
    1. Download from https://developer.android.com/studio
    1. Expand tarball
    1. Run android-studio/bin/studio.sh
    1. Follow the installation wizard. Once it starts the welcome screen shows. Click **More Actions** -> **SDK Manager**
    1. Install the Android SDK Platform 34 (Target API). Choose the base SDK, not the versions with -ext after them. *Note: API 36+ is currently unstable with Maestro.*
    1. Back at the welcome screen click **More Actions** -> **Virtual Device Manager**
    1. Click **Create Device**
    1. Select **Pixel 7** (or any standard phone profile)
    1. Click **Next**
    1. Select the system image for API 34. Let it download.
    1. Click **Next** and rename the AVD to `Medium_Phone_API_34`.
    1. Create an emulator with high resources to ensure ADB responsiveness:
        *   **RAM**: 4GB
        *   **Cores**: 4
3.  **Environment Variables**: Add the following to your `~/.bashrc`:
    ```bash
    export ANDROID_HOME=$HOME/Android/Sdk
    export PATH=$PATH:$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/latest/bin:$HOME/.maestro/bin
    # IMPORTANT: Bypass proxy for local traffic to avoid Maestro/gRPC timeouts
    export NO_PROXY="localhost,127.0.0.1,::1"
    ```

### 3. Expo Account & CLI
We use **EAS (Expo Application Services)** for cloud builds.
1.  **Create Account**: Sign up at [expo.dev](https://expo.dev).
2.  **Login**: Once in the project, run:
    ```bash
    npx eas login
    ```
3.  **Expo Go**: Install the **Expo Go** app on your physical Android device from the Play Store for live testing.

### 4. Maestro (Mobile E2E)
We use **Maestro** for automated mobile testing.
*   **Install**: [Official Guide](https://maestro.mobile.dev/getting-started/installing-maestro)
    ```bash
    curl -Ls "https://get.maestro.mobile.dev" | bash
    ```
*   **Verify**:
    ```bash
    maestro --version
    ```

> [!NOTE]
> `make test-e2e` and `npx playwright test` are configured to automatically start the servers if they are not already running, but running `make dev` manually is recommended for active development.

This ensures that "Day 0" of moving to a remote CI tool (like GitLab/Jenkins) is trivial, as it will simply call these same commands.

## Making Architectural Changes
If you clearly violate a standard or introduce a new technology, you **MUST** propose a new ADR (Architecture Decision Record).

1.  Copy the template from `docs/decisions/TEMPLATE.md`.
2.  Create a pull request with the new decision.

## Documentation Structure
*   `/docs/decisions`: Immutable records of *why* we did things.
*   `/docs/standards`: Living documents of *how* we do things (Coding style, Naming).
*   `ARCHITECTURE.md`: The map of the territory.
