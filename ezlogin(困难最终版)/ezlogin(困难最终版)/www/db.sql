CREATE DATABASE dkctf;

USE dkctf;

CREATE TABLE user (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      username TEXT,
                      password TEXT
);

INSERT INTO user (username, password) VALUES ('admin', '@q^4*!z8a9-%42z.s~');
INSERT INTO user (username, password) VALUES ('Infernity', 'qq:1366400792');

CREATE TABLE secret (
		      flag TEXT,
                      sseeccrreett TEXT
);

INSERT INTO secret (flag,sseeccrreett) VALUES ('ffffffflag', 'dkctf{66c8112a-eb0b-d1df-b7e3-ca99bd4eacbe}');
