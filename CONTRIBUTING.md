# Contributing

Thanks for helping people maintain safer legacy systems.

1. Start with a small issue or pull request describing the target source release,
   package revision, OS/compiler, SAPI and relevant extension versions.
2. Reproduce in an isolated source tree. Include commands, expected behavior,
   actual behavior and sanitized logs. Do not attach real configurations or data.
3. Keep changes narrow. Preserve upstream credits and distinguish original vendor
   patches from any subsequent changes. Update provenance and SHA256SUMS if a
   patch changes, and document the exact reason.
4. Run the source preparation checks and local CLI/CGI tests; add a regression test
   for a behavioral change. Review this repository's PHP 7.2.34 target when shared tooling changes.
5. Explain limitations honestly. A successful build is not a security proof or
   confirmation of all application flows. Follow SECURITY.md for private reports.

A useful compatibility report includes whether patch application used zero fuzz,
which SAPIs were rebuilt, extension/INI comparison, session/upload results,
worker-replacement verification and whether rollback was exercised.

Project supporting materials are MIT licensed. Patch contributions must respect
the applicable PHP/Zend licenses and original notices; do not remove credits or
claim unrelated upstream work as your own. By submitting a contribution, you
agree that it may be distributed under the applicable existing project terms.
