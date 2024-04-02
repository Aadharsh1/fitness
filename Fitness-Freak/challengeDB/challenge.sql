-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `challenge`
--
CREATE DATABASE IF NOT EXISTS `challenge` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `challenge`;

-- --------------------------------------------------------

--
-- Table structure for table `challenge`
--

DROP TABLE IF EXISTS `challenge`;
CREATE TABLE IF NOT EXISTS `challenge` (
  `title` varchar(64) NOT NULL,
  `description` varchar(64) NOT NULL,
  `id` char(5) NOT NULL,
  `reps` varchar(64) NOT NULL,
  `fitnessLevel` varchar(64) NOT NULL,
  `loyaltyPoints` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `book`
--

INSERT INTO `challenge` (`title`, `description`, `id`, `reps`, `fitnessLevel`, `loyaltyPoints`) VALUES
('Pushup', 'Pushup Challenge', '12345', '20', 'Healthy weight', 100),
('Situp', 'Situp Challenge', '22345', '60', 'Healthy weight', 150),
('Squat', 'Squat Challenge', '32345', '40', 'Healthy weight', 150),
('Plank', 'Plank  Challenge', '42345', '1 minute', 'Healthy weight', 150);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;