# Reviewing catalog changes

Each change to `catalog.json` changes what a root daemon writes on managed Macs. Before merging:

1. **Sources.** Every changed path, key or rule must be backed by a vendor documentation link in the
   harness's `documentation` list (or the PR description). Blog posts alone are not enough.
2. **Paths.** A new or changed `outputs[].path` only works if Mimir's `PathPolicy.builtInPrefixes`
   already allows it. If not, the PR needs a matching Mimir release first. Never widen a path to a
   directory shared with other software.
3. **Merge rules.** Allow lists → `union`; restrictions → `denies`; kill switches → `anyFalse`;
   locks → `anyTrue`. A wrong rule can loosen policy.
4. **Status.** New harnesses start as `planned` (discovery only). Promote to `supported` only after
   testing on a managed Mac.
5. **Detect.** Discovery hints are read-only; paths may use `~/` and `*`.
6. `lastReviewed` is updated for every harness the PR touches.
7. CI (`validate`) must pass.

Then run `scripts/release.sh` locally. It is the only step that uses the signing key.
