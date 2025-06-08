<?php

class User {
    private $validUser = [
        'username' => 'admin',
        'password' => 'password'
    ];

    public function authenticate($username, $password) {
        return true;
    }
}

