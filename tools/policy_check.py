"""Deterministic static validator for the aiwk policy corpus.

Checks the repository's Markdown policy modules (*.rules.md, AGENTS*.md),
prompt corpus (*.prompt, manifest.yaml), and executable command policy
comments for the defect classes enumerated in the v3 adversarial-review
task:

  - frontmatter presence, parseability, required fields, format boundary
  - file hygiene: UTF-8 strict, mixed line endings, final newline,
    trailing whitespace, tab characters
  - rule-ID format, uniqueness, namespace consistency, sequence gaps
  - cross-reference resolution for same-directory policy refs,
    .codex/rules policy paths, and dead module names such as `general`
  - manifest coverage: every *.prompt indexed, every manifest path present
  - duplicate normalized normative clauses within and across files
    (IDENTICAL class only; semantic paraphrase dedup is out of scope)
  - shallow MUST vs MUST NOT pairs on shared normalized object text
    (heuristic candidates for human review, not proofs)
  - frontmatter `references` resolution
  - <TBD> marker inventory
  - unbounded-iteration heuristic (retry/loop wording without a bound)

Usage:
  python tools/policy_check.py [--root DIR] [--json OUT]
                               [--exclude REL]... [--quiet]

Exit status is the number of ERROR-severity findings, capped at 125.
This is bounded static analysis over policy text; it does not prove
semantic satisfiability of the rule set.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NORM_VERBS = ("MUST NOT", "MUST", "SHOULD NOT", "SHOULD", "MAY")
RULE_ID_DEF_RE = re.compile(r"^\|\s*([A-Z]{3})-(\d{3})\s*\|")
RULE_ID_RE = re.compile(r"\b([A-Z]{3})-(\d{3})\b")
BACKTICK_REF_RE = re.compile(r"`([^`\n]+?\.(?:rules\.md|md|rules))`")
TBD_RE = re.compile(r"<TBD[^>]*>")
ITER_RE = re.compile(r"\b(retry|retries|loop|until|repeat|repeatedly)\b", re.I)
BOUND_RE = re.compile(
    r"\b(three|3|bounded|budget|termination|terminat\w+|exhaust\w+|escalat\w+|"
    r"stop|limit|maximum|once)\b",
    re.I,
)
HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$")

MD_REQUIRED = {"title", "generated_at", "references"}
PROMPT_REQUIRED = {
    "id",
    "title",
    "category",
    "stage",
    "purpose",
    "inputs",
    "outputs",
    "authority_level",
}

NS_BY_FILE = {
    "coding.rules.md": "COD",
    "commits.rules.md": "COM",
    "configuration.rules.md": "CFG",
    "context.rules.md": "CTX",
    "environments.rules.md": "ENV",
    "metadata.rules.md": "MET",
    "naming.rules.md": "NAM",
    "remotes.rules.md": "REM",
    "security.rules.md": "SEC",
    "skills.rules.md": "SKL",
    "testing.rules.md": "TST",
}

SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", "eval"}
SKIP_REF_CHARS = ("*", "<", ">", "://", "@", "${", "%")
REPO_PATH_PREFIXES = ("rules/", "prompts/", "tools/", "eval/", ".devin/")


def norm_sentence(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def has_normative(s: str) -> bool:
    return any(v in s for v in NORM_VERBS)


def split_frontmatter(text: str):
    """Return (fields, body, errors) for a leading --- YAML block."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None, text, ["no leading frontmatter delimiter"]
    lines = text.split("\n")
    end = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r") == "---":
            end = i
            break
    if end is None:
        return None, text, ["unterminated frontmatter block"]
    fields = {}
    cur_key = None
    for raw in lines[1:end]:
        line = raw.rstrip("\r")
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w]*)\s*:\s*(.*)$", line)
        if m:
            cur_key = m.group(1)
            val = m.group(2).strip()
            if val == "":
                fields[cur_key] = []
            elif val.startswith("[") and val.endswith("]"):
                fields[cur_key] = [
                    v.strip() for v in val[1:-1].split(",") if v.strip()
                ]
            else:
                fields[cur_key] = val
        elif re.match(r"^\s*-\s+", line) and cur_key:
            if not isinstance(fields.get(cur_key), list):
                fields[cur_key] = []
            fields[cur_key].append(re.sub(r"^\s*-\s+", "", line).strip())
    body = "\n".join(lines[end + 1 :])
    errors = []
    after = lines[end + 1 :] if end + 1 < len(lines) else []
    if after and after[0].strip() != "":
        errors.append("closing --- not followed by blank line")
    elif len(after) > 1 and after[0].strip() == "" and after[1].strip() == "":
        errors.append("more than one blank line after frontmatter")
    return fields, body, errors


