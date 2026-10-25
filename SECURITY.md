# Security scope and reporting

## Supported scope

This project distributes community tooling for the specific legacy PHP source
backports targeting CVE-2026-109618 and CVE-2026-109619. PHP 7.2 is end
of life. There is no promise of full vulnerability coverage, commercial support,
a response SLA or compatibility with arbitrary extensions or vendor builds.

The maintained-branch complete fixes and these minimal EOL backports are not
identical implementations. The latter deliberately sacrifice graceful OOM
request shutdown and session upload-progress tracking. Follow the current PHP
advisories and prefer vendor-maintained updates where available.

A 23 October 2026 PHP notice describes a related session upload-progress vector
(CVE-2026-115560). The redistributed patches return before the built-in progress
tracking code. That is a source-level reason to expect that specific vector to
be blocked, not an independent exploit validation for every build. The INI
setting may still display `1` because disabling happens in code.

References:
- https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w
- https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp
- https://www.php.net/archive/2026.php

## Reporting

Do not publish a new working exploit, credentials, customer data or internal
configuration in a public issue. For vulnerabilities in PHP itself, follow the
[PHP security reporting process](https://www.php.net/security/).
For vulnerabilities in this project's helper, use GitHub private vulnerability
reporting if enabled on the repository Security tab. If unavailable, open a
sanitized issue requesting a private channel without exploit details.
Public issues are appropriate for sanitized compatibility and build reports.

## Operational precautions

Build and run memory-exhaustion tests only in a disposable, resource-limited
laboratory. The tests intentionally terminate child processes. Do not point
them at production services or run untrusted fixtures in a live PHP pool.
A successful smoke test or a clean log is not proof of complete security.
