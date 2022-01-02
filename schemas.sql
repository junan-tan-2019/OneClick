--
-- Create Schema/Database for service 0 
--

CREATE DATABASE `stocks` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE stocks;

DROP TABLE IF EXISTS `stocks`;

CREATE TABLE `stocks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location` varchar(64) NOT NULL,
  `longitude` float NOT NULL,
  `latitude` float NOT NULL,
  `stock` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- 
-- Dumping data for table `stocks`
--

INSERT INTO `stocks` VALUES 
(1,'Choa Chu Kang CC', 1.38140, 103.75161, 100),
(2,'Woodland CC', 1.43983, 103.78824, 195),
(3,'Tampines Central CC', 1.35310, 103.94036, 75),
(4,'Punggol Park CC', 1.37814, 103.89633, 200),
(5,'Carinhill CC', 1.31044, 103.83925, 100);

--
-- Create Schema/Database for service 1
--

CREATE DATABASE `registration` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE registration;

DROP TABLE IF EXISTS `registration`;

CREATE TABLE `registration` (
  `PHONENUM` varchar(8) NOT NULL,
  `LOCATION` varchar(255) NOT NULL,
  `UNQREF` varchar(255) NOT NULL,
  PRIMARY KEY (`UNQREF`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


--
-- Create Schema/Database for service 4
--

CREATE DATABASE `collection` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE collection;

DROP TABLE IF EXISTS `item_collection`;

CREATE TABLE `item_collection` (
  `unique_ref` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `phone_number` varchar(8) NOT NULL,
  PRIMARY KEY(`unique_ref`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;