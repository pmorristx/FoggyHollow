-- MySQL dump 10.15  Distrib 10.0.32-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: 
-- ------------------------------------------------------
-- Server version	10.0.32-MariaDB-0+deb8u1

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
-- Current Database: `foggyhollow`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `foggyhollow` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `foggyhollow`;

--
-- Table structure for table `application_properties`
--

DROP TABLE IF EXISTS `application_properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `application_properties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `propName` varchar(45) NOT NULL,
  `propValue` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application_properties`
--

LOCK TABLES `application_properties` WRITE;
/*!40000 ALTER TABLE `application_properties` DISABLE KEYS */;
INSERT INTO `application_properties` VALUES (1,'accessMode','public');
/*!40000 ALTER TABLE `application_properties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `connecting_time_table`
--

DROP TABLE IF EXISTS `connecting_time_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `connecting_time_table` (
  `trainNumber` int(11) NOT NULL,
  `connectingTrainNumber` int(11) DEFAULT NULL,
  `connectingSegment` varchar(20) DEFAULT NULL,
  `arlv` varchar(2) NOT NULL,
  `scheduledTime` time NOT NULL,
  `locationCode` varchar(20) NOT NULL,
  `locationName` varchar(45) DEFAULT NULL,
  `segmentCode` varchar(20) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4092 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `connecting_time_table`
--

LOCK TABLES `connecting_time_table` WRITE;
/*!40000 ALTER TABLE `connecting_time_table` DISABLE KEYS */;
INSERT INTO `connecting_time_table` VALUES (3,NULL,NULL,'Lv','08:00:00','FH','Foggy Hollow','FH-CC',3916),(3,NULL,NULL,'Lv','08:35:00','FE','Fort Eureka','FH-CC',3917),(3,NULL,NULL,'Ar','09:34:00','CC','Colorado City','FH-CC',3918),(3,NULL,NULL,'Lv','09:49:00','CC','Colorado City','CC-DG',3919),(3,NULL,NULL,'Ar','10:47:00','DG','Devil\'s Gulch','CC-DG',3920),(3,NULL,NULL,'Lv','10:57:00','DG','Devil\'s Gulch','DG-E',3921),(3,NULL,NULL,'Lv','11:28:00','SC','Silver City','DG-E',3922),(3,NULL,NULL,'Ar','12:00:00','E','Empire','DG-E',3923),(3,NULL,NULL,'Lv','12:05:00','E','Empire','E-ES',3924),(3,NULL,NULL,'Ar','13:16:00','ES','Excelsior Springs','E-ES',3925),(4,NULL,NULL,'Lv','13:30:00','ES','Excelsior Springs','ES-E',3926),(4,NULL,NULL,'Ar','14:32:00','E','Empire','ES-E',3927),(4,NULL,NULL,'Lv','14:37:00','E','Empire','E-DG',3928),(4,NULL,NULL,'Lv','15:05:00','SC','Silver City','E-DG',3929),(4,NULL,NULL,'Ar','15:33:00','DG','Devil\'s Gulch','E-DG',3930),(4,NULL,NULL,'Lv','15:53:00','DG','Devil\'s Gulch','DG-CC',3931),(4,NULL,NULL,'Ar','16:45:00','CC','Colorado City','DG-CC',3932),(4,NULL,NULL,'Lv','16:55:00','CC','Colorado City','CC-FH',3933),(4,NULL,NULL,'Lv','17:49:00','FE','Fort Eureka','CC-FH',3934),(4,NULL,NULL,'Ar','18:21:00','FH','Foggy Hollow','CC-FH',3935),(5,NULL,NULL,'Lv','10:15:00','CC','Colorado City','CC-LC',3936),(5,NULL,NULL,'Lv','10:43:00','FR','Fall River','CC-LC',3937),(5,NULL,NULL,'Ar','11:22:00','LC','Lost Creek','CC-LC',3938),(5,3,'FH-CC','Lv','08:00:00','FH','Foggy Hollow','',3939),(5,3,'FH-CC','Lv','08:35:00','FE','Fort Eureka','',3940),(5,3,'FH-CC','Ar','09:34:00','CC','Colorado City','',3941),(6,NULL,NULL,'Lv','14:00:00','LC','Lost Creek','LC-CC',3942),(6,NULL,NULL,'Lv','14:35:00','FR','Fall River','LC-CC',3943),(6,NULL,NULL,'Ar','15:00:00','CC','Colorado City','LC-CC',3944),(6,4,'CC-FH','Lv','16:55:00','CC','Colorado City','',3945),(6,4,'CC-FH','Lv','17:49:00','FE','Fort Eureka','',3946),(6,4,'CC-FH','Ar','18:21:00','FH','Foggy Hollow','',3947),(7,NULL,NULL,'Lv','11:15:00','DG','Devil\'s Gulch','DG-MS',3948),(7,NULL,NULL,'Lv','11:48:00','FG','Faun Glen','DG-MS',3949),(7,NULL,NULL,'Lv','12:23:00','BB','Beaver Bend','DG-MS',3950),(7,NULL,NULL,'Ar','13:06:00','MS','Mystic Springs','DG-MS',3951),(7,3,'FH-CC','Lv','08:00:00','FH','Foggy Hollow','',3952),(7,3,'FH-CC','Lv','08:35:00','FE','Fort Eureka','',3953),(7,3,'FH-CC','Ar','09:34:00','CC','Colorado City','',3954),(7,3,'CC-DG','Lv','09:49:00','CC','Colorado City','',3955),(7,3,'CC-DG','Ar','10:47:00','DG','Devil\'s Gulch','',3956),(8,NULL,NULL,'Lv','13:30:00','MS','Mystic Springs','MS-DG',3957),(8,NULL,NULL,'Lv','14:08:00','BB','Beaver Bend','MS-DG',3958),(8,NULL,NULL,'Lv','14:39:00','FG','Faun Glen','MS-DG',3959),(8,NULL,NULL,'Ar','15:08:00','DG','Devil\'s Gulch','MS-DG',3960),(8,4,'DG-CC','Lv','15:53:00','DG','Devil\'s Gulch','',3961),(8,4,'DG-CC','Ar','16:45:00','CC','Colorado City','',3962),(8,4,'CC-FH','Lv','16:55:00','CC','Colorado City','',3963),(8,4,'CC-FH','Lv','17:49:00','FE','Fort Eureka','',3964),(8,4,'CC-FH','Ar','18:21:00','FH','Foggy Hollow','',3965),(9,NULL,NULL,'Lv','11:25:00','DG','Devil\'s Gulch','DG-E',3966),(9,NULL,NULL,'Lv','11:56:00','SC','Silver City','DG-E',3967),(9,NULL,NULL,'Ar','12:28:00','E','Empire','DG-E',3968),(9,NULL,NULL,'Lv','12:38:00','E','Empire','E-SG',3969),(9,NULL,NULL,'Ar','13:52:00','SG','Satyr\'s Glade','E-SG',3970),(9,3,'FH-CC','Lv','08:00:00','FH','Foggy Hollow','',3971),(9,3,'FH-CC','Lv','08:35:00','FE','Fort Eureka','',3972),(9,3,'FH-CC','Ar','09:34:00','CC','Colorado City','',3973),(9,3,'CC-DG','Lv','09:49:00','CC','Colorado City','',3974),(9,3,'CC-DG','Ar','10:47:00','DG','Devil\'s Gulch','',3975),(10,NULL,NULL,'Lv','13:30:00','SG','Satyr\'s Glade','SG-E',3976),(10,NULL,NULL,'Ar','14:35:00','E','Empire','SG-E',3977),(10,NULL,NULL,'Lv','14:45:00','E','Empire','E-DG',3978),(10,NULL,NULL,'Lv','15:13:00','SC','Silver City','E-DG',3979),(10,NULL,NULL,'Ar','15:41:00','DG','Devil\'s Gulch','E-DG',3980),(10,4,'DG-CC','Lv','15:53:00','DG','Devil\'s Gulch','',3981),(10,4,'DG-CC','Ar','16:45:00','CC','Colorado City','',3982),(10,4,'CC-FH','Lv','16:55:00','CC','Colorado City','',3983),(10,4,'CC-FH','Lv','17:49:00','FE','Fort Eureka','',3984),(10,4,'CC-FH','Ar','18:21:00','FH','Foggy Hollow','',3985),(11,NULL,NULL,'Lv','00:00:00','FH','Foggy Hollow','FH-DG',3986),(11,NULL,NULL,'Lv','02:33:00','DG','Devil\'s Gulch','DGMSX',3987),(11,NULL,NULL,'Ar','04:30:00','ES','Excelsior Springs','DGMSX',3988),(12,NULL,NULL,'Lv','05:00:00','ES','Excelsior Springs','MSDGX',3989),(12,NULL,NULL,'Lv','06:38:00','DG','Devil\'s Gulch','DG-FH',3990),(12,NULL,NULL,'Ar','08:50:00','FH','Foggy Hollow','DG-FH',3991),(15,NULL,NULL,'Lv','15:00:00','DG','Devil\'s Gulch','DG-E',3992),(15,NULL,NULL,'Lv','15:31:00','SC','Silver City','DG-E',3993),(15,NULL,NULL,'Ar','16:03:00','E','Empire','DG-E',3994),(15,NULL,NULL,'Lv','16:08:00','E','Empire','E-ES',3995),(15,NULL,NULL,'Ar','17:19:00','ES','Excelsior Springs','E-ES',3996),(16,NULL,NULL,'Lv','09:00:00','ES','Excelsior Springs','ES-E',3997),(16,NULL,NULL,'Ar','10:02:00','E','Empire','ES-E',3998),(16,NULL,NULL,'Lv','10:07:00','E','Empire','E-DG',3999),(16,NULL,NULL,'Lv','10:35:00','SC','Silver City','E-DG',4000),(16,NULL,NULL,'Ar','11:03:00','DG','Devil\'s Gulch','E-DG',4001),(17,NULL,NULL,'Lv','15:15:00','DG','Devil\'s Gulch','DG-E',4002),(17,NULL,NULL,'Lv','15:46:00','SC','Silver City','DG-E',4003),(17,NULL,NULL,'Lv','16:18:00','E','Empire','E-SG',4004),(17,NULL,NULL,'Ar','17:32:00','SG','Satyr\'s Glade','E-SG',4005),(18,NULL,NULL,'Lv','09:00:00','SG','Satyr\'s Glade','SG-E',4006),(18,NULL,NULL,'Lv','10:05:00','E','Empire','E-DG',4007),(18,NULL,NULL,'Lv','10:33:00','SC','Silver City','E-DG',4008),(18,NULL,NULL,'Ar','11:01:00','DG','Devil\'s Gulch','E-DG',4009),(19,NULL,NULL,'Lv','18:00:00','FH','Foggy Hollow','FH-CC',4010),(19,NULL,NULL,'Lv','18:35:00','FE','Fort Eureka','FH-CC',4011),(19,NULL,NULL,'Ar','19:34:00','CC','Colorado City','FH-CC',4012),(19,NULL,NULL,'Lv','19:54:00','CC','Colorado City','CC-DG',4013),(19,NULL,NULL,'Ar','20:52:00','DG','Devil\'s Gulch','CC-DG',4014),(19,NULL,NULL,'Lv','20:57:00','DG','Devil\'s Gulch','DG-E',4015),(19,NULL,NULL,'Lv','21:28:00','SC','Silver City','DG-E',4016),(19,NULL,NULL,'Ar','22:00:00','E','Empire','DG-E',4017),(19,NULL,NULL,'Lv','22:20:00','E','Empire','E-SG',4018),(19,NULL,NULL,'Ar','23:34:00','SG','Satyr\'s Glade','E-SG',4019),(20,NULL,NULL,'Lv','02:30:00','SG','Satyr\'s Glade','SG-E',4020),(20,NULL,NULL,'Ar','03:35:00','E','Empire','SG-E',4021),(20,NULL,NULL,'Lv','03:40:00','E','Empire','E-DG',4022),(20,NULL,NULL,'Lv','04:08:00','SC','Silver City','E-DG',4023),(20,NULL,NULL,'Ar','04:36:00','DG','Devil\'s Gulch','E-DG',4024),(20,NULL,NULL,'Lv','04:46:00','DG','Devil\'s Gulch','DG-CC',4025),(20,NULL,NULL,'Ar','05:38:00','CC','Colorado City','DG-CC',4026),(20,NULL,NULL,'Lv','05:48:00','CC','Colorado City','CC-FH',4027),(20,NULL,NULL,'Lv','06:42:00','FE','Fort Eureka','CC-FH',4028),(20,NULL,NULL,'Ar','07:14:00','FH','Foggy Hollow','CC-FH',4029),(21,NULL,NULL,'Lv','03:50:00','E','Empire','E-ES',4030),(21,NULL,NULL,'Ar','05:01:00','ES','Excelsior Springs','E-ES',4031),(21,20,'SG-E','Lv','02:30:00','SG','Satyr\'s Glade','',4032),(21,20,'SG-E','Ar','03:35:00','E','Empire','',4033),(22,NULL,NULL,'Lv','21:00:00','ES','Excelsior Springs','ES-E',4034),(22,NULL,NULL,'Ar','22:02:00','E','Empire','ES-E',4035),(22,19,'E-SG','Lv','22:20:00','E','Empire','',4036),(22,19,'E-SG','Ar','23:34:00','SG','Satyr\'s Glade','',4037),(23,NULL,NULL,'Lv','04:50:00','DG','Devil\'s Gulch','DG-MS',4038),(23,NULL,NULL,'Lv','05:23:00','FG','Faun Glen','DG-MS',4039),(23,NULL,NULL,'Lv','05:58:00','BB','Beaver Bend','DG-MS',4040),(23,NULL,NULL,'Ar','06:41:00','MS','Mystic Springs','DG-MS',4041),(23,20,'SG-E','Lv','02:30:00','SG','Satyr\'s Glade','',4042),(23,20,'SG-E','Ar','03:35:00','E','Empire','',4043),(23,20,'E-DG','Lv','03:40:00','E','Empire','',4044),(23,20,'E-DG','Lv','04:08:00','SC','Silver City','',4045),(23,20,'E-DG','Ar','04:36:00','DG','Devil\'s Gulch','',4046),(24,NULL,NULL,'Lv','19:00:00','MS','Mystic Springs','MS-DG',4047),(24,NULL,NULL,'Lv','19:38:00','BB','Beaver Bend','MS-DG',4048),(24,NULL,NULL,'Lv','20:09:00','FG','Faun Glen','MS-DG',4049),(24,NULL,NULL,'Ar','20:38:00','DG','Devil\'s Gulch','MS-DG',4050),(24,19,'DG-E','Lv','20:57:00','DG','Devil\'s Gulch','',4051),(24,19,'DG-E','Lv','21:28:00','SC','Silver City','',4052),(24,19,'DG-E','Ar','22:00:00','E','Empire','',4053),(24,19,'E-SG','Lv','22:20:00','E','Empire','',4054),(24,19,'E-SG','Ar','23:34:00','SG','Satyr\'s Glade','',4055),(25,NULL,NULL,'Lv','06:00:00','CC','Colorado City','CC-LC',4056),(25,NULL,NULL,'Lv','06:28:00','FR','Fall River','CC-LC',4057),(25,NULL,NULL,'Ar','07:07:00','LC','Lost Creek','CC-LC',4058),(25,20,'SG-E','Lv','02:30:00','SG','Satyr\'s Glade','',4059),(25,20,'SG-E','Ar','03:35:00','E','Empire','',4060),(25,20,'E-DG','Lv','03:40:00','E','Empire','',4061),(25,20,'E-DG','Lv','04:08:00','SC','Silver City','',4062),(25,20,'E-DG','Ar','04:36:00','DG','Devil\'s Gulch','',4063),(25,20,'DG-CC','Lv','04:46:00','DG','Devil\'s Gulch','',4064),(25,20,'DG-CC','Ar','05:38:00','CC','Colorado City','',4065),(26,NULL,NULL,'Lv','18:15:00','LC','Lost Creek','LC-CC',4066),(26,NULL,NULL,'Lv','18:50:00','FR','Fall River','LC-CC',4067),(26,NULL,NULL,'Ar','19:15:00','CC','Colorado City','LC-CC',4068),(26,19,'CC-DG','Lv','19:54:00','CC','Colorado City','',4069),(26,19,'CC-DG','Ar','20:52:00','DG','Devil\'s Gulch','',4070),(26,19,'DG-E','Lv','20:57:00','DG','Devil\'s Gulch','',4071),(26,19,'DG-E','Lv','21:28:00','SC','Silver City','',4072),(26,19,'DG-E','Ar','22:00:00','E','Empire','',4073),(26,19,'E-SG','Lv','22:20:00','E','Empire','',4074),(26,19,'E-SG','Ar','23:34:00','SG','Satyr\'s Glade','',4075),(27,NULL,NULL,'Lv','09:00:00','MS','Mystic Springs','MS-DG',4076),(27,NULL,NULL,'Lv','09:38:00','BB','Beaver Bend','MS-DG',4077),(27,NULL,NULL,'Lv','10:09:00','FG','Faun Glen','MS-DG',4078),(27,NULL,NULL,'Ar','10:38:00','DG','Devil\'s Gulch','MS-DG',4079),(27,NULL,NULL,'Lv','11:23:00','DG','Devil\'s Gulch','DG-E',4080),(27,NULL,NULL,'Lv','11:54:00','SC','Silver City','DG-E',4081),(27,NULL,NULL,'Lv','12:26:00','E','Empire','E-ES',4082),(27,NULL,NULL,'Ar','13:37:00','ES','Excelsior Springs','E-ES',4083),(28,NULL,NULL,'Lv','09:00:00','ES','Excelsior Springs','ES-E',4084),(28,NULL,NULL,'Lv','10:02:00','E','Empire','E-DG',4085),(28,NULL,NULL,'Lv','10:30:00','SC','Silver City','E-DG',4086),(28,NULL,NULL,'Ar','10:58:00','DG','Devil\'s Gulch','E-DG',4087),(28,NULL,NULL,'Lv','11:43:00','DG','Devil\'s Gulch','DG-MS',4088),(28,NULL,NULL,'Lv','12:16:00','FG','Faun Glen','DG-MS',4089),(28,NULL,NULL,'Lv','12:51:00','BB','Beaver Bend','DG-MS',4090),(28,NULL,NULL,'Ar','13:34:00','MS','Mystic Springs','DG-MS',4091);
/*!40000 ALTER TABLE `connecting_time_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `connecting_train_segments`
--

