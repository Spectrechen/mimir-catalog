# Reviewing catalog changes

Each change to `catalog.json` changes what a root daemon writes on managed Macs. Before merging:

1. **Sources.** Every changed path, key or rule must be backed by a vendor documentation link in the
   harness's `documentation` list (or the PR description). Blog posts alone are not enough.
2. **Paths.** A new or changed `outputs[].path` only works if Mimir's `PathPolicy.builtInPrefixes`
   already allows it. If not, the PR needs a matching Mimir release first. Never widen a path to a
   directory shared with other software.
3. **Merge rules: the more restrictive rule always wins.**
   - Grant lists (servers/permissions a fragment *provides*, e.g. `allowedMcpServers`, `permissions.allow`,
     `mcpServers`) → `union`, so extra access can be added by a separate fragment.
   - Restriction allowlists (the *only* values a user may use, e.g. `availableModels`,
     `allowed_sandbox_modes`, `enabled_providers`) → `intersect`.
   - Deny lists → `union` + `denies` (always beat grants).
   - Enum settings with a clear strictness order (e.g. `sandbox_mode`, `share`) → `strictest` with
     `order`, most restrictive first.
   - Kill switches → `anyFalse`; locks → `anyTrue`; limits → `min` (retention, deadlines) or `max`
     (minimum versions).
   A wrong rule can loosen policy; when unsure, pick the more restrictive strategy.
4. **Status.** New harnesses start as `planned` (discovery only). Promote to `supported` only after
   testing on a managed Mac.
5. **Detect.** Discovery hints are read-only; paths may use `~/` and `*`.
6. `lastReviewed` is updated for every harness the PR touches.
7. CI (`validate`) must pass.

Then run `scripts/release.sh` locally. It is the only step that uses the signing key.
