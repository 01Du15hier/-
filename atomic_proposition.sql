-- MySQL dump 10.13  Distrib 5.5.36, for Win32 (x86)
--
-- Host: localhost    Database: atomic_proposition
-- ------------------------------------------------------
-- Server version	5.5.36

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
-- Table structure for table `atomic_proposition`
--

DROP TABLE IF EXISTS `atomic_proposition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `atomic_proposition` (
  `Atomic_proposition_num` char(10) DEFAULT NULL,
  `meaning` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atomic_proposition`
--

LOCK TABLES `atomic_proposition` WRITE;
/*!40000 ALTER TABLE `atomic_proposition` DISABLE KEYS */;
INSERT INTO `atomic_proposition` VALUES ('1','hairy'),('2','can_give_milk'),('3','feather'),('4','can_fly'),('5','can_lay_eggs'),('6','eat_meat'),('7','have_canine_teeth'),('8','have_claws'),('9','eyes_stare_at_the_front'),('10','tawny'),('11','dark_spots'),('12','black_stripe'),('13','have_long_legs'),('14','long_neck'),('15','black'),('16','can\'t_fly'),('18','hoof'),('19','good_at_flying'),('20','leopard'),('21','tiger'),('22','penguin'),('23','ostrich'),('24','zebra'),('25','albatross'),('26','bird'),('17','can_swim'),('27','giraffe'),('28','carnivore'),('29','birds'),('30','ungulates'),('31','mammal'),('32','ruminant');
/*!40000 ALTER TABLE `atomic_proposition` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-06 17:09:21
