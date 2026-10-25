# Sury security backports for PHP 7.2

Community redistribution of the unmodified **Sury backport for PHP 7.2.34**,
targeting **CVE-2026-109618** and **CVE-2026-109619** (PHP2Shell).

Maintained by [Coolestcool](https://github.com/Coolestcool). Original fix and
backport authorship remains upstream. This is not an official Sury/PHP project
or a GitHub fork of the vendor packaging history. See [provenance](PROVENANCE.md).

**This repository is only for PHP 7.2.34.** For PHP 5.6, use the
[separate repository](https://github.com/Coolestcool/legacy-security-backports-for-php-5.6).

## Download and apply to source

[Download v0.2.0](https://github.com/Coolestcool/legacy-security-backports-for-php-7.2/releases/tag/v0.2.0)
contains the patch, source-preparation tool, guides and licenses. For pristine PHP 7.2.34, the ZSTR_MAX_LEN prerequisite is included and applied automatically.

```sh
git clone --branch v0.2.0 https://github.com/Coolestcool/legacy-security-backports-for-php-7.2.git
cd legacy-security-backports-for-php-7.2
sha256sum -c SHA256SUMS

# Check the complete patch sequence in temporary copies; leave source unchanged.
python3 tools/prepare-source.py /path/to/php-7.2.34
# Explicitly apply only to a disposable, backed-up source working tree.
python3 tools/prepare-source.py /path/to/php-7.2.34 --apply
```

On macOS use `shasum -a 256 -c SHA256SUMS`.
Checksums are not signatures or independent proof of their own origin.
The main patch [`php72-php2shell.patch`](patches/php72-php2shell.patch) targets both named CVEs.

**Patching source does not update a running server.** Rebuild matching
packages/images, retain required extensions and vendor patches, verify each
active SAPI and replace old workers. A package revision is more specific than a
PHP release number; do not overwrite a vendor runtime with a minimal lab build.

- [Installation and rollback](docs/INSTALL.md)
- [Guía en español](docs/INSTALL.es.md)
- [Validation and limits](docs/VALIDATION.md)
- [GitHub Actions](https://github.com/Coolestcool/legacy-security-backports-for-php-7.2/actions)
- [Contributing](CONTRIBUTING.md) · [Security reporting](SECURITY.md)

## Scope and behavior

PHP 7.2 is end of life. These are minimal source backports, not a supported
PHP release or comprehensive coverage of all legacy vulnerabilities. OOM
handling terminates the affected process immediately; user shutdown callbacks
will not run on that path. Built-in session upload-progress tracking is disabled
in code, while normal multipart uploads remain supported and need testing.
A displayed `session.upload_progress.enabled=1` does not prove tracking is active.

Issues and pull requests are welcome. Never attach production configurations,
credentials or customer data. New exploitable vulnerabilities should follow the
private reporting guidance in SECURITY.md.

## Credits and license

The main patch credits Arnaud Le Blanc and Ilija Tovilo. Sury packaging, PHP
Group and Zend contributors retain their credits. Any prerequisite retains its
own header. Exact public sources and hashes are in [provenance.json](provenance.json).
Patch files preserve their upstream PHP/Zend licensing; supporting materials
use the MIT terms in [LICENSE](LICENSE). Original notices are in [LICENSES](LICENSES/).
This product includes PHP software, freely available from <http://www.php.net/software/>.

[PHP announcement](https://www.php.net/archive/2026.php#2026-10-21-5) ·
[CVE-2026-109618](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w) ·
[CVE-2026-109619](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp)
