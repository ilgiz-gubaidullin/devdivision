DROP DATABASE IF EXISTS vkeducation;

CREATE DATABASE vkeducation;

USE vkeducation;

DROP TABLE IF EXISTS test_users;

CREATE TABLE `test_users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `surname` varchar(255) NOT NULL,
    `middle_name` varchar(255) DEFAULT NULL,
    `username` varchar(16) DEFAULT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(64) NOT NULL,
    `access` smallint DEFAULT NULL,
    `active` smallint DEFAULT NULL,
    `start_active_time` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`),
    UNIQUE KEY `ix_test_users_username` (`username`)
);

INSERT test_users(name, surname, username, password, email, access, active)
VALUES ('Main', 'User', 'main_user', 'password', 'qwe@qwe.qwe', 1, 0);

INSERT test_users(name, surname, username, password, email, access, active)
VALUES ('Blocked', 'User1', 'blocked_user1', 'blocked_user1', 'blocked_user1@qwe.qwe', 0, 0);

INSERT test_users(name, surname, username, password, email, access, active)
VALUES ('Blocked', 'User2', 'blocked_user2', 'blocked_user2', 'blocked_user2@qwe.qwe', 0, 0);

CREATE USER 'test_qa' IDENTIFIED BY 'qa_test';

GRANT ALL PRIVILEGES ON vkeducation.test_users TO 'test_qa';

FLUSH PRIVILEGES;