def iter_files(root: Path, excludes: set):
    for p in sorted(root.rglob("*")):
        if p.is_dir() or any(part in SKIP_DIRS for part in p.parts):
            continue
        rel = p.relative_to(root).as_posix()
        if any(rel == e or rel.startswith(e.rstrip("/") + "/") for e in excludes):
            continue
        yield p


def check_file(path: Path, root: Path, findings: list):
    rel = path.relative_to(root).as_posix()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        findings.append(("ERROR", rel, 0, "encoding", f"not valid UTF-8: {e}"))
        return
    if raw.startswith(b"\xef\xbb\xbf"):
        findings.append(("WARN", rel, 0, "encoding", "UTF-8 BOM present"))
    if b"\r\n" in raw and re.search(rb"(?<!\r)\n", raw):
        findings.append(("ERROR", rel, 0, "newlines", "mixed LF/CRLF"))
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        findings.append(("ERROR", rel, 0, "newlines", "not exactly one final newline"))

    is_policy_text = path.suffix.lower() in {".md", ".prompt", ".rules"}
    lines = text.split("\n")
    in_code = False
    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
        if line != line.rstrip(" \t"):
            sev = "WARN" if line.endswith("  ") and is_policy_text else "ERROR"
            findings.append((sev, rel, n, "whitespace", "trailing whitespace"))
        if (
            is_policy_text
            and not in_code
            and ITER_RE.search(line)
            and not BOUND_RE.search(line)
            and (has_normative(line) or "retry" in line.lower())
        ):
            findings.append(
                ("WARN", rel, n, "bounded-loop",
                 "iteration wording without an explicit bound on this line")
            )

    if path.suffix.lower() in {".md", ".prompt"}:
        fields, _body, errs = split_frontmatter(text)
        if fields is None:
            findings.append(("ERROR", rel, 0, "frontmatter", "; ".join(errs)))
            return
        for e in errs:
            findings.append(("ERROR", rel, 0, "frontmatter", e))
        required = PROMPT_REQUIRED if path.suffix == ".prompt" else MD_REQUIRED
        for k in sorted(required - set(fields)):
            findings.append(("ERROR", rel, 0, "frontmatter", f"missing field {k}"))
        refs = fields.get("references")
        if isinstance(refs, list):
            for r in refs:
                if any(c in r for c in SKIP_REF_CHARS):
                    continue
                rp = (path.parent / r[2:]) if r.startswith("./") else (root / r)
                if not rp.exists() and not (path.parent / r).exists():
                    findings.append(
                        ("WARN", rel, 0, "references",
                         f"reference does not resolve: {r}"))


ECOSYSTEM_FILENAMES = {
    "AGENT.md",
    "AGENTS.override.md",
    "CLAUDE.md",
    "CLAUDE.local.md",
    ".windsurfrules",
}


