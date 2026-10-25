#!/usr/bin/env python3
"""Local CLI/CGI fixtures for isolated builds. No listener or production URL."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def check(condition, label):
    if not condition:
        raise RuntimeError('FAIL: ' + label)
    print('PASS: ' + label, flush=True)


def run(command, **kwargs):
    return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, **kwargs)


def main(cli, cgi):
    basic = run([cli, '-n', str(HERE / 'compat.php')])
    if basic.returncode != 0:
        print(basic.stdout.decode(errors='replace'), basic.stderr.decode(errors='replace'), flush=True)
    check(basic.returncode == 0, 'CLI compatibility fixture exits successfully')
    data = json.loads(basic.stdout)
    check(data['version_id'] == 70234, 'expected legacy PHP release')
    check(data['json_roundtrip'] == {'x': [1, 'two', True]} and data['hash'] == hashlib.sha256(b'legacy-source-fixture').hexdigest() and data['date'] == '1970-01-01' and data['integer'] == 42 and data['string'] == 'bcd', 'JSON, hash, date, filter and string compatibility')
    oom = run([cli, '-n', '-d', 'memory_limit=8M', str(HERE / 'oom.php')])
    check(oom.returncode == 1 and b'SHUTDOWN_CALLBACK_RAN' not in oom.stdout and b'Fatal error' in oom.stderr, 'bounded OOM terminates without user shutdown callback')
    with tempfile.TemporaryDirectory(prefix='legacy-session-fixture-') as temp:
        def request(body=b'', content_type=None, cookie='PHPSESSID=legacyfixture'):
            env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'LEGACY_PATCH_LAB': '1',
                   'SCRIPT_FILENAME': str(HERE / 'request.php'), 'SCRIPT_NAME': '/request.php',
                   'REQUEST_METHOD': 'POST' if content_type else 'GET', 'QUERY_STRING': 'x=42',
                   'REDIRECT_STATUS': '1', 'GATEWAY_INTERFACE': 'CGI/1.1',
                   'SERVER_PROTOCOL': 'HTTP/1.1', 'SERVER_NAME': 'localhost', 'SERVER_PORT': '80',
                   'HTTP_COOKIE': cookie}
            if content_type:
                env.update(CONTENT_TYPE=content_type, CONTENT_LENGTH=str(len(body)))
            args = [cgi, '-n', '-d', 'cgi.force_redirect=0', '-d', 'session.save_path=' + temp,
                    '-d', 'session.upload_progress.freq=1', '-d', 'session.upload_progress.min_freq=0']
            response = run(args, input=body, env=env)
            check(response.returncode == 0, 'CGI request completes')
            raw = response.stdout.replace(b'\r\n', b'\n')
            headers, output = raw.split(b'\n\n', 1)
            check(b'Status: 500' not in headers, 'CGI response is not HTTP 500')
            return json.loads(output)
        first = request()
        second = request()
        check(first['get'] == {'x': '42'}, 'CGI GET decoding')
        check(first['session_count'] == 1 and second['session_count'] == 2, 'session persistence across CGI requests')
        post = request(b'a=1&arr%5B%5D=two&arr%5B%5D=3', 'application/x-www-form-urlencoded')
        check(post['post'] == {'a': '1', 'arr': ['two', '3']}, 'CGI POST decoding')
        content = b'legacy-upload-fixture\n' * 512
        boundary = 'LegacyPatchFixtureBoundary'
        body = (('--' + boundary + '\r\nContent-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"\r\n\r\nfixture\r\n--' + boundary + '\r\nContent-Disposition: form-data; name="upload"; filename="fixture.txt"\r\nContent-Type: text/plain\r\n\r\n').encode() + content + ('\r\n--' + boundary + '--\r\n').encode())
        upload = request(body, 'multipart/form-data; boundary=' + boundary, 'PHPSESSID=legacyuploadfixture')
        check(upload['files']['upload'] == {'error': 0, 'uploaded': True, 'sha256': hashlib.sha256(content).hexdigest()}, 'normal multipart upload and digest')
        check(upload['upload_progress_record'] is False, 'session upload-progress state absent')
    print('All local CLI/CGI checks passed. FPM/Apache/application integration not tested here.')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: check-runtime.py /isolated/php /isolated/php-cgi')
    main(str(Path(sys.argv[1]).resolve()), str(Path(sys.argv[2]).resolve()))
