# Releasing

Releases are fully automated: merging PRs to `main` produces a release PR,
and merging that release PR ships the package to PyPI and attaches the
Claude Skill zip to the GitHub release. Nobody tags or uploads by hand.

## The pipeline

| Stage | Workflow | Trigger |
| --- | --- | --- |
| Open/update the release PR | `.github/workflows/release-please.yml` | push to `main` |
| Create the tag + GitHub release | same workflow | merge of the release PR |
| Publish to PyPI | `.github/workflows/publish.yml` | `release: published` |
| Attach the skill zip | `.github/workflows/skill-release.yml` | `release: published` |

## Normal release

1. **Merge feature PRs into `main`.** Squash merge only — GitHub uses the PR
   title as the commit message, and release-please parses that title to
   decide the next version. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
   Conventional Commits rules that `pr-title.yml` enforces.

2. **Wait for the release PR.** On each push to `main`, release-please
   opens or updates a PR titled `chore(main): release X.Y.Z`. It changes
   exactly three files:

   - `pyproject.toml` — the `version` field
   - `CHANGELOG.md` — a new section built from the merged commits
   - `.release-please-manifest.json` — the recorded current version

3. **Review the release PR.** Check that the proposed version matches the
   changes and that the changelog entries read sensibly. If a commit was
   mistyped (a `feat` that should have been a `fix`, or a missing
   `BREAKING CHANGE:` footer), fix it before merging — see
   [Correcting a version bump](#correcting-a-version-bump).

4. **Merge the release PR.** release-please then pushes tag `vX.Y.Z` and
   publishes a GitHub release, which fans out to `publish.yml` (builds the
   sdist + wheel and uploads to PyPI) and `skill-release.yml` (zips
   `skills/wsws-md` and attaches `wsws-md-skill-X.Y.Z.zip` to the release).

5. **Sync `uv.lock`.** release-please does not touch the lockfile, so its
   pinned version of `wsws-md` lags by one release. After the release
   lands, run on `main`:

   ```sh
   uv lock
   git commit -am "chore: sync uv.lock to version X.Y.Z"
   ```

   Open this as a normal PR (branch protection applies to `main` like any
   other change).

6. **Verify.** Confirm the new version appears on
   [PyPI](https://pypi.org/p/wsws-md), the skill zip is attached to the
   [release](https://github.com/JoeMountWSWS/wsws-md/releases), and a
   clean install works:

   ```sh
   uv venv /tmp/release-check
   uv pip install --python /tmp/release-check/bin/python wsws-md==X.Y.Z
   /tmp/release-check/bin/wswsmd --help
   ```

## How the version is chosen

The project is pre-1.0, and `release-please-config.json` sets
`bump-minor-pre-major: true` with `bump-patch-for-minor-pre-major: false`.
While the major version is `0`:

| Commit type | Bump | Example |
| --- | --- | --- |
| `fix:` | patch | 0.3.0 → 0.3.1 |
| `feat:` | minor | 0.3.0 → 0.4.0 |
| `feat!:` / `BREAKING CHANGE:` | minor (not major) | 0.3.0 → 0.4.0 |
| `docs:`, `chore:`, `ci:`, `test:`, … | none | no release PR opened |

Only `feat`, `fix`, and breaking changes trigger a release. A run of
docs-and-chores commits will not produce a release PR at all — that is
expected, not a broken workflow.

Cutting the first stable release means removing `bump-minor-pre-major` from
the config (or landing a breaking change once the version is already 1.x).

## Prerequisites

These are configured once at the repository level; they only need attention
if a release fails to authenticate.

- **GitHub App credentials** — `vars.RELEASE_PLEASE_APP_ID` and
  `secrets.RELEASE_PLEASE_APP_PRIVATE_KEY`. release-please must act as an
  App rather than the default `GITHUB_TOKEN`: releases created with the
  default token do not fire other workflows' `release: published` triggers,
  so `publish.yml` and `skill-release.yml` would silently never run.
- **PyPI Trusted Publishing** — `publish.yml` uses the `pypi` GitHub
  environment with `id-token: write` and no API token. The publisher must
  be registered on PyPI for `JoeMountWSWS/wsws-md` and the `publish.yml`
  workflow.

## Recovery

**A release PR never appeared.** Check that the merged commits include a
`feat` or `fix`; other types do not trigger a release. Then check the
release-please workflow run for an App-token failure.

**PyPI publish failed.** Fix the cause, then re-run `publish.yml` via
**Actions → Publish to PyPI → Run workflow**, passing the tag (e.g.
`v0.3.1`). It checks out that tag and rebuilds from source, so it does not
depend on the failed run's artifacts. PyPI rejects re-uploads of an
already-published version — if a version is partially published, cut a new
patch release instead of trying to overwrite it.

**Skill zip missing from the release.** Re-run `skill-release.yml` the same
way with the tag input. Note that the manual run uploads the zip as a build
artifact but only attaches it to the GitHub release when triggered by a
release event, so attach it by hand if needed:

```sh
gh release upload vX.Y.Z wsws-md-skill-X.Y.Z.zip
```

**Correcting a version bump.** The release PR is regenerated from the
commit history on `main`, so amend the history rather than editing the PR:
close the release PR, correct the offending commit message on `main`, and
push. release-please recomputes the version and reopens the PR on the next
push.

## Known drift

- `src/wswsmd/__init__.py` carries a `__version__` string that
  release-please does not update, so it is stale. It is not used for
  packaging (`pyproject.toml` is the source of truth), but bump it by hand
  if you rely on it, or add it to `extra-files` in
  `release-please-config.json` to automate it.
- `uv.lock` needs the manual sync described in step 5 above.
