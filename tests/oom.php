<?php
// Bounded CLI subprocess only. Never request through a production web worker.
register_shutdown_function(function () { echo "SHUTDOWN_CALLBACK_RAN\n"; });
$items = array();
while (true) {
    $items[] = str_repeat('x', 1024 * 1024);
}
