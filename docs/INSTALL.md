# Install and roll back — PHP 7.2.34

## Identify the real runtime

Inventory exact package revisions, CLI/CGI/FPM binaries, Apache modules, container
images, loaded extensions, INI paths and build options. `php -v` identifies the
CLI selected by PATH, not the web runtime. Treat configuration output as private.

Use source matching your installed package/image and retain every existing
vendor patch. This tool accepts exactly PHP 7.2.34, not arbitrary 7.2.x.
For pristine PHP 7.2.34, the ZSTR_MAX_LEN prerequisite is included and applied automatically.

## Download, check and apply

```sh
git clone --branch v0.2.0 https://github.com/Coolestcool/legacy-security-backports-for-php-7.2.git
cd legacy-security-backports-for-php-7.2
sha256sum -c SHA256SUMS
python3 tools/prepare-source.py /path/to/php-7.2.34
python3 tools/prepare-source.py /path/to/php-7.2.34 --apply
```

The first helper invocation modifies only temporary copies. `--apply` writes
source files after the entire sequence passes with zero fuzz. Python 3.8+, patch
and a writable temporary directory are required. On macOS use
`shasum -a 256 -c SHA256SUMS`. Rejects, wrong versions, modified patch hashes and
repeated main application fail; do not force or ignore them. Use a disposable
source working tree with an original snapshot.

Source archives and hashes are in sources.json. Standalone release downloads
use SHA256SUMS.assets, whose paths are flat filenames. The complete tar archive
retains patches/, tools/ and its internal SHA256SUMS; extract before using the
helper. Neither checksum manifest is a signature.

## Rebuild matching packages or images

Patching source does not update installed binaries. Use the distribution/image
build process, preserving compiler flags, architecture, thread safety, module
ABI, extensions, config paths and linked libraries. Rebuild every SAPI that is
actually used. An updated CLI alone does not update Apache or FPM.

For a **minimal isolated laboratory build only**:

```sh
./configure --disable-all --enable-cli --enable-cgi --enable-fpm \
  --enable-session --enable-json --enable-hash --enable-filter
make -j2
python3 "$PATCH_REPO/tests/check-runtime.py" sapi/cli/php sapi/cgi/php-cgi
```

Set PATCH_REPO to the absolute clone path before changing into the PHP source
directory. This example omits production extensions and Apache integration;
never install it over a packaged production runtime. Prefer vendor-maintained
packages if they already contain the fix; do not apply it twice.

## Stage, deploy and validate

Back up original packages/binaries, Apache module, extensions, configuration,
wrappers, permissions, service definitions and exact image/Compose IDs. Test
restoration in isolation and retain console access.

In staging, compare runtime version, extensions, INI paths and dependencies;
exercise every active SAPI and the application's representative workflows.
Check GET/POST, login/session persistence, normal multipart uploads and logs.
Upload-progress tracking is intentionally disabled in code; OOM shutdown behavior
changes. Run memory-exhaustion fixtures only in an isolated child process.

Deploy through the reviewed package/image procedure. Pin images, retain the
previous image and configuration, and recreate only affected services. Check
proxy resolution if container addresses change. Restart or retire every old
worker and inspect running executable/module mappings, including deleted old
mappings where available. A successful service-manager status is insufficient.
Recheck real HTTP responses and logs after activation.

The supplied tests use local CLI/CGI processes and temporary session storage;
they start no HTTP listener. CI also builds FPM but does not start it. Apache,
FPM pool and application integration remain separate checks.

## Rollback

Restore saved packages/binaries, module, extensions, configuration and prior
image using your deployment controls. Restart/recreate affected services, retire
stale workers and recheck artifact hashes and real application responses.
Reversing source alone does not roll back installed binaries. Do not repair or
reset databases as part of this PHP rollback. Reverting also restores the prior
security exposure; investigate in staging before retrying deployment.
