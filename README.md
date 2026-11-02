# tribe-sdk

Planned public client SDK for AlloyScape seat chat, Studio room protocol, and
speech helpers.

## Status

This repository is a scaffold. It does not yet contain an SDK implementation,
tests, or a release artifact. npm and Python publication are deliberately
blocked until those pieces exist and the release gate is changed in review.

## Publication gate

- `package.json` must remain `private: true` while the repository is a scaffold.
- `tool.szl.publication-authorized` must remain `false`, and the Python project
  must retain the `Private :: Do Not Upload` classifier.
- The automated check requires non-empty implementation and test files before
  publication can be authorized. Package metadata, licensing, build settings,
  and a release workflow still require an explicit release review; this guard
  does not approve them.
- No credentials belong in this repository.

Run the contract check with:

```bash
python3.11 tools/verify_scaffold.py
```
