-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 11, 2025 at 05:06 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbtokoa`
--

-- --------------------------------------------------------

--
-- Table structure for table `barang`
--

CREATE TABLE `barang` (
  `id` int NOT NULL,
  `nama` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `harga` decimal(50,0) NOT NULL,
  `stok` int NOT NULL,
  `kategori` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `deskripsi` text COLLATE utf8mb4_general_ci NOT NULL,
  `gambar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `barang`
--

INSERT INTO `barang` (`id`, `nama`, `harga`, `stok`, `kategori`, `deskripsi`, `gambar_url`) VALUES
(6, 'Apple iPhone 15 - Pink, 128GB', '8000000', 1, 'Elektronik', 'In The Box :\r\n- iPhone 15\r\n- USB-C Charge Cable\r\n- Dokumentasi\r\n\r\nSpesifikasi :\r\n- 6.1 inch ( iPhone 15 )\r\n- Super Retina XDR display\r\n- Aluminum with color-infused glass back\r\n- Dynamic Island, A magical way to interact with iPhone\r\n- A16 Bionic chip with 5-core GPU\r\n- Advanced dual-camera system 48MP Main | 12MP Ultra Wide\r\n- Selfie Camera 12 MP\r\n- USB Type-C 2.0, DisplayPort\r\n- NFC Yes\r\n\r\nWarranty :\r\nGaransi IBOX = bisa di claim di service center resmi apple IBOX kode barang randomID/PA/SA\r\n\r\nWarna :Pink\r\n\r\nFREE : Tempered Glass + Softcase ( Selama persediaan masih ada dan tidak bisa komplain )', 'https://www.digimap.co.id/cdn/shop/files/iPhone_15_Pink_PDP_Image_Position-1__GBEN.jpg?v=1717730898&width=1920'),
(9, 'samsung a55', '6000000', 8, 'Elektronik', 'harga murah', 'https://www.static-src.com/wcsstore/Indraprastha/images/catalog/full/catalog-image/103/MTA-162086655/samsung_samsung_galaxy_a55_5g_full02_jcey6vz1.jpg'),
(17, 'Asus Rog Strix G16 G614jv Core I7 13650hx', '29999999', 7, 'Elektronik', 'f', 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcTyFktcZar6MJWrI1UwsCUTy_ZugXK5LOefdjYSBu967U1_jFoXdMBc_ojrD5VOmfU7y9R0qGVjIgAgceONpi4kjVffDGlPs3WIG2M0EsipS7GXN_xMlm_K'),
(21, 'SAMSUNG 980 PCIE 3.0 NVME M.2 SSD 1TB | SSD M.2 NVMe Gen 3 x4 1TB', '1339000', 5, 'Elektronik', 'SKU	170957\r\nSeries	980\r\nCapacity	1TB\r\nInterface	PCI-Express 3.0 x4, NVMe 1.4\r\nController	Pablo\r\nMemory Components	V-NAND MLC\r\nMax. Sequential Read	Up to 3500 MBps\r\nMax. Sequential Write	Up to 3000 MBps\r\nForm Factor	M.2 2280\r\nWarranty	5 Year(s)', 'https://raw.githubusercontent.com/zhiif/inventorybarang/refs/heads/main/ssd.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `detail_transaksi`
--

CREATE TABLE `detail_transaksi` (
  `id` int NOT NULL,
  `transaksi_id` int DEFAULT NULL,
  `barang_id` int DEFAULT NULL,
  `nama_barang` varchar(100) DEFAULT NULL,
  `harga` int DEFAULT NULL,
  `jumlah` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id` int NOT NULL,
  `tanggal` datetime NOT NULL,
  `total` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int NOT NULL,
  `username` varchar(191) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(191) COLLATE utf8mb4_general_ci NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `role`) VALUES
(1, 'admin', 'admin', 'admin'),
(2, 'fuad', 'fuad123', 'user'),
(3, 'khoirul', 'khoirul123', 'user'),
(4, 'nazhif', 'nazhif123', 'user'),
(9, 'rani', 'anii', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `barang`
--
ALTER TABLE `barang`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `transaksi_id` (`transaksi_id`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `barang`
--
ALTER TABLE `barang`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  ADD CONSTRAINT `detail_transaksi_ibfk_1` FOREIGN KEY (`transaksi_id`) REFERENCES `transaksi` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
