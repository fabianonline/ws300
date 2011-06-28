CREATE TABLE `ws300` (
     `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
     `time` datetime NOT NULL,
     `s0_temp` decimal(4,2) DEFAULT NULL,
     `s0_humi` tinyint(3) unsigned DEFAULT NULL,
     `s0_status` tinyint(3) unsigned DEFAULT NULL,
     `s1_temp` decimal(4,2) DEFAULT NULL,
     `s1_humi` tinyint(3) unsigned DEFAULT NULL,
     `s1_status` tinyint(3) unsigned DEFAULT NULL,
     `s2_temp` decimal(4,2) DEFAULT NULL,
     `s2_humi` tinyint(3) unsigned DEFAULT NULL,
     `s2_status` tinyint(3) unsigned DEFAULT NULL,
     `s3_temp` decimal(4,2) DEFAULT NULL,
     `s3_humi` tinyint(3) unsigned DEFAULT NULL,
     `s3_status` tinyint(3) unsigned DEFAULT NULL,
     `s4_temp` decimal(4,2) DEFAULT NULL,
     `s4_humi` tinyint(3) unsigned DEFAULT NULL,
     `s4_status` tinyint(3) unsigned DEFAULT NULL,
     `s5_temp` decimal(4,2) DEFAULT NULL,
     `s5_humi` tinyint(3) unsigned DEFAULT NULL,
     `s5_status` tinyint(3) unsigned DEFAULT NULL,
     `s6_temp` decimal(4,2) DEFAULT NULL,
     `s6_humi` tinyint(3) unsigned DEFAULT NULL,
     `s6_status` tinyint(3) unsigned DEFAULT NULL,
     `s7_temp` decimal(4,2) DEFAULT NULL,
     `s7_humi` tinyint(3) unsigned DEFAULT NULL,
     `s7_status` tinyint(3) unsigned DEFAULT NULL,
     `s8_temp` decimal(4,2) DEFAULT NULL,
     `s8_humi` tinyint(3) unsigned DEFAULT NULL,
     `s8_status` tinyint(3) unsigned DEFAULT NULL,
     `s9_temp` decimal(4,2) DEFAULT NULL,
     `s9_humi` tinyint(3) unsigned DEFAULT NULL,
     `s9_status` tinyint(3) unsigned DEFAULT NULL,
     `pressure` smallint(5) unsigned DEFAULT NULL,
     `rain_abs` decimal(8,3) DEFAULT NULL,
     `rain_rel` decimal(8,3) DEFAULT NULL,
     `wind` decimal(4,1) DEFAULT NULL,
     `raw_data` binary(37) DEFAULT NULL,
     `raw_dev_data` binary(14) DEFAULT NULL,
     PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
