# Validation — PHP 7.2.34

This repository accepts only PHP 7.2.34 source. Release preparation checks
zero-fuzz patch application, non-mutating check mode, explicit application,
repeated-application rejection and rejection of the other PHP release. The
patch bytes remain identical to the public Sury files recorded in provenance.json.

The version-specific [Actions runs](https://github.com/Coolestcool/legacy-security-backports-for-php-7.2/actions)
are the authority for the current build/runtime status. The workflow builds
minimal CLI, CGI and FPM on Ubuntu 22.04, then runs isolated CLI/CGI fixtures for
JSON/hash/date/filter/string behavior, bounded OOM termination without user
shutdown callbacks, GET/POST, persistent sessions, multipart upload digests and
absence of session upload-progress state. It starts no HTTP listener.

FPM is built, not started. Apache, real FPM pools, full application flows,
production extensions, ZTS, Windows and other distributions are not certified.
A successful build is not proof of complete mitigation of all vulnerabilities.

The earlier combined distribution passed both release matrices in
[run 40149083499](https://github.com/Coolestcool/legacy-security-backports-for-php-5.6/actions/runs/40149083499).
That historical result is separate from each version-specific repository's runs.
No private deployment logs, addresses, credentials, backups or binaries are
included in this distribution.