def resolve_ref(path: Path, root: Path, ref: str):
    """Classify a backticked reference. Returns (severity_key, resolved?)."""
    if any(c in ref for c in SKIP_REF_CHARS):
        return None
    if ref in ECOSYSTEM_FILENAMES:
        return None
    if ref.endswith(".rules.md") or ref in {"AGENTS.md", "AGENTS.local.md"}:
        return ("policy-ref", (path.parent / ref).exists())
    if ref.startswith(".codex/"):
        return ("policy-ref", (root / ".codex/rules").is_dir())
    if ref.startswith(REPO_PATH_PREFIXES):
        return ("policy-ref", (root / ref).exists())
    if ref.startswith(("v1/", "v2/")):
        return ("lineage", False)
    return None


def check_rules_module(path: Path, root: Path, findings: list, sentences: list):
    rel = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    ns = NS_BY_FILE.get(path.name)
    ids = []
    seen = {}
    for m in re.finditer(r"^\|\s*([A-Z]{3})-(\d{3})\s*\|", text, re.M):
        prefix, num = m.group(1), m.group(2)
        rid = f"{prefix}-{num}"
        ids.append((prefix, num))
        if prefix != ns:
            findings.append(("ERROR", rel, 0, "rule-id",
                             f"{rid} does not match namespace {ns}"))
        if rid in seen:
            findings.append(("ERROR", rel, 0, "rule-id", f"duplicate {rid}"))
        seen[rid] = True
    if ns in {"CFG", "CTX", "ENV"} and not ids:
        findings.append(("WARN", rel, 0, "rule-id",
                         f"module has no {ns}-NNN rule identifiers"))
    if ids:
        nums = sorted({int(n) for p, n in ids if p == ns})
        if nums and nums != list(range(nums[0], nums[-1] + 1)):
            missing = sorted(set(range(nums[0], nums[-1] + 1)) - set(nums))
            findings.append(("WARN", rel, 0, "rule-id",
                             f"sequence gap: missing {missing}"))

    in_code = False
    section = ""
    for n, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        hm = HEADING_RE.match(line)
        if hm:
            section = hm.group(1).strip().lower()
        if in_code:
            continue
        historical = "lineage" in section or "migration" in section
        for m in BACKTICK_REF_RE.finditer(line):
            ref = m.group(1)
            outcome = resolve_ref(path, root, ref)
            if outcome is None:
                continue
            kind, ok = outcome
            if kind == "lineage":
                findings.append(("INFO", rel, n, "cross-ref",
                                 f"historical lineage reference `{ref}`"))
            elif not ok:
                sev = "INFO" if historical else "ERROR"
                findings.append((sev, rel, n, "cross-ref",
                                 f"unresolvable reference `{ref}`"))
        for b in re.findall(r"`(general)`", line):
            sev = "INFO" if historical else "ERROR"
            findings.append((sev, rel, n, "cross-ref",
                             f"dead module reference `{b}`"))
        for t in TBD_RE.findall(line):
            findings.append(("INFO", rel, n, "tbd", t))
        for sent in re.split(r"(?<=[.!?])\s+", line):
            if has_normative(sent):
                sentences.append((norm_sentence(sent), rel, n, sent.strip()))


def check_prompt(path: Path, root: Path, findings: list):
    rel = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    for n, line in enumerate(text.split("\n"), 1):
        for b in re.findall(r"`(general)`", line):
            findings.append(("ERROR", rel, n, "cross-ref",
                             f"dead module reference `{b}`"))
        if "rules/version-3" in line:
            findings.append(("ERROR", rel, n, "cross-ref",
                             "stale path `rules/version-3` (actual: rules/version_3)"))


def check_codex_rules(path: Path, root: Path, findings: list):
    rel = path.relative_to(root).as_posix()
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if "rules/version-3" in line:
            findings.append(("ERROR", rel, n, "cross-ref",
                             "stale path `rules/version-3` (actual: rules/version_3)"))


