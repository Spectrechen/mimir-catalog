#!/usr/bin/env python3
"""Structural checks for catalog.json (the authoritative check is `mimirctl catalog verify`)."""
import json, re, sys

ALLOWED_PREFIXES = (
    "/Library/Application Support/ClaudeCode/",
    "/Library/Application Support/opencode/",
    "/Library/Application Support/GeminiCli/",
    "/etc/codex/",
    "/Library/Managed Preferences/com.anthropic.claudefordesktop.plist",
)
STRATEGIES = {"union", "replace", "anyTrue", "anyFalse", "min", "max"}
STATUSES = {"supported", "experimental", "planned"}
FORMATS = {"json", "toml", "plist"}

def fail(msg):
    print("error:", msg); sys.exit(1)

cat = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "catalog.json"))
if cat.get("schemaVersion") != 1: fail("schemaVersion must be 1")
if not re.fullmatch(r"\d{4}\.\d{2}\.\d{2}\.\d+", cat.get("catalogVersion", "")): fail("catalogVersion must be YYYY.MM.DD.N")
ids = set()
for h in cat["harnesses"]:
    hid = h.get("id", "?")
    for k in ("id", "displayName", "vendor", "status", "outputs"):
        if k not in h: fail(f"{hid}: missing {k}")
    if hid in ids: fail(f"duplicate id {hid}")
    ids.add(hid)
    if h["status"] not in STATUSES: fail(f"{hid}: bad status")
    if h["status"] != "planned" and not h["outputs"]: fail(f"{hid}: supported harness without outputs")
    if h["status"] != "planned" and not h.get("documentation"): fail(f"{hid}: documentation links required")
    oids = set()
    for o in h["outputs"]:
        if o["id"] in oids: fail(f"{hid}: duplicate output {o['id']}")
        oids.add(o["id"])
        if o["format"] not in FORMATS: fail(f"{hid}/{o['id']}: bad format")
        p = o["path"]
        if ".." in p.split("/") or not any(p == a or (a.endswith("/") and p.startswith(a)) for a in ALLOWED_PREFIXES):
            fail(f"{hid}/{o['id']}: path {p} is not in Mimir's built-in allowlist")
        for r in o.get("mergeRules", []):
            if "strategy" in r and r["strategy"] not in STRATEGIES: fail(f"{hid}/{o['id']}: bad strategy {r['strategy']}")
print(f"ok: {len(ids)} harnesses, version {cat['catalogVersion']}")
