create database IF NOT EXISTS dev_db;
CREATE USER 'dev_user'@'localhost' IDENTIFIED BY 'dev_password';
GRANT ALL PRIVILEGES ON dev_db . * TO 'dev_user'@'localhost';