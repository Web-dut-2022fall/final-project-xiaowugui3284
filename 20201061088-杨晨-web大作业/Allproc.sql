-- MySQL dump 10.13  Distrib 5.6.21, for osx10.8 (x86_64)
-- 
-- Host: localhost    Database : mclass
-- ------------------------------------------------------
-- Server version	5.6.21


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 
-- Table structure for table `tb_manager`
-- 
DROP TABLE IF EXISTS `tb_manager`;
CREATE TABLE `tb_manager` (
	`manager_id` bigint(20) NOT NULL AUTO_INCREMENT,
	`manager_account` varchar(40) DEFAULT NULL,
	`manager_level` varchar(10) DEFAULT NULL,
	`manager_password` varchar(256) DEFAULT NULL,
	PRIMARY KEY(`manager_id`)
	) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;


-- 
-- Dumping data for table `tb_manager`
-- 
LOCK TABLES `tb_manager` WRITE;
INSERT INTO `tb_manager` VALUES('1', 'root1234', 'root管理员', 'pbkdf2:sha1:1000$yyA2IvmG$246ea3e3b5fd122ee6fcea4b48971174b4edcf97');
UNLOCK TABLES;


-- 
-- Table structure for table `tb_user`
-- 
DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user` (
	`user_id` bigint(20) NOT NULL AUTO_INCREMENT,
	`user_account` varchar(40) DEFAULT NULL,
	`user_password` varchar(256) DEFAULT NULL,
	`user_name` varchar(40) DEFAULT NULL,
	`user_sex` varchar(2) DEFAULT NULL,
	`user_mail` varchar(40) DEFAULT NULL,
	`user_loc` varchar(80) DEFAULT NULL,
	PRIMARY KEY(`user_id`)
	) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;
	

-- 
-- Table structure for table `tb_class`
-- 
DROP TABLE IF EXISTS `tb_class`;
CREATE TABLE `tb_class` (
	`class_id` bigint(20) NOT NULL AUTO_INCREMENT,
	`class_title` varchar(40) DEFAULT NULL,
	PRIMARY KEY(`class_id`)
	) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;


-- 
-- Table structure for table `tb_userclass`
-- 
DROP TABLE IF EXISTS `tb_userclass`;
CREATE TABLE `tb_userclass` (
	`user_id` bigint(20) NOT NULL,
	`class_id` bigint(20) NOT NULL,
	PRIMARY KEY(`user_id`,`class_id`)
	);


-- 
-- Table structure for table `tb_notice`
-- 

DROP TABLE IF EXISTS `tb_notice`;
CREATE TABLE `tb_notice` (
	`no_id` bigint(20) NOT NULL AUTO_INCREMENT,
	`no_title` varchar(40) DEFAULT NULL,
	`no_desc` varchar(1000) DEFAULT NULL,
	`no_class_id` bigint(20) DEFAULT NULL,
	`no_date` date DEFAULT NULL,
	PRIMARY KEY(`no_id`)
	) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;
	
	
-- 
-- Table structure for table `tb_memo`
-- 

DROP TABLE IF EXISTS `tb_memo`;
CREATE TABLE `tb_memo` (
	`memo_id` bigint(20) NOT NULL AUTO_INCREMENT,
	`memo_title` varchar(40) DEFAULT NULL,
	`memo_desc` varchar(1000) DEFAULT NULL,
	`memo_user_id` bigint(20) DEFAULT NULL,
	`memo_date` datetime DEFAULT NULL,
	PRIMARY KEY(`memo_id`)
	) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;


--
-- Create User Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_createUser`(
IN p_account VARCHAR(40),
IN p_password VARCHAR(256)
)
BEGIN
if (select exists(select 1 from tb_user where user_account = p_account)) THEN
select '用户已经存在!';

ELSE
insert into tb_user(user_account,user_password)
values(p_account,p_password);

END IF;
END;;
DELIMITER ;


--
-- Create deleteUser Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_deleteUser`(
IN p_id bigint(20)
)
BEGIN
delete from tb_user where user_id = p_id;
delete from tb_memo where memo_user_id = p_id;
END;;
DELIMITER ;


--
-- Create getallUser Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getallUser`()
BEGIN
select user_id,user_name,user_sex,user_loc,user_mail from tb_user;
END;;
DELIMITER ;


--
-- Create getUser_byid Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getUser_byid`(
IN p_id bigint(20)
)
BEGIN
select user_name,user_sex,user_loc,user_mail from tb_user where user_id = p_id;
END;;
DELIMITER ;


--
-- Create getUserpsw_byid Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getUserpsw_byid`(
IN p_id bigint(20)
)
BEGIN
select user_password from tb_user where user_id = p_id;
END;;
DELIMITER ;