DROP TABLE IF EXISTS `connecting_train_segments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `connecting_train_segments` (
  `trainNumber` int(11) NOT NULL,
  `connectingTrainNumber` int(11) NOT NULL,
  `connectingTrainSegment` varchar(20) NOT NULL,
  `connectingOrder` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `connecting_train_segments`
--

LOCK TABLES `connecting_train_segments` WRITE;
/*!40000 ALTER TABLE `connecting_train_segments` DISABLE KEYS */;
INSERT INTO `connecting_train_segments` VALUES (26,19,'CC-DG',1,1),(26,19,'DG-E',2,2),(26,19,'E-SG',3,3),(5,3,'FH-CC',1,4),(6,4,'CC-FH',1,5),(7,3,'FH-CC',1,6),(7,3,'CC-DG',2,7),(8,4,'DG-CC',1,8),(8,4,'CC-FH',2,9),(9,3,'FH-CC',1,10),(9,3,'CC-DG',2,11),(10,4,'DG-CC',1,12),(10,4,'CC-FH',2,13),(22,19,'E-SG',1,14),(21,20,'SG-E',1,15),(23,20,'SG-E',1,16),(23,20,'E-DG',2,17),(24,19,'DG-E',1,18),(24,19,'E-SG',2,19),(25,20,'SG-E',1,20),(25,20,'E-DG',2,21),(25,20,'DG-CC',3,22);
/*!40000 ALTER TABLE `connecting_train_segments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `connecting_trains`
--

