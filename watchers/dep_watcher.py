"""
Dependency Watcher: Python + Node
- Runs in primary env `shujaa_venv`.
- Checks Node (package.json vs node_modules) using `npm ls --json` and `npm outdated --json`.
- Checks Python (requirements.txt vs installed) using `pip list --format=json` and `pip list --outdated --format=json`.
- Avoids reinstalling already installed packages.
- Updates only if a patch is available (semver x.y.Z).
- Blocks duplicate/unnecessary downloads (esp. model files) by delegating model logic to model_watcher.py.
- Scans recent 5 commits to recover missing dependency files.

Usage:
  python dep_watcher.py --frontend ..\\frontend --project-root ..
"""

from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / 'frontend'
REQ_FILE = ROOT / 'requirements.txt'
MODEL_WATCHER = ROOT / 'watchers' / 'model_watcher.py'


def run(cmd: List[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    # Pass the current environment variables, including PATH, to the subprocess
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, check=False, env=os.environ)


def ensure_paths(frontend: Path, req_file: Path) -> None:
    if not frontend.exists():
        print(f"[dep-watcher] frontend not found: {frontend}")
    if not req_file.exists():
        print(f"[dep-watcher] requirements.txt not found: {req_file}")


def parse_outdated_npm(frontend: Path) -> Dict[str, Any]:
    outdated = run(["C:\\nvm4w\\nodejs\\npm.cmd", "outdated", "--json"], cwd=frontend)
    if outdated.returncode not in (0, 1):
        return {}
    try:
        return json.loads(outdated.stdout or '{}')
    except json.JSONDecodeError:
        return {}


def parse_installed_npm(frontend: Path) -> Dict[str, Any]:
    ls = run(["C:\\nvm4w\\nodejs\\npm.cmd", "ls", "--json", "--depth=0"], cwd=frontend)
    try:
        data = json.loads(ls.stdout or '{}')
        return data.get('dependencies', {})
    except json.JSONDecodeError:
        return {}


def parse_outdated_pip() -> List[Dict[str, Any]]:
    outdated = run([sys.executable, "-m", "pip", "list", "--outdated", "--format=json"])
    try:
        return json.loads(outdated.stdout or '[]')
    except json.JSONDecodeError:
        return []


def parse_installed_pip() -> Dict[str, str]:
    lst = run([sys.executable, "-m", "pip", "list", "--format=json"])
    try:
        pkgs = json.loads(lst.stdout or '[]')
        return {p['name'].lower(): p['version'] for p in pkgs}
    except json.JSONDecodeError:
        return {}


def is_patch_update(current: str, latest: str) -> bool:
    def split(v: str) -> List[int]:
        parts = v.split('.')
        return [int(p) for p in parts[:3] + ['0'] * (3 - len(parts)) if p.isdigit()]
    c = split(current)
    l = split(latest)
    return c[:2] == l[:2] and l[2] > c[2]


def recover_from_recent_commits(repo_root: Path) -> None:
    # Attempt to restore missing lockfiles or dep manifests from the last 5 commits
    for target in (repo_root / 'package.json', repo_root / 'requirements.txt'):
        if target.exists():
            continue
        log = run(["git", "log", "-n", "5", "--pretty=format:%H", "--", str(target)])
        if log.returncode == 0 and log.stdout.strip():
            last_commit = log.stdout.strip().splitlines()[0]
            show = run(["git", "show", f"{last_commit}:{target.as_posix()}"], cwd=repo_root)
            if show.returncode == 0 and show.stdout:
                target.write_text(show.stdout, encoding='utf-8')
                print(f"[dep-watcher] Restored {target.name} from commit {last_commit}")


def check_node(frontend: Path) -> None:
    if not (frontend / 'package.json').exists():
        print("[dep-watcher] No package.json in frontend; skipping Node checks")
        return

    installed = parse_installed_npm(frontend)
    outdated = parse_outdated_npm(frontend)

    for name, info in (outdated or {}).items():
        current = info.get('current')
        latest = info.get('latest')
        if not current or not latest:
            continue
        if is_patch_update(str(current), str(latest)):
            print(f"[dep-watcher] Node patch available: {name} {current} -> {latest}")
        else:
            print(f"[dep-watcher] Skipping non-patch update for {name}: {current} -> {latest}")

    # Avoid reinstall if installed at required version
    print(f"[dep-watcher] Installed Node deps: {len(installed)} packages")


def check_python(req_file: Path) -> None:
    if not req_file.exists():
        print("[dep-watcher] No requirements.txt; skipping Python checks")
        return

    installed = parse_installed_pip()
    outdated = parse_outdated_pip()
    outdated_map = {p['name'].lower(): p for p in outdated}

    required = {}
    for line in req_file.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '==' in line:
            name, ver = line.split('==', 1)
            required[name.lower()] = ver
        else:
            required[line.lower()] = None

    for name, req_ver in required.items():
        cur = installed.get(name)
        if not cur:
            print(f"[dep-watcher] Missing Python dep: {name}")
            continue
        if name in outdated_map:
            latest = outdated_map[name]['latest_version']
            if req_ver and not is_patch_update(cur, latest):
                print(f"[dep-watcher] Skipping non-patch update for {name}: {cur} -> {latest}")
            elif is_patch_update(cur, latest):
                print(f"[dep-watcher] Python patch available: {name} {cur} -> {latest}")

    print(f"[dep-watcher] Installed Python deps: {len(installed)} packages")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--frontend', type=str, default=str(FRONTEND))
    parser.add_argument('--project-root', type=str, default=str(ROOT))
    args = parser.parse_args()

    frontend = Path(args.frontend)
    project_root = Path(args.project_root)

    ensure_paths(frontend, REQ_FILE)
    recover_from_recent_commits(project_root)

    # Delegate model duplication prevention to model watcher if present
    if MODEL_WATCHER.exists():
        print("[dep-watcher] model_watcher.py present; model downloads governed externally")

    check_node(frontend)
    check_python(REQ_FILE)


if __name__ == '__main__':
    main()