--
-- Create updateUserpsw Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_updateUserpsw`(
IN p_id bigint(20),
IN p_password VARCHAR(256)
)
BEGIN
update tb_user set user_password=p_password 
where user_id = p_id;
END;;
DELIMITER ;


--
-- Create updateUserinfo Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_updateUserinfo`(
IN p_id bigint(20),
IN p_name VARCHAR(40),
IN p_sex VARCHAR(2),
IN p_loc VARCHAR(80),
IN p_mail VARCHAR(40)
)
BEGIN
update tb_user set user_name=p_name,user_sex=p_sex,user_mail=p_mail,user_loc=p_loc 
where user_id = p_id;
END;;
DELIMITER ;


--
-- Create validateUserlogin Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_validateUserlogin`(
IN p_account VARCHAR(40)
)
BEGIN
select user_id,user_password from tb_user where user_account = p_account;
END;;
DELIMITER ;


--
-- Create createMemo Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_createMemo`(
IN p_title VARCHAR(40),
IN p_desc VARCHAR(1000),
IN p_userid bigint(20)
)
BEGIN
if (select exists(select 1 from tb_memo where memo_title = p_title and memo_user_id=p_userid)) THEN
select '备忘录已经存在!';

ELSE
insert into tb_memo(memo_title,memo_desc,memo_user_id,memo_date)
values(p_title,p_desc,p_userid,NOW());

END IF;
END;;
DELIMITER ;


--
-- Create deleteMemo Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_deleteMemo`(
IN p_id bigint(20)
)
BEGIN
delete from tb_memo where memo_id = p_id;
END;;
DELIMITER ;


--
-- Create getMemo_byuser Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getMemo_byuser`(
IN p_userid bigint(20)
)
BEGIN
select memo_id,memo_title,memo_desc,memo_date from tb_memo where memo_user_id = p_userid;
END;;
DELIMITER ;


--
-- Create getMemo_byid Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getMemo_byid`(
IN p_id bigint(20)
)
BEGIN
select memo_id,memo_title,memo_desc from tb_memo where memo_id = p_id;
END;;
DELIMITER ;


--
-- Create updateMemo Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_updateMemo`(
IN p_id bigint(20),
IN p_title VARCHAR(40),
IN p_desc VARCHAR(1000),
IN p_userid bigint(20)
)
BEGIN
update tb_memo set memo_title=p_title,memo_desc=p_desc,memo_user_id=p_userid,memo_date=NOW()
where memo_id = p_id;
END;;
DELIMITER ;


--
-- Create searchMemo Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_searchMemo`(
IN p_content VARCHAR(40),
IN p_userid bigint(20)
)
BEGIN
select memo_id,memo_title,memo_desc,memo_date from tb_memo where memo_user_id=p_userid and memo_title like concat('%',p_content,'%');
END;;
DELIMITER ;


--
-- Create validateManagerlogin Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_validateManagerlogin`(
IN p_account VARCHAR(40)
)
BEGIN
select manager_id,manager_password from tb_manager where manager_account = p_account;
END;;
DELIMITER ;


--
-- Create Manager Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_createManager`(
IN p_account VARCHAR(40),
IN p_password VARCHAR(256)
)
BEGIN
if (select exists(select 1 from tb_manager where manager_account = p_account)) THEN
select '管理员已经存在！';

ELSE
insert into tb_manager(manager_account,manager_level,manager_password)
values(p_account,'普通管理员',p_password);

END IF;
END;;
DELIMITER ;


--
-- Create deleteManager Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_deleteManager`(
IN p_id bigint(20)
)
BEGIN
delete from tb_manager where manager_id = p_id;
END;;
DELIMITER ;


--
-- Create getallManager Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getallManager`()
BEGIN
select manager_id,manager_account,manager_level from tb_manager;
END;;
DELIMITER ;


--
-- Create getManager_byid Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getManager_byid`(
IN p_id bigint(20)
)
BEGIN
select manager_id,manager_account,manager_level from tb_manager where manager_id = p_id;
END;;
DELIMITER ;


--
-- Create getManagerpsw_byid Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getManagerpsw_byid`(
IN p_id bigint(20)
)
BEGIN
select manager_password from tb_manager where manager_id = p_id;
END;;
DELIMITER ;


--
-- Create updateManagerpsw Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_updateManagerpsw`(
IN p_id bigint(20),
IN p_password VARCHAR(256)
)
BEGIN
update tb_manager set manager_password=p_password 
where manager_id = p_id;
END;;
DELIMITER ;



--
-- Create searchManager Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_searchManager`(
IN p_content VARCHAR(40)
)
BEGIN
select manager_id,manager_account,manager_level from tb_manager where manager_account like concat('%',p_content,'%');
END;;
DELIMITER ;


--
-- Create Class Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_createClass`(
IN p_title VARCHAR(40)
)
BEGIN
if (select exists(select 1 from tb_class where class_title = p_title)) THEN
select '班级已经存在!';

ELSE
insert into tb_class(class_title)
values(p_title);

END IF;
END;;
DELIMITER ;


--
-- Create deleteClass Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_deleteClass`(
IN p_id bigint(20)
)
BEGIN
delete from tb_class where class_id = p_id;
delete from tb_notice where no_class_id = p_id;
delete from tb_userclass where class_id = p_id;
END;;
DELIMITER ;


--
-- Create getallClass Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getallClass`()
BEGIN
select * from tb_class;
END;;
DELIMITER ;


