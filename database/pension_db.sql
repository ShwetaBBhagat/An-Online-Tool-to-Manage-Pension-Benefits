-- MySQL dump 10.13  Distrib 9.2.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: pension_db
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL,
  `role` enum('user','admin') DEFAULT NULL,
  `mfa_secret` varchar(32) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'John Doe','john@example.com','$2b$12$lCTgRzKnxYOszJugDLufE.etXkN2eB3YjAU5ssVrhBTlX3zl66uoC','user','BKSDCWWOX4RAVQU3GFISHOW7EJO2XNP2','2025-03-06 20:18:39'),(2,'Rachel Green','rachel@example.com','$2b$12$pEt2Ozq0cLTv0Fkij9dbD.xfG39F8aUk.3X1vEu8tIFivwPH/Z3nu','user','SSMLJJR4MGZBHFQMVX63IAVSIX3TKSRK','2025-03-06 20:32:50'),(3,'Alex Russo','alex@example.com','$2b$12$L3omponfOLqYSLu37bxRUeli3zdKPHnYzvB6914VP5rzgzUPrRXCy','user','NLZ65HLQ4PH5CFR7OWPDSWILXY6P2FPT','2025-03-06 22:06:30'),(4,'James Bond','james@example.com','$2b$12$emGtmuT/l3nrSAc3QmyQu..ldoEmGb0CkCtkfZEJ93njimn6QjEgq','user','N27ODEMEUFIJQD4TCBPWB7H7OSS2FZ33','2025-03-06 22:10:16'),(5,'robin hood','robin@example.com','$2b$12$ZpKf/dZLtOHpjBw/SVOxz.OHA/IF8iohgAOGMPrdnQKfOGdVroOou','user','JK3NKBHJ4DIOB6L6W63A6EWYQ7PEZILU','2025-03-06 22:20:45');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-06 22:27:45
