#!/usr/bin/env python3
import subprocess
import sys
import webbrowser
import time
import shutil
import os
from pathlib import Path

def main():
    print("🚀 Starting Documentation Server...")

    # 1. Resolve paths
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent
    
    # Virtual root setup
    temp_dir = Path("/tmp/ps_docs_build")
    docs_root = temp_dir / "docs_root"
    config_file_path = temp_dir / "mkdocs.yml"

    print(f"📦 Building virtual docs root at {docs_root}...")

    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)
    docs_root.mkdir()

    # 2. Mirror everything in the repo into the docs_root
    items_to_link = [
        "ARCHITECTURE.md",
        "CONTRIBUTING.md",
        "REQUIREMENTS.md",
        "INFRASTRUCTURE.md",
        "TESTING.md",
        "docs",
        "planning",
        "blueprints", # RENAMED from templates
    ]

    for item in items_to_link:
        src = project_root / item
        dst = docs_root / item
        if src.exists():
            try:
                os.symlink(src, dst)
            except OSError as e:
                print(f"⚠️ Could not link {item}: {e}")

    # Special case: MkDocs needs an 'index.md'. 
    index_md = docs_root / "index.md"
    if not index_md.exists():
        os.symlink(project_root / "ARCHITECTURE.md", index_md)

    # 3. Read and Patch mkdocs.yml
    src_config = project_root / "mkdocs.yml"
    with open(src_config, "r") as f:
        config_lines = f.readlines()
    
    # Filter out existing nav
    new_config_lines = []
    skip_nav = False
    for line in config_lines:
        stripped = line.strip()
        if stripped.startswith("nav:"):
            skip_nav = True
            continue
        if skip_nav and stripped and not line.startswith(" "):
            skip_nav = False
        
        if not skip_nav:
            new_config_lines.append(line)

    # Define the CORRECT navigation mapping
    navigation = """
nav:
  - Home: index.md
  - Architecture: ARCHITECTURE.md
  - Contributing: CONTRIBUTING.md
  - Planning:
      - Board: planning/BOARD.md
      - Requirements: REQUIREMENTS.md
      - Hierarchy: docs/standards/agile_workflow.md
  - Standards:
      - API: docs/standards/api_standards.md
      - Coding: docs/standards/coding-guidelines.md
      - Testing: docs/standards/testing_traceability.md
      - Monitoring: docs/standards/monitoring.md
      - Security: docs/standards/security.md
  - Decisions:
      - Overview: docs/decisions/0001-record-architecture-decisions.md
  - Templates:
      - PRD: blueprints/prd.md
"""
    
    final_config = "".join(new_config_lines)
    final_config += "\ndocs_dir: docs_root\nuse_directory_urls: false\n"
    final_config += navigation
    
    with open(config_file_path, "w") as f:
        f.write(final_config)

    # 4. Run server
    cmd = [
        "uvx",
        "--from", "mkdocs",
        "--with", "mkdocs-material",
        "--with", "pymdown-extensions",
        "mkdocs", "serve",
        "-f", str(config_file_path)
    ]

    try:
        process = subprocess.Popen(cmd, cwd=temp_dir)
        print("⏳ Waiting for server...")
        time.sleep(2)
        webbrowser.open("http://127.0.0.1:8000/index.html")
        process.wait()
    except KeyboardInterrupt:
        process.terminate()

if __name__ == "__main__":
    main()
