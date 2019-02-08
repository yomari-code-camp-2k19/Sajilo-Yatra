-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 08, 2019 at 05:41 AM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sajilo_yatra`
--

-- --------------------------------------------------------

--
-- Table structure for table `alltrip_table`
--

CREATE TABLE `alltrip_table` (
  `user_id` int(11) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `alltrip_table`
--

INSERT INTO `alltrip_table` (`user_id`, `id`) VALUES
(1, 2),
(1, 2),
(1, 2),
(4, 8),
(4, 10),
(4, 1),
(4, 8),
(4, 10),
(4, 1),
(4, 1),
(4, 8),
(4, 9),
(4, 10),
(4, 8),
(4, 10),
(4, 1),
(4, 1),
(4, 8),
(4, 9),
(4, 10),
(4, 1),
(4, 8),
(4, 9),
(4, 10);

-- --------------------------------------------------------

--
-- Table structure for table `local_table`
--

CREATE TABLE `local_table` (
  `id` int(11) NOT NULL,
  `location` varchar(200) NOT NULL,
  `festival` varchar(200) NOT NULL,
  `food` varchar(200) NOT NULL,
  `events` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  `timing` varchar(50) NOT NULL,
  `date` datetime NOT NULL,
  `duration` int(11) NOT NULL,
  `description` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `local_table`
--

INSERT INTO `local_table` (`id`, `location`, `festival`, `food`, `events`, `user_id`, `timing`, `date`, `duration`, `description`) VALUES
(1, 'kathmandu', 'Indra Jatra', '', '', 3, 'morning to evening', '2011-01-01 06:00:00', 12, 'aaaaaaaaaaaaaa'),
(7, 'pokhara', 'Gode Jatra', '', '', 3, 'morning to afternoon', '2011-01-20 10:00:00', 2, 'bbbbbbbb'),
(8, 'kathmandu', '', 'yomari', '', 3, 'anytime', '2011-01-20 06:00:00', 12, 'ccccccc'),
(9, 'kathmandu', 'Seto Machindra', '', '', 3, 'morning to evening', '2011-01-01 06:00:00', 12, 'cccccccccccccccccccc'),
(10, 'kathmandu', 'Maghe Sakrati', '', '', 3, 'morning to evening', '2011-01-01 06:00:00', 12, 'dddddddddddddddddddd'),
(11, 'pokhara', 'Rato Machindra', '', '', 5, 'morning to evening', '2011-01-01 06:00:00', 12, 'red color');

-- --------------------------------------------------------

--
-- Table structure for table `register_table`
--

CREATE TABLE `register_table` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `pw` varchar(200) NOT NULL,
  `user_type` varchar(20) NOT NULL,
  `location` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register_table`
--

INSERT INTO `register_table` (`user_id`, `user_name`, `pw`, `user_type`, `location`) VALUES
(3, 'manish', '$5$rounds=535000$qaWIvMXNTazQ9ZAd$gW2dR7DoVTqgja9k6r9x8MDWx2FzcDAZ4kWtADjvYFB', 'mentor', 'kathmandu'),
(4, 'neha', '$5$rounds=535000$/D57RKUaHSoIDdmD$02k90yB8TN9fM6PTirhwf7FOclzvG0hE9e9ZREwh/gC', 'user', 'NULL'),
(5, 'ramu', '$5$rounds=535000$gFpuEpIUv1nTR4jZ$s1evqWd9YxjHjZelKjgxHtjcVi0aBnDxvs3.hK86zd4', 'mentor', 'pokhara');

-- --------------------------------------------------------

--
-- Table structure for table `review_table`
--

CREATE TABLE `review_table` (
  `id` int(11) NOT NULL,
  `rating` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `review_table`
--

INSERT INTO `review_table` (`id`, `rating`) VALUES
(1, 3.2),
(7, 2.2),
(8, 4.7),
(9, 1),
(10, 4.2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `local_table`
--
ALTER TABLE `local_table`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `register_table`
--
ALTER TABLE `register_table`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `local_table`
--
ALTER TABLE `local_table`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `register_table`
--
ALTER TABLE `register_table`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
