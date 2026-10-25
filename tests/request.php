<?php
// Invoked directly by the local CGI harness; do not deploy this fixture.
if (getenv('LEGACY_PATCH_LAB') !== '1') {
    http_response_code(403);
    exit;
}
session_start();
$_SESSION['fixture_count'] = isset($_SESSION['fixture_count']) ? $_SESSION['fixture_count'] + 1 : 1;
$files = array();
foreach ($_FILES as $key => $file) {
    $files[$key] = array(
        'error' => $file['error'],
        'uploaded' => is_uploaded_file($file['tmp_name']),
        'sha256' => $file['error'] === UPLOAD_ERR_OK ? hash_file('sha256', $file['tmp_name']) : null
    );
}
$progress = false;
foreach (array_keys($_SESSION) as $key) {
    if (strpos($key, 'upload_progress_') === 0) { $progress = true; }
}
header('Content-Type: application/json');
echo json_encode(array('get' => $_GET, 'post' => $_POST, 'files' => $files,
    'session_count' => $_SESSION['fixture_count'], 'upload_progress_record' => $progress));
