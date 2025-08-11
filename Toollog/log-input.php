<?php
$data = file_get_contents('php://input');
$log = json_decode($data, true);

if (!$log || !isset($log['inputs'])) {
    http_response_code(400);
    exit;
}

$logDir = __DIR__ . '/logs/';
if (!file_exists($logDir)) {
    mkdir($logDir, 0777, true);
}

// Separate log file per user
$username = $log['user_id'] ?? 'guest';
$filePath = $logDir . $username . '_inputs.json';

// Load existing logs
$existingLogs = [];
if (file_exists($filePath)) {
    $existingLogs = json_decode(file_get_contents($filePath), true);
    if (!is_array($existingLogs)) $existingLogs = [];
}

$existingLogs[] = $log;
file_put_contents($filePath, json_encode($existingLogs, JSON_PRETTY_PRINT));

http_response_code(200);
?>