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
-- Database: `product`
--
CREATE DATABASE IF NOT EXISTS `product` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `product`;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `title` varchar(64) NOT NULL,
  `description` varchar(64) NOT NULL,
  `id` char(5) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `availability` int(11) DEFAULT NULL,
  `image` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `book`
--

INSERT INTO `product` (`title`, `description`, `id`, `price`, `availability`, `image`) VALUES
('Nike Shirt', 'Dri-fit shirt', '12345', '21.50', 21, 'https://i.ebayimg.com/images/g/tWUAAOSwiqdiqIRb/s-l1200.webp'),
('Blenderbottle', 'Water bottle', '22345', '99.40', 25, 'https://m.media-amazon.com/images/I/71XRC23uTJL._AC_SL1500_.jpg'),
('5-kg Dumbbell', 'Dumbbell', '32345', '15.00', 30, 'https://i.ebayimg.com/images/g/y1wAAOSw6ZpgHawc/s-l1200.webp'),
('Towel', 'Gym Towel', '62345','11.00', 75, 'https://images-na.ssl-images-amazon.com/images/I/713sl9p3dWL.jpg');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;