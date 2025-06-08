<?php
class notouchitsclass {
    public $data;

    public function __construct($data) {
        $this->data = $data;
    }

    public function __destruct() {
        eval($this->data);
    }
}

class SessionRandom {

    public function generateRandomString() {
    $length = rand(1, 50);

    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';

    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }

    return $randomString;
    }


}

class SessionManager {
    private $sessionPath;
    private $sessionId;
    private $sensitiveFunctions = ['system', 'eval', 'exec', 'passthru', 'shell_exec', 'popen', 'proc_open'];

    public function __construct() {
        if (session_status() == PHP_SESSION_NONE) {
            throw new Exception("Session has not been started. Please start a session before using this class.");
        }
        $this->sessionPath = session_save_path();
        $this->sessionId = session_id();
    }

    private function getSessionFilePath() {
        return $this->sessionPath . "/sess_" . $this->sessionId;
    }

    public function filterSensitiveFunctions() {
        $sessionFile = $this->getSessionFilePath();

        if (file_exists($sessionFile)) {
            $sessionData = file_get_contents($sessionFile);

            foreach ($this->sensitiveFunctions as $function) {
                if (strpos($sessionData, $function) !== false) {
                    $sessionData = str_replace($function, '', $sessionData);
                }
            }
            file_put_contents($sessionFile, $sessionData);

            return "Sensitive functions have been filtered from the session file.";
        } else {
            return "Session file not found.";
        }
    }
}
