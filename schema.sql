DROP DATABASE IF EXISTS net;
CREATE DATABASE net;


DROP USER IF EXISTS 'worker'@'localhost';
CREATE USER 'worker'@'localhost' IDENTIFIED BY 'forwh4t_subnet';
GRANT ALL on net.* TO 'worker'@'localhost';

USE net;
CREATE TABLE computers
(
	`alias` varchar(400), PRIMARY KEY(`alias`),
	`username` varchar(400),
	`pid` int,
	`ip` varchar(20),
	`geo` varchar(1024)
);

CREATE TABLE proxies
(
	`cookie` varchar(64),
	`proxy` varchar(400)
);
