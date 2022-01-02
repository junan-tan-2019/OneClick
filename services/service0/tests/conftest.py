import pytest


@pytest.fixture
def client():
    from src import service_0

    service_0.app.config['TESTING'] = True

    service_0.db.engine.execute('DROP TABLE IF EXISTS `stocks`;')

    service_0.db.engine.execute('''CREATE TABLE `stocks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location` varchar(64) NOT NULL,
  `longitude` float NOT NULL,
  `latitude` float NOT NULL,
  `stock` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;''')

    service_0.db.engine.execute('''INSERT INTO `stocks` VALUES 
(1,'Choa Chu Kang CC', 1.38140, 103.75161, 100),
(2,'Woodland CC', 1.43983, 103.78824, 195),
(3,'Tampines Central CC', 1.35310, 103.94036, 75),
(4,'Punggol Park CC', 1.37814, 103.89633, 200),
(5,'Carinhill CC', 1.31044, 103.83925, 100);''')

    return service_0.app.test_client()