CREATE USER 'api'@'%' IDENTIFIED BY 'passw0rd';
CREATE USER 'api'@'localhost' IDENTIFIED BY 'passw0rd';
CREATE ROLE 'api_role'@'localhost';
GRANT SELECT, UPDATE, INSERT, DELETE ON zukan_db.* TO 'api_role'@'localhost';
GRANT 'api_role'@'localhost' TO 'api'@'%';
GRANT 'api_role'@'localhost' TO 'api'@'localhost';
SET DEFAULT ROLE 'api_role'@'localhost' TO 'api'@'%';
SET DEFAULT ROLE 'api_role'@'localhost' TO 'api'@'localhost';

create database zukan_db;

use zukan_db;

CREATE TABLE zukan (
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     user_id VARCHAR(12) NOT NULL,
     title VARCHAR(60) NOT NULL,
     image_data MEDIUMBLOB,
     image_label TEXT DEFAULT NULL,
     comment TEXT DEFAULT NULL,
     PRIMARY KEY (id)
);
