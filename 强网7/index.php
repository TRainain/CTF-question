<?php
session_start();
require 'user.php';
require 'class.php';

$sessionManager = new SessionManager();
$SessionRandom = new SessionRandom();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $_SESSION['user'] = $username;

    if (!isset($_SESSION['session_key'])) {
        $_SESSION['session_key'] =$SessionRandom -> generateRandomString();
    }
    $_SESSION['password'] = $password;
    $result = $sessionManager->filterSensitiveFunctions();
    header('Location: dashboard.php');
    exit();
} else {
    require 'login.php';
}
