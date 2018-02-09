-- 建表语句
CREATE TABLE novel_test (
        `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `name` varchar(255) DEFAULT NULL,
        `author` varchar(255) DEFAULT NULL,
        `novelurl` varchar(255) ,
        `status` varchar(255) ,
        `number` varchar(255) ,
        `category` varchar(255) ,
        `novelid` varchar(255) ,
        `collect` varchar(255) ,
        `push` varchar(255) ,
        `lastupdate` varchar(255)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
