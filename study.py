"""Does a real project's test suite break on a major upgrade, and can driftfix fix it?

    python study.py check <id>   # free: run tests before and after the upgrade
    python study.py fix <id>     # check, then run driftfix on a confirmed break
    python study.py report       # markdown summary of results/
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
WORK = Path(os.environ.get("STUDY_WORK", "/tmp/study"))
REPO, VENV, PLUGIN = WORK / "repo", WORK / "venv", WORK / "plugin"
PY, SKIP = VENV / "bin" / "python", WORK / "skip.json"
SECRETS = {"ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN", "GITHUB_TOKEN", "GH_TOKEN"}

# Excludes tests that already failed before the upgrade, so "after" is compared like for like.
PLUGIN_SRC = '''
import json, os
_skip = json.load(open(os.environ["STUDY_SKIP"]))
def pytest_ignore_collect(collection_path, config):
    rel = os.path.relpath(collection_path, config.rootpath)
    return True if rel in _skip["files"] else None
def pytest_collection_modifyitems(config, items):
    gone = [i for i in items if i.nodeid in _skip["ids"]]
    if gone:
        config.hook.pytest_deselected(items=gone)
        items[:] = [i for i in items if i.nodeid not in _skip["ids"]]
'''
TEST = (f"STUDY_SKIP={SKIP} PYTHONPATH={PLUGIN}:. {PY} -m pytest -q -rfE -p no:cacheprovider "
        "-p study_plugin -o addopts=''")


def sh(cmd: str, cwd: Path = WORK, timeout: int = 900, secrets: bool = False) -> tuple[int, str]:
    env = {k: v for k, v in os.environ.items() if v and (secrets or k not in SECRETS)}
    try:
        p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"


def version(package: str) -> str:
    code, out = sh(f"{PY} -c \"import importlib.metadata as m; print(m.version('{package}'))\"")
    return out.strip() if code == 0 else ""


def run_tests(skip: dict) -> dict:
    SKIP.write_text(json.dumps(skip))
    code, out = sh(TEST, REPO)
    counts = {k: int(n) for n, k in re.findall(r"(\d+) (passed|failed|errors?|skipped)", out.splitlines()[-1] if out else "")}
    failing = [line.split(" ", 1)[1].split(" - ")[0] for line in out.splitlines()
               if line.startswith(("FAILED ", "ERROR "))]
    return {"code": code, "counts": counts, "failing": failing, "tail": "\n".join(out.splitlines()[-40:])}


def install(c: dict) -> str | None:
    """Install the project as its own files describe. Returns an error string on failure."""
    reqs = [f for f in c["pinned_in"] if f.endswith(".txt") and (REPO / f).exists()]
    reqs += sorted(str(p.relative_to(REPO)) for p in REPO.glob("*requirements*.txt")
                   if "doc" not in p.name and str(p.relative_to(REPO)) not in reqs)
    for f in reqs:
        code, out = sh(f"uv pip install -q -p {PY} -r {f}", REPO)
        if code and f in c["pinned_in"]:
            return f"requirements {f}: {out[-500:]}"
    if (REPO / "setup.py").exists() or (REPO / "pyproject.toml").exists():
        for target in (".[test]", ".[tests]", ".[dev]", "."):
            if sh(f"uv pip install -q -p {PY} -e '{target}'", REPO)[0] == 0:
                break
    sh(f"uv pip install -q -p {PY} pytest")
    return None


def check(c: dict) -> dict:
    r = {k: c[k] for k in ("id", "repo", "package", "upgrade", "stars")}
    sh(f"rm -rf {WORK} && mkdir -p {PLUGIN}", ROOT)
    (PLUGIN / "study_plugin.py").write_text(PLUGIN_SRC)
    if sh(f"git clone -q --depth 1 https://github.com/{c['repo']} {REPO}")[0]:
        return {**r, "status": "clone_failed"}
    r["sha"] = sh("git rev-parse HEAD", REPO)[1].strip()
    sh(f"uv venv -q --seed -p {c['python']} {VENV}")
    if err := install(c):
        return {**r, "status": "install_failed", "error": err}
    r["old"] = version(c["package"])
    if not r["old"] or int(r["old"].split(".")[0]) >= int(re.search(r">=(\d+)", c["upgrade"])[1]):
        return {**r, "status": "not_on_old_version"}

    skip = {"ids": [], "files": []}
    first = run_tests(skip)
    if first["code"] == 5 or not first["counts"].get("passed"):
        return {**r, "status": "no_passing_tests", "baseline": first}
    for item in first["failing"]:
        skip["files" if "::" not in item else "ids"].append(item)
    base = run_tests(skip)
    r["baseline"] = {**base, "preexisting_failures": len(first["failing"])}
    if base["code"]:
        return {**r, "status": "unstable_baseline"}

    sh(f"uv pip install -q -p {PY} -U '{c['upgrade']}'")
    r["new"] = version(c["package"])
    after = run_tests(skip)
    r["after"] = after
    return {**r, "status": "broken" if after["code"] else "not_broken"}


def fix(c: dict, budget: str, model: str) -> dict:
    r = check(c)
    if r["status"] != "broken":
        return r
    # Hide setup artifacts (egg-info, caches) so driftfix sees a clean tree.
    untracked = sh("git ls-files --others --exclude-standard --directory", REPO)[1]
    with open(REPO / ".git" / "info" / "exclude", "a") as f:
        f.write(untracked)
    report = WORK / "report.md"
    code, out = sh(f"driftfix fix --package {c['package']} --from {r['old']} --to {r['new']} "
                   f"--test \"{TEST}\" --model {model} --budget {budget} --timeout 900 --summary {report}",
                   REPO, timeout=3600, secrets=True)
    cost = re.search(r"cost \$([\d.]+)", report.read_text() if report.exists() else out)
    sh("git add -A --intent-to-add .", REPO)  # so new files show up in the diff
    diff = sh("git diff", REPO)[1]
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"{c['id']}.diff").write_text(diff)
    (RESULTS / f"{c['id']}.md").write_text(report.read_text() if report.exists() else out[-5000:])
    return {**r, "driftfix": {"exit": code, "fixed": code == 0, "cost": float(cost[1]) if cost else None,
                              "model": model, "diffstat": sh("git diff --shortstat", REPO)[1].strip()}}


def report() -> str:
    rows = [json.loads(p.read_text()) for p in sorted(RESULTS.glob("*.json"))]
    statuses = {}
    for r in rows:
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    out = [f"**{len(rows)} projects.** " + ", ".join(f"{k}: {v}" for k, v in sorted(statuses.items())), "",
           "| Project | Package | Upgrade | Status | Tests (base → after) | driftfix |", "|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["status"] != "broken", -r["stars"])):
        b, a = r.get("baseline", {}).get("counts", {}), r.get("after", {}).get("counts", {})
        tests = f"{b.get('passed', '')} passed → {a.get('failed', 0) + a.get('error', 0) + a.get('errors', 0)} failing" \
            if a else ""
        d = r.get("driftfix")
        df = "" if not d else f"{'✅' if d['fixed'] else '❌'} ${d['cost'] or 0:.2f} {d['diffstat']}"
        out.append(f"| [{r['repo']}](https://github.com/{r['repo']}) | {r['package']} | "
                   f"{r.get('old', '')} → {r.get('new', '')} | {r['status']} | {tests} | {df} |")
    return "\n".join(out)


def main() -> None:
    cmd, *rest = sys.argv[1:]
    if cmd == "report":
        print(report())
        return
    c = next(c for c in json.loads((ROOT / "candidates.json").read_text()) if c["id"] == rest[0])
    r = check(c) if cmd == "check" else fix(c, os.environ.get("BUDGET", "2"), os.environ.get("MODEL", "claude-opus-5"))
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"{c['id']}.json").write_text(json.dumps(r, indent=1))
    print(r["status"], r.get("old"), "->", r.get("new"), r.get("driftfix", ""))


if __name__ == "__main__":
    main()