def check_manifest(root: Path, findings: list):
    manifest = root / "prompts/manifest.yaml"
    if not manifest.exists():
        findings.append(("WARN", "prompts/manifest.yaml", 0, "manifest",
                         "manifest not found"))
        return
    text = manifest.read_text(encoding="utf-8")
    entries = re.findall(r"-\s*\{id:\s*([^,}]+),\s*path:\s*([^,}]+)", text)
    indexed_paths = set()
    for pid, ppath in entries:
        ppath = ppath.strip()
        indexed_paths.add(ppath)
        target = root / "prompts" / ppath
        if not target.exists():
            findings.append(("ERROR", "prompts/manifest.yaml", 0, "manifest",
                             f"indexed path missing: {ppath} (id {pid.strip()})"))
    for p in sorted((root / "prompts").rglob("*.prompt")):
        rel = p.relative_to(root / "prompts").as_posix()
        if rel not in indexed_paths:
            findings.append(("ERROR", p.relative_to(root).as_posix(), 0,
                             "manifest", f"prompt not indexed in manifest: {rel}"))


def duplicate_analysis(sentences: list, findings: list):
    by_norm = {}
    for norm, rel, n, raw in sentences:
        if len(norm) < 40:
            continue
        by_norm.setdefault(norm, []).append((rel, n, raw))
    for norm, occs in sorted(by_norm.items()):
        locs = {(r, n) for r, n, _ in occs}
        files = {r for r, _, _ in occs}
        if len(locs) > 1:
            tag = "IDENTICAL-cross-file" if len(files) > 1 else "IDENTICAL-intra-file"
            where = "; ".join(f"{r}:{n}" for r, n, _ in occs[:6])
            findings.append(("WARN", occs[0][0], occs[0][1], "dup-clause",
                             f"{tag}: {where} :: {occs[0][2][:110]}"))

    must, mustnot = {}, {}
    for norm, rel, n, raw in sentences:
        obj = norm
        for v in ("must not", "must", "should not", "should", "may"):
            obj = obj.replace(v, " ")
        obj = re.sub(r"\s+", " ", obj).strip()
        if len(obj) < 25:
            continue
        if "MUST NOT" in raw:
            mustnot.setdefault(obj, []).append((rel, n, raw))
        elif re.search(r"\bMUST\b", raw):
            must.setdefault(obj, []).append((rel, n, raw))
    for obj, pos in must.items():
        if obj in mustnot:
            for r, n, raw in pos + mustnot[obj]:
                findings.append(("WARN", r, n, "contradiction-candidate",
                                 "shared normalized object with MUST/MUST NOT pair: "
                                 + obj[:80]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    excludes = set(args.exclude)

    findings: list[tuple] = []
    sentences: list[tuple] = []

    for p in iter_files(root, excludes):
        name = p.name
        if ".codex" in p.parts and p.suffix == ".rules":
            check_file(p, root, findings)
            check_codex_rules(p, root, findings)
        elif p.suffix == ".prompt":
            check_file(p, root, findings)
            check_prompt(p, root, findings)
        elif p.suffix == ".md":
            check_file(p, root, findings)
            if p.parent.name in {"version_3", "version-3"} and (
                name.endswith(".rules.md") or name.startswith("AGENTS")
            ):
                check_rules_module(p, root, findings, sentences)
        else:
            check_file(p, root, findings)

    check_manifest(root, findings)
    duplicate_analysis(sentences, findings)

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda f: (order.get(f[0], 3), f[1], f[2]))
    errors = sum(1 for f in findings if f[0] == "ERROR")
    warns = sum(1 for f in findings if f[0] == "WARN")
    infos = sum(1 for f in findings if f[0] == "INFO")

    report = {
        "root": str(root),
        "excluded": sorted(excludes),
        "errors": errors,
        "warnings": warns,
        "info": infos,
        "findings": [
            {"severity": s, "file": f, "line": n, "check": c, "detail": d}
            for s, f, n, c, d in findings
        ],
    }
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
    if not args.quiet:
        for s, f, n, c, d in findings:
            if s == "INFO":
                continue
            print(f"{s:5} {f}:{n} [{c}] {d}")
        print(f"\n{errors} error(s), {warns} warning(s), {infos} info marker(s)")
    return min(errors, 125)


if __name__ == "__main__":
    sys.exit(main())
