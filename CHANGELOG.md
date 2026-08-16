# Changelog

## [0.2.0](https://github.com/JoeMountWSWS/wsws-md/compare/v0.1.2...v0.2.0) (2026-08-16)


### ⚠ BREAKING CHANGES

* **deps:** drop Python 3.9 support to patch urllib3 CVE-2026-44432 ([#6](https://github.com/JoeMountWSWS/wsws-md/issues/6))

### Features

* **cli:** add --no-frontmatter flag to omit YAML header ([#3](https://github.com/JoeMountWSWS/wsws-md/issues/3)) ([471e6b1](https://github.com/JoeMountWSWS/wsws-md/commit/471e6b1f860e248f3c111181b8d15db9905287a3))
* package wsws-md as a Claude Skill with a release-zip workflow ([#2](https://github.com/JoeMountWSWS/wsws-md/issues/2)) ([9d7b874](https://github.com/JoeMountWSWS/wsws-md/commit/9d7b8741dd0a466fd37673797af21b34661d9555))


### Bug Fixes

* **cli:** handle BrokenPipeError when stdout is closed early ([#5](https://github.com/JoeMountWSWS/wsws-md/issues/5)) ([04d3ff0](https://github.com/JoeMountWSWS/wsws-md/commit/04d3ff0970fb2b79da12db1535b0af86c1fc2b06))
* **deps:** drop Python 3.9 support to patch urllib3 CVE-2026-44432 ([#6](https://github.com/JoeMountWSWS/wsws-md/issues/6)) ([35fce01](https://github.com/JoeMountWSWS/wsws-md/commit/35fce0183661000db33120af2ddd9258f0fc6c10))


### Documentation

* explain why WSWS-specific extraction beats generic converters ([9c3910c](https://github.com/JoeMountWSWS/wsws-md/commit/9c3910c5ccd2c26900032eb96f1e639d3d7003a9))

## [0.1.1](https://github.com/JoeMountWSWS/wsws-md/compare/v0.1.0...v0.1.1) (2026-07-14)


### Bug Fixes

* **ci:** pin setup-uv to v7 ([b61bada](https://github.com/JoeMountWSWS/wsws-md/commit/b61badacccd7482bca0f11bfd6544bb5ac98aae5))