--
-- Create getClass_byid Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getClass_byid`(
IN p_id bigint(20)
)
BEGIN
select * from tb_class where class_id = p_id;
END;;
DELIMITER ;


--
-- Create updateClass_byid Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_updateClass_byid`(
IN p_id bigint(20),
IN p_title VARCHAR(40)
)
BEGIN
update tb_class set class_title=p_title where class_id = p_id;
END;;
DELIMITER ;

--
-- Create searchClass Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_searchClass`(
IN p_content VARCHAR(40)
)
BEGIN
select * from tb_class where class_title like concat('%',p_content,'%');
END;;
DELIMITER ;


--
-- Create createNotice Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_createNotice`(
IN p_title VARCHAR(40),
IN p_desc VARCHAR(1000),
IN p_class_id bigint(20)
)
BEGIN
if (select exists(select 1 from tb_notice where no_title = p_title and no_class_id=p_class_id)) THEN
select '该公告已经存在';

ELSE
insert into tb_notice(no_title,no_desc,no_class_id,no_date)
values(p_title,p_desc,p_class_id,NOW());

END IF;
END;;
DELIMITER ;


--
-- Create deleteNotice Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_deleteNotice`(
IN p_id bigint(20)
)
BEGIN
delete from tb_notice where no_id = p_id;
END;;
DELIMITER ;


--
-- Create getallNotice Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getallNotice`(
IN p_class_id bigint(20)
)
BEGIN
select no_id,no_title,no_desc,no_date from tb_notice where no_class_id = p_class_id;
END;;
DELIMITER ;


--
-- Create getNotice_byid Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getNotice_byid`(
IN p_id bigint(20)
)
BEGIN
select no_title,no_desc from tb_notice where no_id = p_id;
END;;
DELIMITER ;


--
-- Create updateNotice Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_updateNotice`(
IN p_id bigint(20),
IN p_title VARCHAR(40),
IN p_desc VARCHAR(1000)
)
BEGIN
update tb_notice set no_title=p_title,no_desc=p_desc,no_date=NOW()
where no_id = p_id;
END;;
DELIMITER ;


--
-- Create searchNotice Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_searchNotice`(
IN p_class_id bigint(20),
IN p_content VARCHAR(40)
)
BEGIN
select no_id,no_title,no_desc,no_date from tb_notice where no_class_id=p_class_id and no_title like concat('%',p_content,'%');
END;;
DELIMITER ;


--
-- Create addClassmate Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_addClassmate`(
IN p_uid bigint(20),
IN p_cid bigint(20)
)
BEGIN
if (select exists(select 1 from tb_userclass where p_uid = user_id and p_cid = class_id)) THEN
select '该用户已经存在于该班级中!';

ELSE
insert into tb_userclass(user_id,class_id)
values(p_uid,p_cid);

END IF;
END;;
DELIMITER ;


--
-- Create deleteUser_fromClass Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_deleteUser_fromClass`(
IN p_uid bigint(20),
IN p_cid bigint(20)
)
BEGIN
delete from tb_userclass where user_id = p_uid and class_id=p_cid;
END;;
DELIMITER ;


--
-- Create getUser_byclass Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getUser_byclass`(
IN p_class_id bigint(20)
)
BEGIN
select user_id,user_name,user_sex,user_loc,user_mail from tb_user where user_id in (select user_id from tb_userclass where class_id = p_class_id);
END;;
DELIMITER ;


--
-- Create searchUser_byName Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_searchUser_byName`(
IN p_class_id bigint(20),
IN p_content VARCHAR(40)
)
BEGIN
select user_id,user_name,user_sex,user_loc,user_mail from tb_user where user_id in (select user_id from tb_userclass where class_id = p_class_id) and user_name like concat('%',p_content,'%');
END;;
DELIMITER ;


--
-- Create searchUser_bySex Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_searchUser_bySex`(
IN p_class_id bigint(20),
IN p_content VARCHAR(40)
)
BEGIN
select user_id,user_name,user_sex,user_loc,user_mail from tb_user where user_id in (select user_id from tb_userclass where class_id = p_class_id) and user_sex = p_content;
END;;
DELIMITER ;


--
-- Create searchUser_byLoc Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_searchUser_byLoc`(
IN p_class_id bigint(20),
IN p_content VARCHAR(40)
)
BEGIN
select user_id,user_name,user_sex,user_loc,user_mail from tb_user where user_id in (select user_id from tb_userclass where class_id = p_class_id) and user_loc like concat('%',p_content,'%');
END;;
DELIMITER ;


--
-- Create searchUser_byEmail Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_searchUser_byEmail`(
IN p_class_id bigint(20),
IN p_content VARCHAR(40)
)
BEGIN
select user_id,user_name,user_sex,user_loc,user_mail from tb_user where user_id in (select user_id from tb_userclass where class_id = p_class_id) and user_mail=p_content;
END;;
DELIMITER ;