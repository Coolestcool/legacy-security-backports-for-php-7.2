<?php
// Run only with isolated test binaries; no production configuration is loaded.
echo json_encode(array(
    'version_id' => PHP_VERSION_ID,
    'json_roundtrip' => json_decode(json_encode(array('x' => array(1, 'two', true))), true),
    'hash' => hash('sha256', 'legacy-source-fixture'),
    'date' => gmdate('Y-m-d', 0),
    'integer' => filter_var('42', FILTER_VALIDATE_INT),
    'string' => substr('abcdef', 1, 3)
), JSON_UNESCAPED_SLASHES), "\n";