DROP TABLE IF EXISTS `connecting_trains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `connecting_trains` (
  `trainNumber` int(11) NOT NULL,
  `connectingTrain` int(11) NOT NULL,
  `connectingRoute` int(11) DEFAULT NULL,
  `connectingRouteName` varchar(45) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `connecting_trains`
--

LOCK TABLES `connecting_trains` WRITE;
/*!40000 ALTER TABLE `connecting_trains` DISABLE KEYS */;
INSERT INTO `connecting_trains` VALUES (5,3,31,'FH-CC',1),(7,3,32,'FH-CC',2),(7,3,31,'CC-DG',3),(9,3,32,'FH-CC',4),(9,3,31,'CC-DG',5),(24,19,193,'DG-E',6),(24,19,45,'E-SG',7),(23,20,196,'SG-E',8),(6,4,43,'CC-FH',9),(26,19,193,'DG-E',10),(26,19,45,'E-SG',11),(26,19,32,'FH-CC',12),(25,20,196,'SG-E',13),(25,20,197,'E-DG',14),(22,19,45,'E-SG',15),(8,4,42,'DG-CC',16),(8,4,43,'CC-FH',17),(10,4,42,'DG-CC',18),(10,4,43,'CC-FH',19),(21,20,45,'E-SG',20),(23,20,197,'E-DG',21),(25,20,NULL,NULL,22);
/*!40000 ALTER TABLE `connecting_trains` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `locations` (
  `locationId` int(11) NOT NULL AUTO_INCREMENT,
  `locationCode` varchar(4) DEFAULT NULL,
  `locationName` varchar(45) NOT NULL,
  `milePost` float NOT NULL,
  `services` varchar(45) NOT NULL,
  `privateServices` varchar(20) DEFAULT NULL,
  `privateLocationName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`locationId`),
  UNIQUE KEY `Name_UNIQUE` (`locationName`),
  UNIQUE KEY `locationCode_UNIQUE` (`locationCode`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
INSERT INTO `locations` VALUES (1,'FH','Foggy Hollow',0,'ABTX','ABGTX',NULL),(2,'FE','Fort Eureka',15.72,'T','GT',NULL),(3,'BB','Beaver Bend',84.05,'ABMTX','ABGMTX',NULL),(4,'CC','Colorado City',41.85,'ABTX','ABGTX',NULL),(5,'DG','Devil\'s Gulch',62.74,'ABMTX','ABGMTX',NULL),(6,'E','Empire',82.85,'FT','FGLT','Priapus Junction'),(7,'ES','Excelsior Springs',104.16,'ABTX','ABGHSTX',NULL),(8,'FR','Fall River',51.88,'F','FGL',NULL),(9,'FG','Faun Glen',73.97,'FT','FGT','Pissing Falls'),(10,'SG','Satyr\'s Glade',105.45,'ABT','ABLST',NULL),(11,'MS','Mystic Springs',97.35,'ABTX','ABGHSTX',NULL),(12,'LC','Lost Creek',66.6,'ABTX','ABGTX',NULL),(13,'SC','Silver City',72.94,'F','FG',NULL);
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `private_time_table`
--

DROP TABLE IF EXISTS `private_time_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `private_time_table` (
  `trainNumber` int(11) NOT NULL,
  `connectingTrainNumber` int(11) DEFAULT NULL,
  `connectingSegment` varchar(20) DEFAULT NULL,
  `arlv` varchar(2) NOT NULL,
  `scheduledTime` time NOT NULL,
  `locationCode` varchar(20) NOT NULL,
  `locationName` varchar(45) DEFAULT NULL,
  `segmentCode` varchar(20) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1101 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `private_time_table`
--

LOCK TABLES `private_time_table` WRITE;
/*!40000 ALTER TABLE `private_time_table` DISABLE KEYS */;
INSERT INTO `private_time_table` VALUES (3,NULL,NULL,'Lv','08:00:00','FH','Foggy Hollow','FH-CC',925),(3,NULL,NULL,'Lv','08:35:00','FE','Fort Eureka','FH-CC',926),(3,NULL,NULL,'Ar','09:34:00','CC','Colorado City','FH-CC',927),(3,NULL,NULL,'Lv','09:49:00','CC','Colorado City','CC-DG',928),(3,NULL,NULL,'Ar','10:47:00','DG','Devil\'s Gulch','CC-DG',929),(3,NULL,NULL,'Lv','10:57:00','DG','Devil\'s Gulch','DG-E',930),(3,NULL,NULL,'Lv','11:28:00','SC','Silver City','DG-E',931),(3,NULL,NULL,'Ar','12:00:00','E','Empire','DG-E',932),(3,NULL,NULL,'Lv','12:05:00','E','Empire','E-ES',933),(3,NULL,NULL,'Ar','13:16:00','ES','Excelsior Springs','E-ES',934),(4,NULL,NULL,'Lv','13:30:00','ES','Excelsior Springs','ES-E',935),(4,NULL,NULL,'Ar','14:32:00','E','Empire','ES-E',936),(4,NULL,NULL,'Lv','14:37:00','E','Empire','E-DG',937),(4,NULL,NULL,'Lv','15:05:00','SC','Silver City','E-DG',938),(4,NULL,NULL,'Ar','15:33:00','DG','Devil\'s Gulch','E-DG',939),(4,NULL,NULL,'Lv','15:53:00','DG','Devil\'s Gulch','DG-CC',940),(4,NULL,NULL,'Ar','16:45:00','CC','Colorado City','DG-CC',941),(4,NULL,NULL,'Lv','16:55:00','CC','Colorado City','CC-FH',942),(4,NULL,NULL,'Lv','17:49:00','FE','Fort Eureka','CC-FH',943),(4,NULL,NULL,'Ar','18:21:00','FH','Foggy Hollow','CC-FH',944),(5,NULL,NULL,'Lv','10:15:00','CC','Colorado City','CC-LC',945),(5,NULL,NULL,'Lv','10:43:00','FR','Fall River','CC-LC',946),(5,NULL,NULL,'Ar','11:22:00','LC','Lost Creek','CC-LC',947),(5,3,'FH-CC','Lv','08:00:00','FH','Foggy Hollow','',948),(5,3,'FH-CC','Lv','08:35:00','FE','Fort Eureka','',949),(5,3,'FH-CC','Ar','09:34:00','CC','Colorado City','',950),(6,NULL,NULL,'Lv','14:00:00','LC','Lost Creek','LC-CC',951),(6,NULL,NULL,'Lv','14:35:00','FR','Fall River','LC-CC',952),(6,NULL,NULL,'Ar','15:00:00','CC','Colorado City','LC-CC',953),(6,4,'CC-FH','Lv','16:55:00','CC','Colorado City','',954),(6,4,'CC-FH','Lv','17:49:00','FE','Fort Eureka','',955),(6,4,'CC-FH','Ar','18:21:00','FH','Foggy Hollow','',956),(7,NULL,NULL,'Lv','11:15:00','DG','Devil\'s Gulch','DG-MS',957),(7,NULL,NULL,'Lv','11:48:00','FG','Faun Glen','DG-MS',958),(7,NULL,NULL,'Lv','12:23:00','BB','Beaver Bend','DG-MS',959),(7,NULL,NULL,'Ar','13:06:00','MS','Mystic Springs','DG-MS',960),(7,3,'FH-CC','Lv','08:00:00','FH','Foggy Hollow','',961),(7,3,'FH-CC','Lv','08:35:00','FE','Fort Eureka','',962),(7,3,'FH-CC','Ar','09:34:00','CC','Colorado City','',963),(7,3,'CC-DG','Lv','09:49:00','CC','Colorado City','',964),(7,3,'CC-DG','Ar','10:47:00','DG','Devil\'s Gulch','',965),(8,NULL,NULL,'Lv','13:30:00','MS','Mystic Springs','MS-DG',966),(8,NULL,NULL,'Lv','14:08:00','BB','Beaver Bend','MS-DG',967),(8,NULL,NULL,'Lv','14:39:00','FG','Faun Glen','MS-DG',968),(8,NULL,NULL,'Ar','15:08:00','DG','Devil\'s Gulch','MS-DG',969),(8,4,'DG-CC','Lv','15:53:00','DG','Devil\'s Gulch','',970),(8,4,'DG-CC','Ar','16:45:00','CC','Colorado City','',971),(8,4,'CC-FH','Lv','16:55:00','CC','Colorado City','',972),(8,4,'CC-FH','Lv','17:49:00','FE','Fort Eureka','',973),(8,4,'CC-FH','Ar','18:21:00','FH','Foggy Hollow','',974),(9,NULL,NULL,'Lv','11:25:00','DG','Devil\'s Gulch','DG-E',975),(9,NULL,NULL,'Lv','11:56:00','SC','Silver City','DG-E',976),(9,NULL,NULL,'Ar','12:28:00','E','Empire','DG-E',977),(9,NULL,NULL,'Lv','12:38:00','E','Empire','E-SG',978),(9,NULL,NULL,'Ar','13:52:00','SG','Satyr\'s Glade','E-SG',979),(9,3,'FH-CC','Lv','08:00:00','FH','Foggy Hollow','',980),(9,3,'FH-CC','Lv','08:35:00','FE','Fort Eureka','',981),(9,3,'FH-CC','Ar','09:34:00','CC','Colorado City','',982),(9,3,'CC-DG','Lv','09:49:00','CC','Colorado City','',983),(9,3,'CC-DG','Ar','10:47:00','DG','Devil\'s Gulch','',984),(10,NULL,NULL,'Lv','13:30:00','SG','Satyr\'s Glade','SG-E',985),(10,NULL,NULL,'Ar','14:35:00','E','Empire','SG-E',986),(10,NULL,NULL,'Lv','14:45:00','E','Empire','E-DG',987),(10,NULL,NULL,'Lv','15:13:00','SC','Silver City','E-DG',988),(10,NULL,NULL,'Ar','15:41:00','DG','Devil\'s Gulch','E-DG',989),(10,4,'DG-CC','Lv','15:53:00','DG','Devil\'s Gulch','',990),(10,4,'DG-CC','Ar','16:45:00','CC','Colorado City','',991),(10,4,'CC-FH','Lv','16:55:00','CC','Colorado City','',992),(10,4,'CC-FH','Lv','17:49:00','FE','Fort Eureka','',993),(10,4,'CC-FH','Ar','18:21:00','FH','Foggy Hollow','',994),(11,NULL,NULL,'Lv','00:00:00','FH','Foggy Hollow','FH-DG',995),(11,NULL,NULL,'Lv','02:33:00','DG','Devil\'s Gulch','DGMSX',996),(11,NULL,NULL,'Ar','04:30:00','ES','Excelsior Springs','DGMSX',997),(12,NULL,NULL,'Lv','05:00:00','ES','Excelsior Springs','MSDGX',998),(12,NULL,NULL,'Lv','06:38:00','DG','Devil\'s Gulch','DG-FH',999),(12,NULL,NULL,'Ar','08:50:00','FH','Foggy Hollow','DG-FH',1000),(15,NULL,NULL,'Lv','15:00:00','DG','Devil\'s Gulch','DG-E',1001),(15,NULL,NULL,'Lv','15:31:00','SC','Silver City','DG-E',1002),(15,NULL,NULL,'Ar','16:03:00','E','Empire','DG-E',1003),(15,NULL,NULL,'Lv','16:08:00','E','Empire','E-ES',1004),(15,NULL,NULL,'Ar','17:19:00','ES','Excelsior Springs','E-ES',1005),(16,NULL,NULL,'Lv','09:00:00','ES','Excelsior Springs','ES-E',1006),(16,NULL,NULL,'Ar','10:02:00','E','Empire','ES-E',1007),(16,NULL,NULL,'Lv','10:07:00','E','Empire','E-DG',1008),(16,NULL,NULL,'Lv','10:35:00','SC','Silver City','E-DG',1009),(16,NULL,NULL,'Ar','11:03:00','DG','Devil\'s Gulch','E-DG',1010),(17,NULL,NULL,'Lv','15:15:00','DG','Devil\'s Gulch','DG-E',1011),(17,NULL,NULL,'Lv','15:46:00','SC','Silver City','DG-E',1012),(17,NULL,NULL,'Lv','16:18:00','E','Empire','E-SG',1013),(17,NULL,NULL,'Ar','17:32:00','SG','Satyr\'s Glade','E-SG',1014),(18,NULL,NULL,'Lv','09:00:00','SG','Satyr\'s Glade','SG-E',1015),(18,NULL,NULL,'Lv','10:05:00','E','Empire','E-DG',1016),(18,NULL,NULL,'Lv','10:33:00','SC','Silver City','E-DG',1017),(18,NULL,NULL,'Ar','11:01:00','DG','Devil\'s Gulch','E-DG',1018),(19,NULL,NULL,'Lv','18:00:00','FH','Foggy Hollow','FH-CC',1019),(19,NULL,NULL,'Lv','18:35:00','FE','Fort Eureka','FH-CC',1020),(19,NULL,NULL,'Ar','19:34:00','CC','Colorado City','FH-CC',1021),(19,NULL,NULL,'Lv','19:54:00','CC','Colorado City','CC-DG',1022),(19,NULL,NULL,'Ar','20:52:00','DG','Devil\'s Gulch','CC-DG',1023),(19,NULL,NULL,'Lv','20:57:00','DG','Devil\'s Gulch','DG-E',1024),(19,NULL,NULL,'Lv','21:28:00','SC','Silver City','DG-E',1025),(19,NULL,NULL,'Ar','22:00:00','E','Empire','DG-E',1026),(19,NULL,NULL,'Lv','22:20:00','E','Empire','E-SG',1027),(19,NULL,NULL,'Ar','23:34:00','SG','Satyr\'s Glade','E-SG',1028),(20,NULL,NULL,'Lv','02:30:00','SG','Satyr\'s Glade','SG-E',1029),(20,NULL,NULL,'Ar','03:35:00','E','Empire','SG-E',1030),(20,NULL,NULL,'Lv','03:40:00','E','Empire','E-DG',1031),(20,NULL,NULL,'Lv','04:08:00','SC','Silver City','E-DG',1032),(20,NULL,NULL,'Ar','04:36:00','DG','Devil\'s Gulch','E-DG',1033),(20,NULL,NULL,'Lv','04:46:00','DG','Devil\'s Gulch','DG-CC',1034),(20,NULL,NULL,'Ar','05:38:00','CC','Colorado City','DG-CC',1035),(20,NULL,NULL,'Lv','05:48:00','CC','Colorado City','CC-FH',1036),(20,NULL,NULL,'Lv','06:42:00','FE','Fort Eureka','CC-FH',1037),(20,NULL,NULL,'Ar','07:14:00','FH','Foggy Hollow','CC-FH',1038),(21,NULL,NULL,'Lv','03:50:00','E','Empire','E-ES',1039),(21,NULL,NULL,'Ar','05:01:00','ES','Excelsior Springs','E-ES',1040),(21,20,'SG-E','Lv','02:30:00','SG','Satyr\'s Glade','',1041),(21,20,'SG-E','Ar','03:35:00','E','Empire','',1042),(22,NULL,NULL,'Lv','21:00:00','ES','Excelsior Springs','ES-E',1043),(22,NULL,NULL,'Ar','22:02:00','E','Empire','ES-E',1044),(22,19,'E-SG','Lv','22:20:00','E','Empire','',1045),(22,19,'E-SG','Ar','23:34:00','SG','Satyr\'s Glade','',1046),(23,NULL,NULL,'Lv','04:50:00','DG','Devil\'s Gulch','DG-MS',1047),(23,NULL,NULL,'Lv','05:23:00','FG','Faun Glen','DG-MS',1048),(23,NULL,NULL,'Lv','05:58:00','BB','Beaver Bend','DG-MS',1049),(23,NULL,NULL,'Ar','06:41:00','MS','Mystic Springs','DG-MS',1050),(23,20,'SG-E','Lv','02:30:00','SG','Satyr\'s Glade','',1051),(23,20,'SG-E','Ar','03:35:00','E','Empire','',1052),(23,20,'E-DG','Lv','03:40:00','E','Empire','',1053),(23,20,'E-DG','Lv','04:08:00','SC','Silver City','',1054),(23,20,'E-DG','Ar','04:36:00','DG','Devil\'s Gulch','',1055),(24,NULL,NULL,'Lv','19:00:00','MS','Mystic Springs','MS-DG',1056),(24,NULL,NULL,'Lv','19:38:00','BB','Beaver Bend','MS-DG',1057),(24,NULL,NULL,'Lv','20:09:00','FG','Faun Glen','MS-DG',1058),(24,NULL,NULL,'Ar','20:38:00','DG','Devil\'s Gulch','MS-DG',1059),(24,19,'DG-E','Lv','20:57:00','DG','Devil\'s Gulch','',1060),(24,19,'DG-E','Lv','21:28:00','SC','Silver City','',1061),(24,19,'DG-E','Ar','22:00:00','E','Empire','',1062),(24,19,'E-SG','Lv','22:20:00','E','Empire','',1063),(24,19,'E-SG','Ar','23:34:00','SG','Satyr\'s Glade','',1064),(25,NULL,NULL,'Lv','06:00:00','CC','Colorado City','CC-LC',1065),(25,NULL,NULL,'Lv','06:28:00','FR','Fall River','CC-LC',1066),(25,NULL,NULL,'Ar','07:07:00','LC','Lost Creek','CC-LC',1067),(25,20,'SG-E','Lv','02:30:00','SG','Satyr\'s Glade','',1068),(25,20,'SG-E','Ar','03:35:00','E','Empire','',1069),(25,20,'E-DG','Lv','03:40:00','E','Empire','',1070),(25,20,'E-DG','Lv','04:08:00','SC','Silver City','',1071),(25,20,'E-DG','Ar','04:36:00','DG','Devil\'s Gulch','',1072),(25,20,'DG-CC','Lv','04:46:00','DG','Devil\'s Gulch','',1073),(25,20,'DG-CC','Ar','05:38:00','CC','Colorado City','',1074),(26,NULL,NULL,'Lv','18:15:00','LC','Lost Creek','LC-CC',1075),(26,NULL,NULL,'Lv','18:50:00','FR','Fall River','LC-CC',1076),(26,NULL,NULL,'Ar','19:15:00','CC','Colorado City','LC-CC',1077),(26,19,'CC-DG','Lv','19:54:00','CC','Colorado City','',1078),(26,19,'CC-DG','Ar','20:52:00','DG','Devil\'s Gulch','',1079),(26,19,'DG-E','Lv','20:57:00','DG','Devil\'s Gulch','',1080),(26,19,'DG-E','Lv','21:28:00','SC','Silver City','',1081),(26,19,'DG-E','Ar','22:00:00','E','Empire','',1082),(26,19,'E-SG','Lv','22:20:00','E','Empire','',1083),(26,19,'E-SG','Ar','23:34:00','SG','Satyr\'s Glade','',1084),(27,NULL,NULL,'Lv','09:00:00','MS','Mystic Springs','MS-DG',1085),(27,NULL,NULL,'Lv','09:38:00','BB','Beaver Bend','MS-DG',1086),(27,NULL,NULL,'Lv','10:09:00','FG','Faun Glen','MS-DG',1087),(27,NULL,NULL,'Ar','10:38:00','DG','Devil\'s Gulch','MS-DG',1088),(27,NULL,NULL,'Lv','11:23:00','DG','Devil\'s Gulch','DG-E',1089),(27,NULL,NULL,'Lv','11:54:00','SC','Silver City','DG-E',1090),(27,NULL,NULL,'Lv','12:26:00','E','Empire','E-ES',1091),(27,NULL,NULL,'Ar','13:37:00','ES','Excelsior Springs','E-ES',1092),(28,NULL,NULL,'Lv','09:00:00','ES','Excelsior Springs','ES-E',1093),(28,NULL,NULL,'Lv','10:02:00','E','Empire','E-DG',1094),(28,NULL,NULL,'Lv','10:30:00','SC','Silver City','E-DG',1095),(28,NULL,NULL,'Ar','10:58:00','DG','Devil\'s Gulch','E-DG',1096),(28,NULL,NULL,'Lv','11:43:00','DG','Devil\'s Gulch','DG-MS',1097),(28,NULL,NULL,'Lv','12:16:00','FG','Faun Glen','DG-MS',1098),(28,NULL,NULL,'Lv','12:51:00','BB','Beaver Bend','DG-MS',1099),(28,NULL,NULL,'Ar','13:34:00','MS','Mystic Springs','DG-MS',1100);
/*!40000 ALTER TABLE `private_time_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `private_time_table_east_vw`
--

DROP TABLE IF EXISTS `private_time_table_east_vw`;
/*!50001 DROP VIEW IF EXISTS `private_time_table_east_vw`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `private_time_table_east_vw` (
  `locationCode` tinyint NOT NULL,
  `arlv` tinyint NOT NULL,
  `scheduledTime` tinyint NOT NULL,
  `locationName` tinyint NOT NULL,
  `milePost` tinyint NOT NULL,
  `services` tinyint NOT NULL,
  `trainNumber` tinyint NOT NULL,
  `connectingTrainNumber` tinyint NOT NULL,
  `trainName` tinyint NOT NULL,
  `westDays` tinyint NOT NULL,
  `allDays` tinyint NOT NULL,
  `eastDays` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `private_time_table_vw`
--

DROP TABLE IF EXISTS `private_time_table_vw`;
/*!50001 DROP VIEW IF EXISTS `private_time_table_vw`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `private_time_table_vw` (
  `trainNumber` tinyint NOT NULL,
  `trainName` tinyint NOT NULL,
  `connectingTrainNumber` tinyint NOT NULL,
  `arlv` tinyint NOT NULL,
  `scheduledTime` tinyint NOT NULL,
  `locationName` tinyint NOT NULL,
  `locationCode` tinyint NOT NULL,
  `milePost` tinyint NOT NULL,
  `services` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `private_time_table_west_vw`
--

DROP TABLE IF EXISTS `private_time_table_west_vw`;
/*!50001 DROP VIEW IF EXISTS `private_time_table_west_vw`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `private_time_table_west_vw` (
  `trainNumber` tinyint NOT NULL,
  `trainName` tinyint NOT NULL,
  `connectingTrainNumber` tinyint NOT NULL,
  `trainDays` tinyint NOT NULL,
  `scheduledTime` tinyint NOT NULL,
  `arlv` tinyint NOT NULL,
  `locationName` tinyint NOT NULL,
  `milePost` tinyint NOT NULL,
  `services` tinyint NOT NULL,
  `locationCode` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `route_segments`
--

DROP TABLE IF EXISTS `route_segments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `route_segments` (
  `segmentCode` varchar(20) NOT NULL,
  `segmentDirection` enum('W','E','N','S') NOT NULL DEFAULT 'W' COMMENT 'W,E,N,S',
  PRIMARY KEY (`segmentCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `route_segments`
--

LOCK TABLES `route_segments` WRITE;
/*!40000 ALTER TABLE `route_segments` DISABLE KEYS */;
INSERT INTO `route_segments` VALUES ('CC-DG','W'),('CC-FH','E'),('CC-LC','W'),('DG-CC','E'),('DG-E','W'),('DG-MS','W'),('E-DG','E'),('E-ES','W'),('E-SG','W'),('ES-E','E'),('FH-CC','W'),('LC-CC','E'),('MS-DG','E'),('SG-E','E');
/*!40000 ALTER TABLE `route_segments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sections`
--

DROP TABLE IF EXISTS `sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sections` (
  `sectionNumber` int(11) NOT NULL AUTO_INCREMENT,
  `sectionName` varchar(45) NOT NULL,
  `startLocationId` int(11) NOT NULL,
  `startLocationCode` varchar(5) DEFAULT NULL,
  `endLocationId` int(11) NOT NULL,
  `endLocationCode` varchar(5) DEFAULT NULL,
  `distance` float NOT NULL,
  `avgSpeedWest` float NOT NULL,
  `avgSpeedEast` float DEFAULT NULL,
  `avgTime` double DEFAULT NULL,
  PRIMARY KEY (`sectionNumber`),
  UNIQUE KEY `sectionNumber_UNIQUE` (`sectionNumber`),
  UNIQUE KEY `sectionName_UNIQUE` (`sectionName`),
  KEY `endLoc_fk_idx` (`endLocationId`),
  KEY `startLoc_idx` (`startLocationId`),
  KEY `endLoc_idx` (`endLocationId`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sections`
--

LOCK TABLES `sections` WRITE;
/*!40000 ALTER TABLE `sections` DISABLE KEYS */;
INSERT INTO `sections` VALUES (1,'FH-FE',1,'FH',2,'FE',15.72,26.8,29.3,NULL),(2,'FE-CC',2,'FE',4,'CC',26.13,26.5,29.1,NULL),(3,'CC-DG',4,'CC',5,'DG',20.89,21.5,24.1,NULL),(4,'DG-FG',5,'DG',9,'FG',11.13,20.2,22.8,NULL),(5,'FG-BB',9,'FG',3,'BB',10.8,18.3,20.9,NULL),(6,'BB-MS',3,'BB',11,'MS',13.3,18.6,21.2,NULL),(7,'DG-SC',5,'DG',13,'SC',10.2,19.5,22.1,NULL),(8,'SC-E',13,'SC',6,'E',9.91,18.5,21.1,NULL),(9,'E-ES',6,'E',7,'ES',21.31,18.1,20.7,NULL),(10,'E-SG',6,'E',10,'SG',22.5,18.3,20.9,NULL),(11,'CC-FR',4,'CC',8,'FR',10.3,22.4,25,NULL),(12,'FR-LC',8,'FR',12,'LC',14.72,22.5,25.1,NULL),(13,'DG-DG',5,'DG',5,'DG',0,22,24.6,NULL),(14,'FH-FH',1,'FH',1,'FH',0,21,23.6,NULL),(17,'CC-CC',4,'CC',4,'CC',0,22,24.6,NULL),(18,'LC-FR',12,'LC',8,'FR',14.72,23.5,26.1,NULL),(19,'FR-CC',8,'FR',4,'CC',10.03,23.2,25.8,NULL),(20,'LC-LC',12,'LC',12,'LC',0.1,1,1,NULL),(23,'MS-MS',11,'MS',11,'MS',0,1,1,NULL),(24,'FH-DG',1,'FH',5,'DG',62.73,24.6,28.5,NULL),(25,'DG-MS',5,'DG',7,'ES',41.42,21.3,25.4,NULL),(26,'SG-E',10,'SG',6,'E',22.5,18.7,20.3,NULL),(27,'SG-SG',10,'SG',10,'SG',0,1,1,NULL),(28,'E-E',6,'E',6,'E',0,1,1,NULL),(29,'ES-ES',7,'ES',7,'ES',0,1,1,NULL);
/*!40000 ALTER TABLE `sections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `segment_sections`
--

DROP TABLE IF EXISTS `segment_sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `segment_sections` (
  `segmentCode` varchar(20) NOT NULL DEFAULT '',
  `sectionCode` varchar(20) NOT NULL,
  `sectionOrder` int(11) NOT NULL,
  `segmentDirection` char(1) CHARACTER SET latin1 DEFAULT NULL,
  `segmentId` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`segmentId`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `segment_sections`
--

LOCK TABLES `segment_sections` WRITE;
/*!40000 ALTER TABLE `segment_sections` DISABLE KEYS */;
INSERT INTO `segment_sections` VALUES ('FH-CC','FH-FE',0,'W',1),('FH-CC','FE-CC',1,'W',2),('CC-LC','CC-FR',0,'W',3),('CC-LC','FR-LC',1,'W',4),('CC-DG','CC-DG',0,'W',5),('DG-MS','DG-FG',0,'W',6),('DG-MS','FG-BB',1,'W',7),('DG-MS','BB-MS',2,'W',8),('DG-E','DG-SC',0,'W',9),('DG-E','SC-E',1,'W',10),('E-ES','E-ES',0,'W',11),('E-SG','E-SG',0,'W',12),('LC-CC','FR-LC',0,'E',13),('LC-CC','CC-FR',1,'E',14),('ES-E','E-ES',0,'E',15),('E-DG','SC-E',0,'E',16),('E-DG','DG-SC',1,'E',17),('DG-CC','CC-DG',0,'E',18),('CC-FH','FE-CC',0,'E',19),('CC-FH','FH-FE',1,'E',20),('MS-DG','BB-MS',0,'E',21),('MS-DG','FG-BB',1,'E',22),('MS-DG','DG-FG',2,'E',23),('SG-E','E-SG',0,'E',24),('FH-DG','FH-DG',0,'W',25),('DG-FH','FH-DG',1,'E',30),('ES-DG','DG-MS',1,'E',31),('DGMSX','DG-MS',1,'W',32),('MSDGX','DG-MS',1,'E',33);
/*!40000 ALTER TABLE `segment_sections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services` (
  `serviceCode` varchar(5) NOT NULL,
  `serviceDescription` varchar(50) NOT NULL,
  `servicePrivate` bit(1) NOT NULL DEFAULT b'0',
  `longDescription` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`serviceCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES ('A','Ticket Agent','\0',NULL),('B','Checked Baggage','\0','Checked baggage is accepted for loading or unloaded for claim.'),('F','Flag Stop','\0','Trains only stop to load or unload passengers when signaled.'),('G','Glory','',NULL),('H','Hookers','',NULL),('L','Lockers','\0','Lockers are available for passengers to store personal items.'),('M','Box Lunch','\0','Box lunches are available for purchase.'),('S','Showers','','Showers are available in the men\'s rest room.'),('T','Telegraph','\0','A Western Union telegraph office is available to passengers in the station.'),('X','Express','\0','Railway Express Agency services are available for shipping parcels and light freight.');
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `services_legend_vw`
--

DROP TABLE IF EXISTS `services_legend_vw`;
/*!50001 DROP VIEW IF EXISTS `services_legend_vw`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `services_legend_vw` (
  `serviceCode` tinyint NOT NULL,
  `serviceDescription` tinyint NOT NULL,
  `longDescription` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `station_schedules`
--

DROP TABLE IF EXISTS `station_schedules`;
/*!50001 DROP VIEW IF EXISTS `station_schedules`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `station_schedules` (
  `station` tinyint NOT NULL,
  `trainNumber` tinyint NOT NULL,
  `trainName` tinyint NOT NULL,
  `arlv` tinyint NOT NULL,
  `scheduleTime` tinyint NOT NULL,
  `direction` tinyint NOT NULL,
  `trainDays` tinyint NOT NULL,
  `destination` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `station_services`
--

DROP TABLE IF EXISTS `station_services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `station_services` (
  `locationId` int(11) DEFAULT NULL,
  `locationCode` varchar(4) DEFAULT NULL,
  `serviceCode` varchar(4) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `ss_service_fk_idx` (`serviceCode`),
  KEY `ss_location_fk_idx` (`locationId`),
  CONSTRAINT `ss_location_fk` FOREIGN KEY (`locationId`) REFERENCES `locations` (`locationId`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `ss_service_fk` FOREIGN KEY (`serviceCode`) REFERENCES `services` (`serviceCode`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COMMENT='Cross-link between locations and services';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station_services`
--

LOCK TABLES `station_services` WRITE;
/*!40000 ALTER TABLE `station_services` DISABLE KEYS */;
INSERT INTO `station_services` VALUES (1,'FH','A',1),(1,'FH','B',2),(1,'FH','T',3),(2,'FE','T',4),(1,'FH','G',5),(4,'CC','A',6),(4,'CC','T',7),(4,'CC','B',8),(5,'DG','A',9),(5,'DG','B',10),(5,'DG','T',12),(5,'DG','G',14),(5,'DG','M',15),(5,'DG','X',16),(10,'SG','L',17),(10,'SG','T',18),(7,'ES','H',19);
/*!40000 ALTER TABLE `station_services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `metadata_item_id` int(11) DEFAULT NULL,
  `tag` varchar(255) DEFAULT NULL,
  `tag_type` int(11) DEFAULT NULL,
  `user_thumb_url` varchar(255) DEFAULT NULL,
  `user_art_url` varchar(255) DEFAULT NULL,
  `user_music_url` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `tag_value` int(11) DEFAULT NULL,
  `extra_data` varchar(255) DEFAULT NULL,
  `key` varchar(255) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `time_table_east_vw`
--

DROP TABLE IF EXISTS `time_table_east_vw`;
/*!50001 DROP VIEW IF EXISTS `time_table_east_vw`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `time_table_east_vw` (
  `locationCode` tinyint NOT NULL,
  `arlv` tinyint NOT NULL,
  `scheduledTime` tinyint NOT NULL,
  `locationName` tinyint NOT NULL,
  `milePost` tinyint NOT NULL,
  `services` tinyint NOT NULL,
  `trainNumber` tinyint NOT NULL,
  `connectingTrainNumber` tinyint NOT NULL,
  `trainName` tinyint NOT NULL,
  `westDays` tinyint NOT NULL,
  `allDays` tinyint NOT NULL,
  `eastDays` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `time_table_segments_vw`
--

DROP TABLE IF EXISTS `time_table_segments_vw`;
/*!50001 DROP VIEW IF EXISTS `time_table_segments_vw`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `time_table_segments_vw` (
  `trainNumber` tinyint NOT NULL,
  `trainName` tinyint NOT NULL,
  `connectingTrainNumber` tinyint NOT NULL,
  `arlv` tinyint NOT NULL,
  `scheduledTime` tinyint NOT NULL,
  `locationName` tinyint NOT NULL,
  `locationCode` tinyint NOT NULL,
  `milePost` tinyint NOT NULL,
  `services` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `time_table_west_vw`
--

DROP TABLE IF EXISTS `time_table_west_vw`;
/*!50001 DROP VIEW IF EXISTS `time_table_west_vw`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `time_table_west_vw` (
  `trainNumber` tinyint NOT NULL,
  `trainName` tinyint NOT NULL,
  `connectingTrainNumber` tinyint NOT NULL,
  `trainDays` tinyint NOT NULL,
  `scheduledTime` tinyint NOT NULL,
  `arlv` tinyint NOT NULL,
  `locationName` tinyint NOT NULL,
  `milePost` tinyint NOT NULL,
  `services` tinyint NOT NULL,
  `locationCode` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `train_days`
--

DROP TABLE IF EXISTS `train_days`;
/*!50001 DROP VIEW IF EXISTS `train_days`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `train_days` (
  `westTrain` tinyint NOT NULL,
  `westDays` tinyint NOT NULL,
  `allDays` tinyint NOT NULL,
  `eastDays` tinyint NOT NULL,
  `eastTrain` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `train_segments`
--

DROP TABLE IF EXISTS `train_segments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `train_segments` (
  `trainNumber` int(11) NOT NULL,
  `segmentCode` varchar(20) NOT NULL,
  `segmentOrder` int(11) NOT NULL,
  `segmentDelay` int(11) NOT NULL DEFAULT '0',
  `segmentStartTime` time DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `fk_ts_trainNum` (`trainNumber`),
  CONSTRAINT `fk_ts_trainNum` FOREIGN KEY (`trainNumber`) REFERENCES `trains` (`trainNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `train_segments`
--

LOCK TABLES `train_segments` WRITE;
/*!40000 ALTER TABLE `train_segments` DISABLE KEYS */;
INSERT INTO `train_segments` VALUES (3,'FH-CC',1,0,'08:00:00',1),(3,'CC-DG',2,15,NULL,2),(3,'DG-E',3,10,NULL,3),(19,'FH-CC',1,0,'18:00:00',4),(19,'CC-DG',2,20,NULL,5),(19,'DG-E',3,5,NULL,6),(19,'E-SG',4,20,NULL,7),(26,'LC-CC',1,0,'18:15:00',8),(3,'E-ES',4,5,NULL,10),(4,'ES-E',1,0,'13:30:00',11),(4,'E-DG',2,5,NULL,12),(4,'DG-CC',3,20,NULL,13),(4,'CC-FH',4,10,NULL,14),(5,'CC-LC',1,0,'10:15:00',15),(6,'LC-CC',1,0,'14:00:00',16),(7,'DG-MS',1,0,'11:15:00',17),(8,'MS-DG',1,0,'13:30:00',18),(9,'DG-E',1,0,'11:25:00',19),(9,'E-SG',2,10,NULL,20),(10,'SG-E',1,0,'13:30:00',21),(10,'E-DG',2,10,NULL,22),(21,'E-ES',1,0,'03:50:00',23),(22,'ES-E',1,0,'21:00:00',24),(20,'SG-E',1,0,'02:30:00',25),(20,'E-DG',2,5,NULL,26),(20,'DG-CC',3,10,NULL,27),(20,'CC-FH',4,10,NULL,28),(23,'DG-MS',1,0,'04:50:00',29),(24,'MS-DG',1,0,'19:00:00',30),(25,'CC-LC',1,0,'06:00:00',31),(15,'DG-E',1,0,'15:00:00',32),(15,'E-ES',2,5,NULL,33),(16,'ES-E',1,0,'09:00:00',34),(16,'E-DG',2,5,NULL,35),(17,'DG-E',1,0,'15:15:00',36),(17,'E-SG',2,0,NULL,37),(18,'SG-E',1,0,'09:00:00',38),(18,'E-DG',2,0,NULL,39),(11,'FH-DG',1,0,'00:00:00',40),(11,'DGMSX',2,10,NULL,41),(12,'MSDGX',1,0,'05:00:00',42),(12,'DG-FH',2,10,NULL,43),(27,'MS-DG',1,0,'09:00:00',44),(27,'DG-E',2,45,NULL,45),(27,'E-ES',3,0,NULL,46),(28,'ES-E',1,0,'09:00:00',47),(28,'E-DG',2,0,NULL,48),(28,'DG-MS',3,45,NULL,49);
/*!40000 ALTER TABLE `train_segments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `train_segments_vw`
--

DROP TABLE IF EXISTS `train_segments_vw`;
/*!50001 DROP VIEW IF EXISTS `train_segments_vw`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `train_segments_vw` (
  `trainNumber` tinyint NOT NULL,
  `segmentDirection` tinyint NOT NULL,
  `segmentStartTime` tinyint NOT NULL,
  `segmentCode` tinyint NOT NULL,
  `segmentDelay` tinyint NOT NULL,
  `sectionCode` tinyint NOT NULL,
  `distance` tinyint NOT NULL,
  `startLocation` tinyint NOT NULL,
  `startLocationCode` tinyint NOT NULL,
  `endLocation` tinyint NOT NULL,
  `endLocationCode` tinyint NOT NULL,
  `avgSpeed` tinyint NOT NULL,
  `segmentOrder` tinyint NOT NULL,
  `sectionOrder` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `trains`
--

DROP TABLE IF EXISTS `trains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trains` (
  `trainNumber` int(11) NOT NULL,
  `trainName` varchar(45) NOT NULL,
  `trainType` enum('P','F','M') DEFAULT 'P' COMMENT 'Passenger, Freight, Mixed',
  `trainDays` varchar(45) DEFAULT NULL,
  `trainDirection` enum('East','West','North','South') NOT NULL,
  `trainStartTime` time DEFAULT NULL,
  `connectingTrain` int(11) DEFAULT NULL COMMENT 'Train continuing on',
  `reverseDirectionTrainNum` int(11) DEFAULT NULL,
  `privateName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`trainNumber`),
  UNIQUE KEY `trainNumber_UNIQUE` (`trainNumber`),
  KEY `t_connectTrain_fk_idx` (`trainNumber`,`connectingTrain`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trains`
--

LOCK TABLES `trains` WRITE;
/*!40000 ALTER TABLE `trains` DISABLE KEYS */;
INSERT INTO `trains` VALUES (3,'Mountaineer','P','Daily','West','08:00:00',NULL,4,NULL),(4,'Mountaineer','P','Daily','East','13:30:00',NULL,3,NULL),(5,'River Valley Flyer','P','Mon - Wed - Fri','West','09:56:00',3,6,NULL),(6,'River Valley Flyer','P','Fri - Sat - Sun','East','14:30:00',4,5,NULL),(7,'Weekend Escape','P','Fri - Sat - Sun','West','11:07:00',3,8,NULL),(8,'Weekend Escape','P','Fri - Sat - Sun','East','13:30:00',4,7,NULL),(9,'Mountain Scout','P','Friday','West','11:07:00',3,10,'Bukkake Scout'),(10,'Mountain Scout','P','Sunday','East','13:30:00',NULL,9,'Bukkake Scout'),(11,'Midnight Express ','P','Tue - Thu - Sun','West','00:00:00',NULL,12,NULL),(12,'Midnight Express','P','Tue - Thu - Sun','East','05:00:00',NULL,11,NULL),(15,'Mine Excursion','P','Tue - Thu','West','15:00:00',NULL,16,'Corn Hole Excursion'),(16,'Mine Excursion','P','Tue - Thu','East','09:00:00',NULL,15,'Corn Hole Excursion'),(17,'Mountain Excursion','P','Sunday','West','15:00:00',NULL,18,'Nudist Excursion'),(18,'Mountain Excursion','P','Saturday','East','09:00:00',NULL,17,'Nudist Excursion'),(19,'Moonlight Adventurer','P','Friday','West','18:00:00',NULL,20,'Satyr Moon Traveller'),(20,'Moonlight Adventurer','P','Saturday','East','02:30:00',NULL,19,'Satyr Moon Traveller'),(21,'Full Moon Special','P','Friday','West','21:15:00',19,22,'Ganymede Flyer'),(22,'Full Moon Special','P','Saturday','East','02:30:00',20,21,'Ganymede Flyer'),(23,'Night Owl Flyer','P','Saturday','West','04:45:00',NULL,24,'Phallus Connector'),(24,'Night Owl Flyer','P','Friday','East','19:15:00',NULL,23,'Phallus Connector'),(25,'Fall River Special','P','Saturday','West','05:40:00',NULL,26,'Golden Shower Express'),(26,'Fall River Special','P','Friday','East','18:15:00',NULL,25,'Golden Shower Express'),(27,'Hot Spring Exchange','P','Mon - Wed - Fri','East','09:00:00',NULL,28,NULL),(28,'Hot Spring Exchange','P','Mon - Wed - Fri','West','09:00:00',NULL,27,NULL);
/*!40000 ALTER TABLE `trains` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'foggyhollow'
--

--
-- Dumping routines for database 'foggyhollow'
--
/*!50003 DROP FUNCTION IF EXISTS `GETLOCATIONNAME` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`foggyhollow`@`%` FUNCTION `GETLOCATIONNAME`(locationCodeIn VARCHAR(5)) RETURNS varchar(40) CHARSET utf8
BEGIN
	declare accessMode Varchar(45);
    declare result Varchar(100);
    
    set result = "";
    
	SELECT 
    propValue
INTO accessMode FROM
    application_properties
WHERE
    propName = 'accessMode';
    
    if (accessMode = "private") then
		select coalesce(privateLocationName, locationName) as 'Location Name' into result from locations where locationCode = locationCodeIn;    
    else
		select locationName as 'Location Name' into result from locations where locationCode = locationCodeIn;
    end if;
RETURN result;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `GETSERVICES` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`foggyhollow`@`%` FUNCTION `GETSERVICES`(locationCodeIn VARCHAR(5)) RETURNS varchar(100) CHARSET utf8
BEGIN

 DECLARE accessMode Varchar(45);

    DECLARE result Varchar(100);



    SET result = "";



 SELECT

    propValue

INTO accessMode FROM

    application_properties

WHERE

    propName = 'accessMode';



    IF (accessMode = "private") THEN

           (SELECT privateServices INTO result FROM locations WHERE locationCode = locationCodeIn);

    /*

        (SELECT

                GROUP_CONCAT(`s`.`serviceCode`

                        SEPARATOR '') AS 'Services' INTO result

            FROM

                (`services` `s`

                JOIN `station_services` `ss`)

            WHERE

                ((`s`.`serviceCode` = `ss`.`serviceCode`)

                    AND (`ss`.`locationCode` = locationCodeIn))

            GROUP BY NULL

            ORDER BY s.serviceCode);

    */

    ELSE

       (SELECT  services INTO result FROM locations WHERE locationCode = locationCodeIn);

    END IF;



  RETURN RESULT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `GETTRAINNAME` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`foggyhollow`@`%` FUNCTION `GETTRAINNAME`(trainNumIn INT) RETURNS varchar(100) CHARSET utf8
BEGIN
	declare accessMode Varchar(45);
    declare result Varchar(100);
    
    set result = "";
    
	SELECT 
    propValue
INTO accessMode FROM
    application_properties
WHERE
    propName = 'accessMode';
    
    if (accessMode = "private") then
        SELECT COALESCE(privateName, trainName) as 'Train Name' into result  FROM trains where trainNumber = trainNumIn;
	else 
        SELECT trainName as 'Train Name' into result  FROM trains where trainNumber = trainNumIn;   
	end if;
    
    RETURN RESULT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `get_location_name` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`foggyhollow`@`%` FUNCTION `get_location_name`(locationCodeIn VARCHAR(5)) RETURNS varchar(40) CHARSET utf8
BEGIN

 DECLARE accessMode Varchar(45);

  DECLARE result Varchar(100);



  SET result = "";



 SELECT

    propValue

INTO accessMode FROM

    application_properties

WHERE

    propName = 'accessMode';



    IF (accessMode = "private") THEN

  SELECT coalesce(privateLocationName, locationName) AS 'Location Name' INTO result FROM locations WHERE locationCode = locationCodeIn;

    ELSE

  SELECT locationName AS 'Location Name' INTO result FROM locations WHERE locationCode = locationCodeIn;

    END IF;

RETURN result;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `BuildAllTrains` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`foggyhollow`@`%` PROCEDURE `BuildAllTrains`()
BEGIN



	declare loopDone int;

    declare trainNum int;

    

	DECLARE trainData CURSOR FOR  SELECT trainNumber

	FROM trains

	Order by trainNumber;



	DECLARE CONTINUE HANDLER FOR NOT FOUND SET loopDone = 1;  

  

	OPEN trainData;

	SET loopDone = 0;



	REPEAT

		FETCH trainData INTO trainNum;

		IF not loopDone then 

			call BuildConnectingTrains(trainNum);

		end if;



	UNTIL loopDone END REPEAT;



	CLOSE trainData;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `BuildConnectingTrainFromSegments` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`foggyhollow`@`%` PROCEDURE `BuildConnectingTrainFromSegments`(trainNumberIn INT)
BEGIN

  DECLARE isDone           int;

  DECLARE isDone2 int;



  DECLARE connTrain     int;

  DECLARE connTrainSegment VARCHAR(5);

  DECLARE connLocation     VARCHAR(45);

  DECLARE connTime         TIME;

  DECLARE connarlv         VARCHAR(2);

  DECLARE connLocCode      VARCHAR(5);

  DECLARE connectCount INT;





  DECLARE curs CURSOR FOR  SELECT connectingTrainNumber, connectingTrainSegment from connecting_train_segments

  where trainNumber = trainNumberIn order by connectingOrder;



  DECLARE CONTINUE HANDLER FOR NOT FOUND SET isDone = 1;

  delete from connecting_time_table where trainNumber = trainNumberIn;



  CALL BuildTrainFromSegments(trainNumberIn);



  OPEN curs;



  SET isDone    = 0;

  set isDone2 = 0;

  set connectCount = 0;





  REPEAT

    FETCH curs INTO connTrain, connTrainSegment;



    IF NOT isDone THEN



      BEGIN

        DECLARE curs2 CURSOR FOR select scheduledTime, arlv, locationName, locationCode from connecting_time_table where trainNumber = connTrain and segmentCode = connTrainSegment order by scheduledTime;

        DECLARE CONTINUE HANDLER FOR NOT FOUND SET isDone2 = 1;

          OPEN curs2;

        REPEAT

          FETCH curs2 INTO connTime, connarlv, connLocation, connLocCode;



          IF NOT isDone2 THEN



/*            if (connectCount > 0) then */

              insert into connecting_time_table (trainNumber, segmentCode, connectingTrainNumber, connectingSegment, scheduledTime, arlv, locationName, locationCode)

              values (trainNumberIn, '', connTrain, connTrainSegment, connTime, connarlv, connLocation, connLocCode);

/*           end if;*/

            set connectCount = connectCount + 1;

          end if;

        UNTIL isDone2

        END REPEAT;



        CLOSE curs2; 

        set isDone2 = 0;

      END;

     

    end if;



  UNTIL isDone

  END REPEAT;



  CLOSE curs;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `BuildConnectingTrains` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`foggyhollow`@`%` PROCEDURE `BuildConnectingTrains`(trainNumberIn INT)
BEGIN

  DECLARE isDone           int;

  DECLARE isDone2 int;



  DECLARE connTrain     int;

  DECLARE connTrainSegment VARCHAR(5);

  DECLARE connLocation     VARCHAR(45);

  DECLARE connTime         TIME;

  DECLARE connarlv         VARCHAR(2);

  DECLARE connLocCode      VARCHAR(5);

  DECLARE connectCount INT;

  declare accessMode VARCHAR(45);



  DECLARE curs CURSOR FOR  SELECT connectingTrainNumber, connectingTrainSegment from connecting_train_segments

  where trainNumber = trainNumberIn order by connectingOrder;



  DECLARE CONTINUE HANDLER FOR NOT FOUND SET isDone = 1;

  

  SELECT propValue

  INTO   accessMode

  FROM   application_properties

  WHERE  propName = 'accessMode';

  

  

  IF (accessMode = 'private')

  THEN

    DELETE FROM private_time_table

    WHERE       trainNumber = trainNumberIn;

  ELSE

    DELETE FROM connecting_time_table

    WHERE       trainNumber = trainNumberIn;

  END IF;



  CALL BuildTrain(trainNumberIn);



  OPEN curs;



  SET isDone    = 0;

  set isDone2 = 0;

  set connectCount = 0;





  REPEAT

    FETCH curs INTO connTrain, connTrainSegment;



    IF NOT isDone THEN



      BEGIN

        DECLARE curs2 CURSOR FOR select scheduledTime, arlv, locationName, locationCode from connecting_time_table where trainNumber = connTrain and segmentCode = connTrainSegment order by scheduledTime;

        DECLARE CONTINUE HANDLER FOR NOT FOUND SET isDone2 = 1;

          OPEN curs2;

        REPEAT

          FETCH curs2 INTO connTime, connarlv, connLocation, connLocCode;



          IF NOT isDone2 THEN



            if (accessMode = 'private') then

              insert into private_time_table (trainNumber, segmentCode, connectingTrainNumber, connectingSegment, scheduledTime, arlv, locationName, locationCode)

              values (trainNumberIn, '', connTrain, connTrainSegment, connTime, connarlv, connLocation, connLocCode);            

            else

              insert into connecting_time_table (trainNumber, segmentCode, connectingTrainNumber, connectingSegment, scheduledTime, arlv, locationName, locationCode)

              values (trainNumberIn, '', connTrain, connTrainSegment, connTime, connarlv, connLocation, connLocCode);

            end if;

            set connectCount = connectCount + 1;

          end if;

        UNTIL isDone2

        END REPEAT;



        CLOSE curs2; 

        set isDone2 = 0;

      END;

     

    end if;



  UNTIL isDone

  END REPEAT;



  CLOSE curs;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `BuildTrain` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`foggyhollow`@`%` PROCEDURE `BuildTrain`(trainNumberIn INT)
BEGIN

  DECLARE isDone  INT;

  DECLARE loopCount  INT;

  DECLARE loc VARCHAR(45);



  DECLARE startLoc VARCHAR(45);

  DECLARE endLoc VARCHAR(45);

  DECLARE stTime TIME;

  DECLARE segCode Varchar(5);

  DECLARE secCode varchar(5);

  DECLARE dist FLOAT;

  DECLARE speed FLOAT;

  DECLARE trNum INT;

  DECLARE segDelay FLOAT;

  DECLARE prevLoc VARCHAR(45);

  DECLARE prevTime TIME;

  DECLARE prevDist FLOAT;

  DECLARE prevSpeed FLOAT;

  DECLARE startLocCode VARCHAR(5);

  DECLARE endLocCode VARCHAR(5);

  DECLARE prevLocCode VARCHAR(5);

  DECLARE prevSegCode VARCHAR(5);



  DECLARE schedTime TIME;





  DECLARE accessMode VARCHAR(10);

  DECLARE privateAccess TinyInt;







  DECLARE curs CURSOR FOR  SELECT trainNumber, segmentStartTime, segmentCode, segmentDelay,sectionCode, distance,

  startLocation, startLocationCode, endLocation,  endLocationCode, avgSpeed

  FROM train_segments_vw

  WHERE trainNumber = trainNumberIn

  ORDER BY segmentOrder, sectionOrder;



  DECLARE CONTINUE HANDLER FOR NOT FOUND SET isDone = 1;



  SELECT propValue

  INTO   accessMode

  FROM   application_properties

  WHERE  propName = 'accessMode';



  SET privateAccess = accessMode = 'private';



  OPEN curs;



  SET isDone        = 0;

  SET loopCount     = 1;



  IF (accessMode = 'private')

  THEN

    DELETE FROM private_time_table

    WHERE       trainNumber = trainNumberIn;

  ELSE

    DELETE FROM connecting_time_table

    WHERE       trainNumber = trainNumberIn;

  END IF;



  REPEAT

    FETCH curs

      INTO trNum, stTime, segCode, segDelay, secCode, dist, startLoc, startLocCode, endLoc, endLocCode,

           speed;



    IF NOT isDone

    THEN

      SET schedTime   = stTime;



      IF (loopCount = 1)

      THEN

        IF (accessMode = 'private')

        THEN

          INSERT INTO private_time_table(trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

          VALUES      (trNum, segCode, schedTime, 'Lv', startloc, startLocCode);

        ELSE

          INSERT INTO connecting_time_table(trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

          VALUES      (trNum, segCode, schedTime, 'Lv', startloc, startLocCode);

        END IF;

      ELSE

        SET schedTime = DATE_ADD(prevTime, INTERVAL ((prevDist / prevSpeed) * 60) MINUTE);



        IF (segDelay = 0)

        THEN

          IF (accessMode = 'private')

          THEN

            INSERT INTO private_time_table(trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

            VALUES      (trNum, segCode, schedTime, 'Lv', prevLoc, prevLocCode);

          ELSE

            INSERT INTO connecting_time_table(trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

            VALUES      (trNum, segCode, schedTime, 'Lv', prevLoc, prevLocCode);

          END IF;

        ELSE

          IF (accessMode = 'private')

          THEN

            INSERT INTO private_time_table(trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

            VALUES      (trNum, prevSegCode, schedTime, 'Ar', prevLoc, prevLocCode);

          ELSE

            INSERT INTO connecting_time_table(trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

            VALUES      (trNum, prevSegCode, schedTime, 'Ar', prevLoc, prevLocCode);

          END IF;



          SET schedTime = DATE_ADD(schedTime, INTERVAL segDelay MINUTE);



          IF (accessMode = 'private')

          THEN

            INSERT INTO private_time_table(trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

            VALUES      (trNum, segCode, schedTime, 'Lv', prevLoc, prevLocCode);

          ELSE

            INSERT INTO connecting_time_table(trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

            VALUES      (trNum, segCode, schedTime, 'Lv', prevLoc, prevLocCode);

          END IF;

        END IF;

      END IF;



      SET prevLoc     = endLoc;

      SET prevLocCode = endLocCode;

      SET prevTime    = schedTime;

      SET prevSpeed   = speed;

      SET prevDist    = dist;

      SET prevSegCode = segCode;



      SET loopCount   = loopCount + 1;

    END IF;

  UNTIL isDone

  END REPEAT;



  SET schedTime     = DATE_ADD(schedTime, INTERVAL ((dist / speed) * 60) MINUTE);



  IF (accessMode = 'private')

  THEN

    INSERT INTO private_time_table(trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

    VALUES      (trNum, segCode, schedTime, 'Ar', prevLoc, prevLocCode);

  ELSE

    INSERT INTO connecting_time_table(trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

    VALUES      (trNum, segCode, schedTime, 'Ar', prevLoc, prevLocCode);

  END IF;



  CLOSE curs;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `BuildTrainFromSegments` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`foggyhollow`@`%` PROCEDURE `BuildTrainFromSegments`(trainNumberIn INT)
BEGIN

  DECLARE isDone  INT;

  DECLARE loopCount  INT;

  DECLARE loc VARCHAR(45);

  DECLARE startLoc VARCHAR(45);

  DECLARE endLoc VARCHAR(45);

  DECLARE stTime TIME;

  DECLARE segCode Varchar(5);

  DECLARE secCode varchar(5);

  DECLARE dist FLOAT;

  DECLARE speed FLOAT;

  DECLARE trNum INT;

  DECLARE segDelay FLOAT;

  DECLARE prevLoc VARCHAR(45);

  DECLARE prevTime TIME;

  DECLARE prevDist FLOAT;

  DECLARE prevSpeed FLOAT;

  DECLARE startLocCode VARCHAR(5);

  DECLARE endLocCode VARCHAR(5);

  DECLARE prevLocCode VARCHAR(5);

  DECLARE prevSegCode VARCHAR(5);



  DECLARE schedTime TIME;



  DECLARE curs CURSOR FOR  SELECT trainNumber, segmentStartTime, segmentCode, segmentDelay,sectionCode, distance,

  startLocation, startLocationCode, endLocation,  endLocationCode, avgSpeed

  FROM train_segments_vw

  WHERE trainNumber = trainNumberIn

  ORDER BY segmentOrder, sectionOrder;



  DECLARE CONTINUE HANDLER FOR NOT FOUND SET isDone = 1;



  DROP TEMPORARY TABLE IF EXISTS tblResults;



  CREATE TEMPORARY TABLE IF NOT EXISTS tblResults(

    trainNumber INT, scheduledTime TIME, arLv VARCHAR(2), locationName VARCHAR(45));



  OPEN curs;



  SET isDone    = 0;

  SET loopCount = 1;



  delete from connecting_time_table where trainNumber = trainNumberIn;

  REPEAT

    FETCH curs INTO trNum, stTime, segCode, segDelay, secCode, dist, startLoc, startLocCode, endLoc, endLocCode, speed;



    IF NOT isDone

    THEN

      SET schedTime = stTime;



      IF (loopCount = 1)

      THEN

        INSERT INTO tblResults

        VALUES      (trNum, schedTime, 'Lv', startloc);

        

        INSERT INTO connecting_time_table (trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

        VALUES      (trNum, segCode, schedTime, 'Lv', startloc, startLocCode);        

      ELSE

        SET schedTime = DATE_ADD(prevTime, INTERVAL ((prevDist / prevSpeed) * 60) MINUTE);



        IF (segDelay = 0)

        THEN

          INSERT INTO tblResults

          VALUES      (trNum, schedTime, 'Lv', prevLoc);

          

          INSERT INTO connecting_time_table (trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

          VALUES      (trNum, segCode, schedTime, 'Lv', prevLoc, prevLocCode);

        ELSE

          INSERT INTO tblResults

          VALUES      (trNum, schedTime, 'Ar', prevLoc);



          INSERT INTO connecting_time_table (trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)

          VALUES      (trNum, prevSegCode, schedTime, 'Ar', prevLoc, prevLocCode);          

          

          SET schedTime = DATE_ADD(schedTime, INTERVAL segDelay MINUTE);



          INSERT INTO tblResults

          VALUES      (trNum, schedTime, 'Lv', prevLoc);

          

          INSERT INTO connecting_time_table (trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)  

          VALUES      (trNum, segCode, schedTime, 'Lv', prevLoc, prevLocCode);          

        END IF;

      END IF;



      SET prevLoc   = endLoc;

      SET prevLocCode = endLocCode;

      SET prevTime  = schedTime;

      SET prevSpeed = speed;

      SET prevDist  = dist;

      SET prevSegCode = segCode;



      SET loopCount = loopCount + 1;

    END IF;

  UNTIL isDone

  END REPEAT;



  SET schedTime = DATE_ADD(schedTime, INTERVAL ((dist / speed) * 60) MINUTE);



  INSERT INTO tblResults

  VALUES      (trNum, schedTime, 'Ar', prevLoc);

  

  INSERT INTO connecting_time_table (trainNumber, segmentCode, scheduledTime, arlv, locationName, locationCode)   

  VALUES      (trNum, segCode, schedTime, 'Ar', prevLoc, prevLocCode);

  

  CLOSE curs;



  SELECT * FROM tblResults;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `stationTrainBoard` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`foggyhollow`@`%` PROCEDURE `stationTrainBoard`(stationName varchar(45), trainDay varchar(20))
BEGIN

	select * from station_schedules where station = stationName and (trainDays like '%trainDay%' or trainDays = "Daily")

order by str_to_date(scheduletime, '%l:%i %p') asc;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Current Database: `foggyhollow`
--

USE `foggyhollow`;

--
-- Final view structure for view `private_time_table_east_vw`
--

/*!50001 DROP TABLE IF EXISTS `private_time_table_east_vw`*/;
/*!50001 DROP VIEW IF EXISTS `private_time_table_east_vw`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`foggyhollow`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `private_time_table_east_vw` AS select `tt`.`locationCode` AS `locationCode`,`tt`.`arlv` AS `arlv`,time_format(`tt`.`scheduledTime`,'%h:%i %p') AS `scheduledTime`,`GETLOCATIONNAME`(`tt`.`locationCode`) AS `locationName`,format(`l`.`milePost`,1) AS `milePost`,`GETSERVICES`(`tt`.`locationCode`) AS `services`,`tt`.`trainNumber` AS `trainNumber`,`tt`.`connectingTrainNumber` AS `connectingTrainNumber`,`GETTRAINNAME`(coalesce(`tt`.`connectingTrainNumber`,`tt`.`trainNumber`)) AS `trainName`,`td`.`westDays` AS `westDays`,`td`.`allDays` AS `allDays`,`td`.`eastDays` AS `eastDays` from ((`private_time_table` `tt` join `locations` `l`) join `train_days` `td`) where ((`tt`.`locationCode` = `l`.`locationCode`) and (not((`tt`.`trainNumber` % 2))) and (`tt`.`trainNumber` = `td`.`eastTrain`)) order by `tt`.`trainNumber`,`tt`.`scheduledTime` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `private_time_table_vw`
--

/*!50001 DROP TABLE IF EXISTS `private_time_table_vw`*/;
/*!50001 DROP VIEW IF EXISTS `private_time_table_vw`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`foggyhollow`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `private_time_table_vw` AS select `private_time_table`.`trainNumber` AS `trainNumber`,`GetTrainName`(`private_time_table`.`trainNumber`) AS `trainName`,`private_time_table`.`connectingTrainNumber` AS `connectingTrainNumber`,`private_time_table`.`arlv` AS `arlv`,time_format(`private_time_table`.`scheduledTime`,'%h:%i %p') AS `scheduledTime`,`GetLocationName`(`private_time_table`.`locationCode`) AS `locationName`,`private_time_table`.`locationCode` AS `locationCode`,format(`locations`.`milePost`,1) AS `milePost`,`GetServices`(`private_time_table`.`locationCode`) AS `services` from (`private_time_table` join `locations`) where (`private_time_table`.`locationCode` = `locations`.`locationCode`) order by `private_time_table`.`trainNumber`,`private_time_table`.`scheduledTime` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `private_time_table_west_vw`
--

/*!50001 DROP TABLE IF EXISTS `private_time_table_west_vw`*/;
/*!50001 DROP VIEW IF EXISTS `private_time_table_west_vw`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`foggyhollow`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `private_time_table_west_vw` AS select `tt`.`trainNumber` AS `trainNumber`,`GETTRAINNAME`(coalesce(`tt`.`connectingTrainNumber`,`tt`.`trainNumber`)) AS `trainName`,`tt`.`connectingTrainNumber` AS `connectingTrainNumber`,`t`.`trainDays` AS `trainDays`,time_format(`tt`.`scheduledTime`,'%h:%i %p') AS `scheduledTime`,`tt`.`arlv` AS `arlv`,`GETLOCATIONNAME`(`tt`.`locationCode`) AS `locationName`,format(`l`.`milePost`,1) AS `milePost`,`GETSERVICES`(`tt`.`locationCode`) AS `services`,`tt`.`locationCode` AS `locationCode` from ((`private_time_table` `tt` join `locations` `l`) join `trains` `t`) where ((`tt`.`trainNumber` = `t`.`trainNumber`) and (`tt`.`locationCode` = `l`.`locationCode`) and (`tt`.`trainNumber` % 2)) order by `tt`.`trainNumber`,`tt`.`scheduledTime` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `services_legend_vw`
--

/*!50001 DROP TABLE IF EXISTS `services_legend_vw`*/;
/*!50001 DROP VIEW IF EXISTS `services_legend_vw`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`foggyhollow`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `services_legend_vw` AS select `services`.`serviceCode` AS `serviceCode`,`services`.`serviceDescription` AS `serviceDescription`,`services`.`longDescription` AS `longDescription` from `services` where ((`services`.`servicePrivate` = (select (`application_properties`.`propValue` = 'private') from `application_properties` where (`application_properties`.`propName` = 'accessMode'))) or (((`services`.`servicePrivate` = 1) or (`services`.`servicePrivate` <> 1)) and (select (`application_properties`.`propValue` = 'private') from `application_properties` where (`application_properties`.`propName` = 'accessMode')))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `station_schedules`
--

/*!50001 DROP TABLE IF EXISTS `station_schedules`*/;
/*!50001 DROP VIEW IF EXISTS `station_schedules`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`foggyhollow`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `station_schedules` AS select `tt`.`locationName` AS `station`,`tt`.`trainNumber` AS `trainNumber`,`tt`.`trainName` AS `trainName`,`tt`.`arlv` AS `arlv`,`tt`.`scheduledTime` AS `scheduleTime`,`t`.`trainDirection` AS `direction`,`t`.`trainDays` AS `trainDays`,(select `tt1`.`locationName` from `time_table_segments_vw` `tt1` where (`tt1`.`trainNumber` = `tt`.`trainNumber`) order by str_to_date(`tt1`.`scheduledTime`,'%h:%i %p') desc limit 1) AS `destination` from (`time_table_segments_vw` `tt` join `trains` `t`) where ((`tt`.`trainNumber` = `t`.`trainNumber`) and isnull(`tt`.`connectingTrainNumber`)) order by `tt`.`locationName`,str_to_date(`tt`.`scheduledTime`,'%h:%i %p') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `time_table_east_vw`
--

/*!50001 DROP TABLE IF EXISTS `time_table_east_vw`*/;
/*!50001 DROP VIEW IF EXISTS `time_table_east_vw`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`foggyhollow`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `time_table_east_vw` AS select `tt`.`locationCode` AS `locationCode`,`tt`.`arlv` AS `arlv`,time_format(`tt`.`scheduledTime`,'%h:%i %p') AS `scheduledTime`,`GETLOCATIONNAME`(`tt`.`locationCode`) AS `locationName`,format(`l`.`milePost`,1) AS `milePost`,`GETSERVICES`(`tt`.`locationCode`) AS `services`,`tt`.`trainNumber` AS `trainNumber`,`tt`.`connectingTrainNumber` AS `connectingTrainNumber`,`GETTRAINNAME`(coalesce(`tt`.`connectingTrainNumber`,`tt`.`trainNumber`)) AS `trainName`,`td`.`westDays` AS `westDays`,`td`.`allDays` AS `allDays`,`td`.`eastDays` AS `eastDays` from (((`connecting_time_table` `tt` join `locations` `l`) join `trains` `t`) join `train_days` `td`) where ((`tt`.`locationCode` = `l`.`locationCode`) and (`tt`.`trainNumber` = `t`.`trainNumber`) and (`t`.`trainDirection` = 'East') and (`tt`.`trainNumber` = `td`.`eastTrain`)) order by `tt`.`trainNumber`,`tt`.`scheduledTime` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `time_table_segments_vw`
--

/*!50001 DROP TABLE IF EXISTS `time_table_segments_vw`*/;
/*!50001 DROP VIEW IF EXISTS `time_table_segments_vw`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`foggyhollow`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `time_table_segments_vw` AS select `connecting_time_table`.`trainNumber` AS `trainNumber`,`GetTrainName`(`connecting_time_table`.`trainNumber`) AS `trainName`,`connecting_time_table`.`connectingTrainNumber` AS `connectingTrainNumber`,`connecting_time_table`.`arlv` AS `arlv`,time_format(`connecting_time_table`.`scheduledTime`,'%h:%i %p') AS `scheduledTime`,`GetLocationName`(`connecting_time_table`.`locationCode`) AS `locationName`,`connecting_time_table`.`locationCode` AS `locationCode`,format(`locations`.`milePost`,1) AS `milePost`,`GetServices`(`connecting_time_table`.`locationCode`) AS `services` from (`connecting_time_table` join `locations`) where (`connecting_time_table`.`locationCode` = `locations`.`locationCode`) order by `connecting_time_table`.`trainNumber`,`connecting_time_table`.`scheduledTime` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `time_table_west_vw`
--

/*!50001 DROP TABLE IF EXISTS `time_table_west_vw`*/;
/*!50001 DROP VIEW IF EXISTS `time_table_west_vw`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`foggyhollow`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `time_table_west_vw` AS select `tt`.`trainNumber` AS `trainNumber`,`GetTrainName`(coalesce(`tt`.`connectingTrainNumber`,`tt`.`trainNumber`)) AS `trainName`,`tt`.`connectingTrainNumber` AS `connectingTrainNumber`,`t`.`trainDays` AS `trainDays`,time_format(`tt`.`scheduledTime`,'%h:%i %p') AS `scheduledTime`,`tt`.`arlv` AS `arlv`,`GetLocationName`(`tt`.`locationCode`) AS `locationName`,format(`l`.`milePost`,1) AS `milePost`,`GetServices`(`tt`.`locationCode`) AS `services`,`tt`.`locationCode` AS `locationCode` from ((`connecting_time_table` `tt` join `locations` `l`) join `trains` `t`) where ((`tt`.`trainNumber` = `t`.`trainNumber`) and (`tt`.`locationCode` = `l`.`locationCode`) and (`t`.`trainDirection` = 'West')) order by `tt`.`trainNumber`,`tt`.`scheduledTime` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `train_days`
--

/*!50001 DROP TABLE IF EXISTS `train_days`*/;
/*!50001 DROP VIEW IF EXISTS `train_days`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`foggyhollow`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `train_days` AS select `t`.`trainNumber` AS `westTrain`,(case when ((`t`.`trainDirection` = 'West') and (`t`.`trainDays` <> `rt`.`trainDays`)) then `t`.`trainDays` else '' end) AS `westDays`,(case when (`t`.`trainDays` = `rt`.`trainDays`) then `t`.`trainDays` else '' end) AS `allDays`,(case when ((`rt`.`trainDirection` = 'East') and (`t`.`trainDays` <> `rt`.`trainDays`)) then `rt`.`trainDays` else '' end) AS `eastDays`,`rt`.`trainNumber` AS `eastTrain` from (`trains` `t` join `trains` `rt`) where ((`t`.`trainNumber` = `rt`.`reverseDirectionTrainNum`) and (`t`.`trainDirection` = 'West')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `train_segments_vw`
--

/*!50001 DROP TABLE IF EXISTS `train_segments_vw`*/;
/*!50001 DROP VIEW IF EXISTS `train_segments_vw`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`foggyhollow`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `train_segments_vw` AS select `t`.`trainNumber` AS `trainNumber`,`ss`.`segmentDirection` AS `segmentDirection`,`ts`.`segmentStartTime` AS `segmentStartTime`,`ts`.`segmentCode` AS `segmentCode`,(case `ss`.`sectionOrder` when 0 then `ts`.`segmentDelay` else 0 end) AS `segmentDelay`,`ss`.`sectionCode` AS `sectionCode`,`s`.`distance` AS `distance`,(case `ss`.`segmentDirection` when 'W' then (select `l`.`locationName` from `locations` `l` where (`l`.`locationId` = `s`.`startLocationId`)) when 'E' then (select `l`.`locationName` from `locations` `l` where (`l`.`locationId` = `s`.`endLocationId`)) end) AS `startLocation`,(case `ss`.`segmentDirection` when 'W' then `s`.`startLocationCode` when 'E' then `s`.`endLocationCode` end) AS `startLocationCode`,(case `ss`.`segmentDirection` when 'W' then (select `l`.`locationName` from `locations` `l` where (`l`.`locationId` = `s`.`endLocationId`)) when 'E' then (select `l`.`locationName` from `locations` `l` where (`l`.`locationId` = `s`.`startLocationId`)) end) AS `endLocation`,(case `ss`.`segmentDirection` when 'W' then `s`.`endLocationCode` when 'E' then `s`.`startLocationCode` end) AS `endLocationCode`,(case `ss`.`segmentDirection` when 'W' then `s`.`avgSpeedWest` when 'E' then `s`.`avgSpeedEast` end) AS `avgSpeed`,`ts`.`segmentOrder` AS `segmentOrder`,`ss`.`sectionOrder` AS `sectionOrder` from (((`trains` `t` join `train_segments` `ts`) join `segment_sections` `ss`) join `sections` `s`) where ((`t`.`trainNumber` = `ts`.`trainNumber`) and (`ts`.`segmentCode` = `ss`.`segmentCode`) and (`ss`.`sectionCode` = `s`.`sectionName`)) order by `t`.`trainNumber`,`ts`.`segmentOrder`,`ss`.`sectionOrder` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-02-14 17:14:21
