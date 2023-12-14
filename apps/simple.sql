-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 13, 2023 at 10:40 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `simple`
--

-- --------------------------------------------------------

--
-- Table structure for table `addresses`
--

CREATE TABLE `addresses` (
  `Address_ID` int(11) NOT NULL,
  `Street` varchar(255) DEFAULT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `Zipcode` varchar(255) DEFAULT NULL,
  `Country` varchar(255) DEFAULT NULL,
  `Person_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `addresses`
--

INSERT INTO `addresses` (`Address_ID`, `Street`, `City`, `State`, `Zipcode`, `Country`, `Person_ID`) VALUES
(157, '6642 Brianna Turnpike', 'North Barbaraside', 'South Dakota', '90854', 'Islands', 6),
(207, '9422 Gibbs Gateway', 'Orozcoview', 'California', '25232', 'India', 1),
(215, '9979 Welch Meadow', 'East Danielle', 'Alaska', '81144', 'Mongolia', 4),
(281, '43072 Carter Grove', 'West Andreafurt', 'Delaware', '22744', 'Mozambique', 9),
(436, '3285 Watson Springs', 'West Nicole', 'Minnesota', '32065', 'Gambia', 3),
(530, '5660 Terry Prairie', 'Lake Jamesside', 'Oregon', '35506', 'Lesotho', 7),
(600, '662 Johnson Square', 'North Andreaville', 'Montana', '91773', 'Mayotte', 10),
(707, '8973 Johnathan Glens', 'South Michelle', 'Louisiana', '26226', 'Australia', 8),
(739, '441 Jennings Tunnel', 'Lake Kristin', 'Missouri', '56047', 'Norway', 2),
(983, '81387 Dylan Knolls', 'Port Lauren', 'Rhode Island', '82490', 'Ethiopia', 5),
(987, 'ward no. 8 near AMsoft technologies Doctor accadmy street lodhran', 'lodhran', 'punjab', '59320', 'Pakistan', 71),
(988, 'Peace lounge, gulshan e khudad Appartment A2 ,E11/1', 'Islamabad', 'Pakistan', '44000', 'Pakistan', 72),
(989, 'street 3', 'Chichago', 'California', 'E26 JA', 'USA', 73);

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `contracts`
--

CREATE TABLE `contracts` (
  `Contract_ID` int(11) NOT NULL,
  `Installation_date` date DEFAULT NULL,
  `Monthly_charges` decimal(10,2) DEFAULT NULL,
  `Billing_date` date DEFAULT NULL,
  `Renewal_date` date DEFAULT NULL,
  `Person_ID` int(11) NOT NULL,
  `Role` enum('Executive','Legal','Accountant') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contracts`
--

INSERT INTO `contracts` (`Contract_ID`, `Installation_date`, `Monthly_charges`, `Billing_date`, `Renewal_date`, `Person_ID`, `Role`) VALUES
(139, '2021-11-24', 425.69, '2021-04-05', '2026-10-17', 1, 'Executive'),
(150, '2018-05-10', 150.55, '2022-02-21', '2027-06-21', 2, 'Executive'),
(181, '2018-11-15', 74.63, '2022-01-19', '2028-04-20', 3, 'Executive'),
(267, '2020-01-25', 346.58, '2020-08-16', '2025-02-08', 10, 'Executive'),
(432, '2019-10-28', 166.43, '2019-11-12', '2024-08-04', 9, 'Executive'),
(702, '2019-06-14', 112.78, '2018-07-20', '2028-05-02', 8, 'Executive'),
(821, '2020-12-01', 476.11, '2019-03-13', '2025-08-12', 7, 'Executive'),
(916, '2021-03-09', 482.60, '2020-10-10', '2026-03-31', 6, 'Executive'),
(968, '2018-04-18', 290.96, '2018-02-12', '2027-09-06', 1, 'Executive'),
(974, '2019-01-09', 253.94, '2019-08-26', '2024-04-19', 2, 'Executive'),
(975, '2019-06-14', 112.78, '2018-07-20', '2028-05-02', 1, 'Legal'),
(976, '2023-12-13', 123.00, '2023-12-29', '2023-12-18', 71, 'Legal'),
(977, '2023-12-12', 1220.00, '2023-12-21', '2024-01-04', 71, 'Legal'),
(978, '2023-12-20', 123.00, '2023-12-15', '2023-11-30', 71, 'Legal');

-- --------------------------------------------------------

--
-- Table structure for table `contract_equipments`
--

CREATE TABLE `contract_equipments` (
  `Contract_ID` int(11) NOT NULL,
  `Equipment_ID` int(11) NOT NULL,
  `Person_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contract_equipments`
--

INSERT INTO `contract_equipments` (`Contract_ID`, `Equipment_ID`, `Person_ID`) VALUES
(976, 7, 4),
(139, 7, 5),
(978, 7, 5),
(977, 983, 72);

-- --------------------------------------------------------

--
-- Table structure for table `equipments`
--

CREATE TABLE `equipments` (
  `Equipment_ID` int(11) NOT NULL,
  `Asset_Tag_Number` varchar(255) DEFAULT NULL,
  `Equipment_name` varchar(255) DEFAULT NULL,
  `Serial_number` varchar(255) DEFAULT NULL,
  `Install_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `equipments`
--

INSERT INTO `equipments` (`Equipment_ID`, `Asset_Tag_Number`, `Equipment_name`, `Serial_number`, `Install_date`) VALUES
(7, 'QWE-45678', 'Lenovo', '23213323', '2023-12-13'),
(120, 'sMtLwNxQ', 'webcam', 'XyZbCfDgHj', '2022-01-12'),
(253, 'hLpDgBxQ', 'mouse', 'RfGhJkMnLp', '2021-03-21'),
(320, 'tQpNzDmG', 'printer', 'JhZqFxGyLd', '2021-10-17'),
(394, 'kVnJwFyH', 'keyboard', 'QmBtCnDpFw', '2018-07-14'),
(424, 'gTTRxLmC', 'router', 'QzWxYTjLsV', '2020-07-30'),
(539, 'DkXlTPwB', 'modem', 'XwRLvBpFgG', '2019-02-11'),
(606, 'mQyZxLpW', 'scanner', 'FqWbHpJvYs', '2018-03-25'),
(761, 'qRtKwVbY', 'computer', 'DxQlMnGtJv', '2020-01-06'),
(877, 'wJhQpNgR', 'laptop', 'GfHpJzKvYt', '2019-06-05'),
(981, 'cXgFzHtK', 'monitor', 'KvLwMbNpGt', '2022-05-02'),
(982, 'mmmmm', 'asdasda', 'asdsadasd', '2023-12-14'),
(983, 'qwe4321', 'testEquip', '1234567890', '2023-12-12'),
(984, '1234', 'M24', '1122', '2023-12-13');

-- --------------------------------------------------------

--
-- Table structure for table `flask_dance_oauth`
--

CREATE TABLE `flask_dance_oauth` (
  `id` int(11) NOT NULL,
  `provider` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL,
  `token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`token`)),
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `persons`
--

CREATE TABLE `persons` (
  `Person_ID` int(11) NOT NULL,
  `First_Name` varchar(255) DEFAULT NULL,
  `Last_Name` varchar(255) DEFAULT NULL,
  `Gender` char(10) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Role` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `persons`
--

INSERT INTO `persons` (`Person_ID`, `First_Name`, `Last_Name`, `Gender`, `Email`, `Role`) VALUES
(1, 'John', 'Doe', 'M', 'john.doe@example.com', 'Software Developer'),
(2, 'Jane', 'Smith', 'F', 'jane.smith@example.com', 'Project Manager'),
(3, 'Bob', 'Brown', 'M', 'bob.brown@example.com', 'Analyst'),
(4, 'Emily', 'Johnson', 'F', 'emily.johnson@example.com', 'Client'),
(5, 'Michael', 'Davis', 'M', 'michael.davis@example.com', 'Client'),
(6, 'Laura', 'Miller', 'F', 'laura.miller@example.com', 'Administrator'),
(7, 'Steve', 'Wilson', 'M', 'steve.wilson@example.com', 'Consultant'),
(8, 'Sarah', 'Taylor', 'F', 'sarah.taylor@example.com', 'HR Manager'),
(9, 'David', 'Moore', 'M', 'david.moore@example.com', 'Marketing Specialist'),
(10, 'Linda', 'Anderson', 'F', 'linda.anderson@example.com', 'Sales Associate'),
(71, 'Ahsan', 'Rao', 'M', 'raoahsan110@gmail.com', 'Legal'),
(72, 'nyphomanic', 'ism', 'Male', 'nyphomanicism@gmail.com', 'Client'),
(73, 'ahmad waleed', 'hamid', 'Male', 'abc@123.com', 'Client');

-- --------------------------------------------------------

--
-- Table structure for table `phone_numbers`
--

CREATE TABLE `phone_numbers` (
  `Phone_ID` int(11) NOT NULL,
  `Home_Phone_Number` varchar(255) DEFAULT NULL,
  `Business_Phone_Number` varchar(255) DEFAULT NULL,
  `Person_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `phone_numbers`
--

INSERT INTO `phone_numbers` (`Phone_ID`, `Home_Phone_Number`, `Business_Phone_Number`, `Person_ID`) VALUES
(1, '555-1234', '555-5678', 1),
(2, '555-2345', '555-6789', 2),
(3, '555-3456', '555-7890', 3),
(4, '555-4567', '555-8901', 4),
(5, '555-5678', '555-9012', 5),
(6, '555-6789', '555-0123', 6),
(7, '555-7890', '555-1234', 7),
(8, '555-8901', '555-2345', 8),
(9, '555-9012', '555-3456', 9),
(10, '555-0123', '555-4567', 10),
(21, '03106884650', '', 71),
(22, '03419602305', '', 72),
(23, '1234556', '12344456', 73);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `password` blob DEFAULT NULL,
  `oauth_github` varchar(100) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `about` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `oauth_github`, `first_name`, `last_name`, `address`, `about`) VALUES
(1, 'ash', 'rao@gmail.com', 0x633534393465386431343865323137616435333330343130653961363562343633306166376432366438363537653464333536643263636463316435636633636365363331663631363764623038663130356239623664623833626434323039323362353232333337393664306636666439313836303335313735646163386238383530373539666636306263396562323662306163616265326237346138313862663131353361353366323936653034386266323265306539393435656634, NULL, 'ahsan', 'rao', 'nothing', 'about me'),
(5, 'user', 'nyphomanicism@gmail.com', 0x356230666430326564376333636134303431643733353133616232326362353233323263623763666662373064336364343138656332386537366561323736316661386630333066313336386532333964373361656530613461333038373461316562643238303835396463613033613063616439366166353039656663313938663961613366366463326666636464343838393764646432643932653134323862386131363566656139633530636662663934333465643430353230633063, NULL, NULL, NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `addresses`
--
ALTER TABLE `addresses`
  ADD PRIMARY KEY (`Address_ID`),
  ADD KEY `Person_ID` (`Person_ID`);

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `contracts`
--
ALTER TABLE `contracts`
  ADD PRIMARY KEY (`Contract_ID`),
  ADD KEY `fk_person_id` (`Person_ID`);

--
-- Indexes for table `contract_equipments`
--
ALTER TABLE `contract_equipments`
  ADD PRIMARY KEY (`Contract_ID`,`Equipment_ID`),
  ADD KEY `Equipment_ID` (`Equipment_ID`),
  ADD KEY `Person_ID` (`Person_ID`);

--
-- Indexes for table `equipments`
--
ALTER TABLE `equipments`
  ADD PRIMARY KEY (`Equipment_ID`),
  ADD UNIQUE KEY `Asset_Tag_Number` (`Asset_Tag_Number`),
  ADD UNIQUE KEY `Serial_number` (`Serial_number`);

--
-- Indexes for table `flask_dance_oauth`
--
ALTER TABLE `flask_dance_oauth`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `persons`
--
ALTER TABLE `persons`
  ADD PRIMARY KEY (`Person_ID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `phone_numbers`
--
ALTER TABLE `phone_numbers`
  ADD PRIMARY KEY (`Phone_ID`),
  ADD KEY `Person_ID` (`Person_ID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `addresses`
--
ALTER TABLE `addresses`
  MODIFY `Address_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=990;

--
-- AUTO_INCREMENT for table `contracts`
--
ALTER TABLE `contracts`
  MODIFY `Contract_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=979;

--
-- AUTO_INCREMENT for table `equipments`
--
ALTER TABLE `equipments`
  MODIFY `Equipment_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=985;

--
-- AUTO_INCREMENT for table `flask_dance_oauth`
--
ALTER TABLE `flask_dance_oauth`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `persons`
--
ALTER TABLE `persons`
  MODIFY `Person_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

--
-- AUTO_INCREMENT for table `phone_numbers`
--
ALTER TABLE `phone_numbers`
  MODIFY `Phone_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `addresses`
--
ALTER TABLE `addresses`
  ADD CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`Person_ID`) REFERENCES `persons` (`Person_ID`);

--
-- Constraints for table `contracts`
--
ALTER TABLE `contracts`
  ADD CONSTRAINT `fk_person_id` FOREIGN KEY (`Person_ID`) REFERENCES `Persons` (`Person_ID`);

--
-- Constraints for table `contract_equipments`
--
ALTER TABLE `contract_equipments`
  ADD CONSTRAINT `contract_equipments_ibfk_1` FOREIGN KEY (`Contract_ID`) REFERENCES `contracts` (`Contract_ID`),
  ADD CONSTRAINT `contract_equipments_ibfk_2` FOREIGN KEY (`Equipment_ID`) REFERENCES `equipments` (`Equipment_ID`),
  ADD CONSTRAINT `contract_equipments_ibfk_3` FOREIGN KEY (`Person_ID`) REFERENCES `persons` (`Person_ID`);

--
-- Constraints for table `flask_dance_oauth`
--
ALTER TABLE `flask_dance_oauth`
  ADD CONSTRAINT `flask_dance_oauth_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `phone_numbers`
--
ALTER TABLE `phone_numbers`
  ADD CONSTRAINT `phone_numbers_ibfk_1` FOREIGN KEY (`Person_ID`) REFERENCES `persons` (`Person_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
