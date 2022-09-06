--SCRIPT THAT CREATE THE DATABASE hbnb_dev_db
--script that prepares a MySQL server for the project:
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IS NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY hbnb_dev_pwd;
GRANT ALL ON hbnb_test_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON perfonmance_schema.* TO 'hbnb_dev'@'localhost';
