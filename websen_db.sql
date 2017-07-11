-- phpMyAdmin SQL Dump
-- version 4.5.4.1
-- http://www.phpmyadmin.net
--
-- Host: localhost:3306
-- Generation Time: Jul 10, 2017 at 05:54 PM
-- Server version: 5.6.29
-- PHP Version: 5.6.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `websen_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `absen`
--

CREATE TABLE `absen` (
  `id` int(11) NOT NULL,
  `pegawai_id` int(11) DEFAULT NULL,
  `masuk` tinyint(4) DEFAULT '0',
  `keluar` tinyint(4) DEFAULT '0',
  `tanggal` date DEFAULT NULL,
  `create_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `jabatan`
--

CREATE TABLE `jabatan` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) DEFAULT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `jabatan`
--

INSERT INTO `jabatan` (`id`, `nama`, `create_at`, `update_at`) VALUES
(1, 'Administrator', '2017-05-29 23:07:43', '2017-05-29 23:17:14'),
(3, 'Pegawai', '2017-06-04 00:44:48', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `jadwal`
--

CREATE TABLE `jadwal` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `display_name` varchar(50) NOT NULL,
  `jadwal_masuk_start` time NOT NULL,
  `jadwal_masuk_end` time NOT NULL,
  `jadwal_keluar_start` time NOT NULL,
  `jadwal_keluar_end` time NOT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `jadwal`
--

INSERT INTO `jadwal` (`id`, `nama`, `display_name`, `jadwal_masuk_start`, `jadwal_masuk_end`, `jadwal_keluar_start`, `jadwal_keluar_end`, `create_at`, `update_at`) VALUES
(3, 'pagi', 'Pagi', '07:30:00', '08:00:00', '13:00:00', '13:30:00', '2017-06-03 23:46:14', '2017-06-04 00:53:20'),
(5, 'siang', 'Siang', '12:30:00', '13:00:00', '17:00:00', '17:30:00', '2017-06-04 00:58:23', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `pegawai`
--

CREATE TABLE `pegawai` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `nip` varchar(11) NOT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `tempat_lahir` varchar(50) NOT NULL,
  `alamat` text NOT NULL,
  `foto` varchar(255) NOT NULL,
  `jabatan_id` int(11) DEFAULT NULL,
  `jadwal_id` int(11) DEFAULT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pegawai`
--

INSERT INTO `pegawai` (`id`, `nama`, `nip`, `tanggal_lahir`, `tempat_lahir`, `alamat`, `foto`, `jabatan_id`, `jadwal_id`, `create_at`, `update_at`, `user_id`) VALUES
(7, 'Eman Widiawati', '', '1993-10-23', 'Dompu', 'Konte, Dompu', '', 1, 3, '2017-06-04 03:26:41', '2017-06-04 03:27:41', 7),
(8, 'Wardi Rusmwatai', '86547874675', '1993-11-20', 'Lengkok Lendang', '', '/static/uploads/profile/logo.png', 3, 5, '2017-06-04 03:30:32', NULL, 11),
(9, 'nilham', '085436', '0000-00-00', 'masbagen', '', '/static/uploads/profile/Capturea.PNG', 3, 5, '2017-06-04 05:40:18', NULL, 12),
(10, 'eter', '099989900', '2017-06-06', 'lendang dangka', '', '/static/uploads/profile/Captures.PNG', 1, 3, '2017-06-04 05:44:02', NULL, 13),
(11, 'ahmad syrif hidayat', '0446365674', '0000-00-00', 'bermi', '', '/static/uploads/profile/Captureass.PNG', 3, 3, '2017-06-04 05:46:06', NULL, 14),
(12, 'depi', '0976543', '0000-00-00', 'apitai', '', '/static/uploads/profile/Capturea.PNG', 3, 5, '2017-06-04 05:47:59', NULL, 15),
(13, 'ermawati', '0094274', '0000-00-00', 'kelayu', '', '/static/uploads/profile/Capture.PNG', 3, 3, '2017-06-04 05:53:19', NULL, 16);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(45) NOT NULL,
  `active` tinyint(1) DEFAULT '0',
  `create_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `active`, `create_at`, `update_at`) VALUES
(7, 'admin', '21232f297a57a5a743894a0e4a801fc3', 1, '2017-05-30 03:26:58', '2017-06-03 23:50:29'),
(11, 'wardi_8lh', '3c1d2a53bd3c7ed9765ed26c46a0edea', 1, '2017-06-04 03:30:32', '2017-06-04 03:40:40'),
(12, 'nilham_0xw', 'f58cd1d236eba7fd8504425c1c507a40', 1, '2017-06-04 05:40:18', '2017-06-04 06:00:34'),
(13, 'eter_lxa', '05b675e8875cb64890d7f8c1c36eed61', 0, '2017-06-04 05:44:02', NULL),
(14, 'ahmad_n2x', '033794271ccdd402e25ed23a17211ac0', 0, '2017-06-04 05:46:06', NULL),
(15, 'depi_dx4', '3dcd19f383c779060aed9da30e968bcd', 0, '2017-06-04 05:47:59', NULL),
(16, 'ermawati_n5q', 'f2e77697e8f82bc1a0e9a427e43f26a9', 0, '2017-06-04 05:53:19', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `absen`
--
ALTER TABLE `absen`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_absen_pegawai` (`pegawai_id`);

--
-- Indexes for table `jabatan`
--
ALTER TABLE `jabatan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pegawai`
--
ALTER TABLE `pegawai`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nip` (`nip`),
  ADD KEY `FK_pegawai_jadwal` (`jadwal_id`),
  ADD KEY `FK_pegawai_jabatan` (`jabatan_id`),
  ADD KEY `FK_pegawai_users` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `absen`
--
ALTER TABLE `absen`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `jabatan`
--
ALTER TABLE `jabatan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `jadwal`
--
ALTER TABLE `jadwal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `pegawai`
--
ALTER TABLE `pegawai`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `absen`
--
ALTER TABLE `absen`
  ADD CONSTRAINT `FK_absen_pegawai` FOREIGN KEY (`pegawai_id`) REFERENCES `pegawai` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `pegawai`
--
ALTER TABLE `pegawai`
  ADD CONSTRAINT `FK_pegawai_jabatan` FOREIGN KEY (`jabatan_id`) REFERENCES `jabatan` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_pegawai_jadwal` FOREIGN KEY (`jadwal_id`) REFERENCES `jadwal` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_pegawai_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
