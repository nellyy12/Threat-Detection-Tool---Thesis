<?php
// Enable error reporting for debugging
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Get POSTed raw JSON data
$data = file_get_contents('php://input');
$log = json_decode($data, true);

// Validate session_id
if (!$log || !isset($log['session_id'])) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Invalid log data']);
    exit;
}

// Clean .php from pages_visited
if (isset($log['pages_visited']) && is_array($log['pages_visited'])) {
    $log['pages_visited'] = array_unique(array_map(function ($page) {
        return str_replace('.php', '', $page);
    }, $log['pages_visited']));
}

// Clean input_logs to keep only values
if (isset($log['input_logs']) && is_array($log['input_logs'])) {
    $log['input_logs'] = array_values(array_filter(array_map(function ($entry) {
        return isset($entry['value']) ? $entry['value'] : null;
    }, $log['input_logs'])));
}

// Set up logs directory
$logDir = __DIR__ . '/logs/';
if (!file_exists($logDir)) {
    mkdir($logDir, 0777, true);
}

// Determine filename based on user ID
$username = isset($log['user_id']) && $log['user_id'] !== '' ? $log['user_id'] : 'guest';
$filePath = $logDir . $username . '.json';

// Load existing log file if available
$existingLogs = [];
if (file_exists($filePath)) {
    $existingLogs = json_decode(file_get_contents($filePath), true);
    if (!is_array($existingLogs)) {
        $existingLogs = [];
    }
}

// If session already exists, merge input_logs and pages_visited
if (isset($existingLogs[$log['session_id']])) {
    $existing = &$existingLogs[$log['session_id']];

    // Merge input_logs without duplicates
    if (isset($log['input_logs'])) {
        $existing['input_logs'] = array_values(array_unique(array_merge($existing['input_logs'] ?? [], $log['input_logs'])));
    }

    // Merge pages_visited without duplicates
    if (isset($log['pages_visited'])) {
        $existing['pages_visited'] = array_values(array_unique(array_merge($existing['pages_visited'] ?? [], $log['pages_visited'])));
    }

    // Update other fields
    foreach ($log as $key => $value) {
        if (!in_array($key, ['input_logs', 'pages_visited'])) {
            $existing[$key] = $value;
        }
    }
} else {
    // New session log
    $existingLogs[$log['session_id']] = $log;
}

// Save updated logs
file_put_contents($filePath, json_encode($existingLogs, JSON_PRETTY_PRINT));

echo json_encode(['status' => 'success']);