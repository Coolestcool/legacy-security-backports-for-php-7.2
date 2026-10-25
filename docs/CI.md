# Version-specific CI — PHP 7.2.34

The active workflow is `.github/workflows/validate.yml`; it is installed/updated
through the GitHub web interface because the current publishing CLI token lacks
the workflow scope. No token permissions are expanded for publication.

The template in [ci/validate.yml](ci/validate.yml) targets **only PHP 7.2.34**.
It checks pinned source and patch hashes, prepares source, builds minimal
CLI/CGI/FPM and exercises local CLI/CGI fixtures on Ubuntu 22.04. It needs no
secrets and has read-only repository permissions. FPM and Apache integration
are separate checks. Keep the active workflow and template consistent.

Consult [the actual runs](https://github.com/Coolestcool/legacy-security-backports-for-php-7.2/actions) before
claiming validation. Downloading patches or submitting PRs requires no workflow
permission changes by contributors.
