# Contributing

## Conventional Commits

Pull request titles **must** follow the [Conventional Commits](https://www.conventionalcommits.org/)
format:

```
<type>[optional scope]: <description>
```

Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
`build`, `ci`, `chore`, `revert`.

Examples:

```
feat: support extracting article tags
fix: handle articles with no byline
docs: add usage example for --output flag
```

For a breaking change, add `!` after the type/scope (e.g. `feat!: drop Python 3.9 support`)
or include a `BREAKING CHANGE:` footer in the PR description.

This repo merges pull requests via **squash merge only**, and GitHub uses the
PR title as the resulting commit message. A CI check
(`.github/workflows/pr-title.yml`) enforces the format on every PR, and
[release-please](https://github.com/googleapis/release-please) reads these
commit messages after merge to determine version bumps and generate the
changelog, so an accurately-typed title is required for a PR to merge.

## Releases

Releases are automated with release-please (`.github/workflows/release-please.yml`).
On every push to `main`, it opens/updates a "release PR" that bumps the
version in `pyproject.toml` and updates `CHANGELOG.md` based on merged
commits since the last release. Merging that PR creates the GitHub release
and tag, which in turn publishes to PyPI and attaches the packaged Claude
Skill to the release.

See [RELEASING.md](RELEASING.md) for the full process, including how the
version bump is chosen, the required repository secrets, and how to recover
from a failed publish.
