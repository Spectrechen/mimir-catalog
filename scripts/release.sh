#!/bin/zsh
# Bumps catalogVersion to today's date (+ counter), signs catalog.json with the offline key,
# commits, tags and publishes a GitHub release with catalog.json + catalog.json.sig.
#   scripts/release.sh [signing key]   (default ~/.config/mimir-signing/catalog-ed25519.key)
set -euo pipefail
cd "${0:A:h}/.."
KEY="${1:-$HOME/.config/mimir-signing/catalog-ed25519.key}"
CTL="${MIMIRCTL:-$(command -v mimirctl || echo "$HOME/Library/Caches/Mimir-build/spm/debug/mimirctl")}"
[[ -f "$KEY" ]] || { echo "signing key not found: $KEY" >&2; exit 1; }
[[ -z "$(git status --porcelain)" ]] || { echo "working tree not clean" >&2; exit 1; }
git pull --ff-only

today=$(date +%Y.%m.%d)
n=1
while git rev-parse -q --verify "refs/tags/$today.$n" >/dev/null; do n=$((n + 1)); done
version="$today.$n"
/usr/bin/python3 - "$version" <<'PY'
import json, re, sys
path = "catalog.json"
text = open(path).read()
text = re.sub(r'"catalogVersion": "[^"]*"', f'"catalogVersion": "{sys.argv[1]}"', text, count=1)
open(path, "w").write(text)
json.loads(text)
PY
/usr/bin/python3 scripts/validate.py catalog.json
"$CTL" catalog sign catalog.json --key "$KEY"
"$CTL" catalog verify catalog.json
git add catalog.json catalog.json.sig
git commit -m "Release catalog $version"
git tag "$version"
git push origin HEAD --tags
gh release create "$version" catalog.json catalog.json.sig --title "Catalog $version" --notes "Signed vendor catalog $version."
echo "Published $version"
