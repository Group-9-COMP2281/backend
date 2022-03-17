SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `engagement-db`
--
CREATE DATABASE IF NOT EXISTS `engagement-db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `engagement-db`;

-- --------------------------------------------------------

--
-- Table structure for table `Attachment`
--

CREATE TABLE `Attachment` (
  `attachment_id` int NOT NULL,
  `post_id` int NOT NULL,
  `url` varchar(2048) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Post`
--

CREATE TABLE `Post` (
  `post_id` int NOT NULL,
  `service_id` varchar(32) DEFAULT NULL,
  `post_author` varchar(15) DEFAULT NULL,
  `post_text` varchar(500) DEFAULT NULL,
  `date_posted` datetime NOT NULL,
  `date_found` datetime NOT NULL,
  `url` varchar(280) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `University`
--

CREATE TABLE `University` (
  `university_name` varchar(100) NOT NULL,
  `post_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Attachment`
--
ALTER TABLE `Attachment`
  ADD PRIMARY KEY (`attachment_id`,`post_id`);

--
-- Indexes for table `Post`
--
ALTER TABLE `Post`
  ADD PRIMARY KEY (`post_id`),
  ADD UNIQUE KEY `service_id` (`service_id`);

--
-- Indexes for table `University`
--
ALTER TABLE `University`
  ADD PRIMARY KEY (`university_name`,`post_id`),
  ADD KEY `post_id_idx` (`post_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Attachment`
--
ALTER TABLE `Attachment`
  MODIFY `attachment_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Post`
--
ALTER TABLE `Post`
  MODIFY `post_id` int NOT NULL AUTO_INCREMENT;
COMMIT;
