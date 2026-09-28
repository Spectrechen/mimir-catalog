# mimir-catalog

The vendor catalog for [Mimir](https://github.com/spectrechen/mimir), a macOS daemon that merges MDM
policy fragments into the native managed configuration of AI agent harnesses.

`catalog.json` describes, per harness:

- **outputs**: the admin-level files Mimir writes (path, format, mode), with **merge rules** per key path
  (`union`, `replace`, `anyTrue`, `anyFalse`, `min`, `max`, deny lists with `denies` / `matchField`);
- **conflictingPreferenceDomains**: vendor MDM domains that would override Mimir's file;
- **detect**: read-only discovery hints (app bundle IDs, executables, process names, user config paths);
- **status**: `supported`, `experimental` or `planned` (inventoried, never applied);
- **notes**, **documentation** and **lastReviewed**.

It is data only. Mimir additionally limits every output path to an allowlist compiled into its binary,
so a catalog can never make the daemon write anywhere else.

## Trust

Releases carry `catalog.json` and `catalog.json.sig`, a detached Ed25519 signature. Mimir accepts a
catalog only with a valid signature from a key compiled into Mimir, and never one older than the
catalog it already has (unless an admin pins a version).

Public key (base64, raw Ed25519): `pgqDLMFazqC34VUJQU144gjpHfuM6/b6D8qXjVkTEoM=`

The private key is kept offline and never used in CI.

## Harnesses

| id | Harness | Status |
|---|---|---|
| `claude-code` | Claude Code | supported |
| `claude-desktop` | Claude Desktop | experimental |
| `opencode` | opencode | supported |
| `codex` | OpenAI Codex CLI | supported |
| `gemini-cli` | Gemini CLI | planned |
| `github-copilot-cli` | GitHub Copilot CLI | planned |
| `cursor` | Cursor | planned |
| `vscode-copilot` | VS Code (Copilot Chat) | planned |
| `windsurf` | Windsurf / Devin Desktop | planned |
| `goose` | goose | planned |
| `cline` | Cline | planned |
| `claw-code` | claw-code | planned |
| `kiro-cli` | Kiro CLI | planned |
| `droid-cli` | Droid CLI | planned |
| `amp-cli` | Amp CLI | planned |
| `warp` | Warp (Agent Mode) | planned |
| `muse-code` | Muse Code | planned |
| `crush` | Crush | planned |

## Updating

Changes come in as pull requests (a weekly research agent opens them; see [REVIEW.md](REVIEW.md)).
After merging, the maintainer signs and publishes locally:

```bash
scripts/release.sh            # bumps catalogVersion, signs, tags, creates the GitHub release
```
