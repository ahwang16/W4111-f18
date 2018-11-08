schema.sql

CREATE TABLE `Appearances` (
  `yearID` varchar(6) NOT NULL,
  `teamID` varchar(8) NOT NULL,
  `lgID` text,
  `playerID` varchar(12) NOT NULL,
  `G_all` text,
  `GS` text,
  `G_batting` text,
  `G_defense` text,
  `G_p` text,
  `G_c` text,
  `G_1b` text,
  `G_2b` text,
  `G_3b` text,
  `G_ss` text,
  `G_lf` text,
  `G_cf` text,
  `G_rf` text,
  `G_of` text,
  `G_dh` text,
  `G_ph` text,
  `G_pr` text,
  PRIMARY KEY (`playerID`,`teamID`,`yearID`),
  KEY `apptoteams_idx` (`teamID`,`yearID`),
  CONSTRAINT `apptopeople` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerid`),
  CONSTRAINT `apptoteams` FOREIGN KEY (`teamID`, `yearID`) REFERENCES `teams` (`teamid`, `yearid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `Batting` (
  `playerID` varchar(12) NOT NULL,
  `yearID` varchar(6) NOT NULL,
  `stint` int(11) NOT NULL,
  `teamID` varchar(8) NOT NULL,
  `lgID` text,
  `G` text,
  `AB` text,
  `R` text,
  `H` text,
  `2B` text,
  `3B` text,
  `HR` text,
  `RBI` text,
  `SB` text,
  `CS` text,
  `BB` text,
  `SO` text,
  `IBB` text,
  `HBP` text,
  `SH` text,
  `SF` text,
  `GIDP` text,
  PRIMARY KEY (`playerID`,`teamID`,`yearID`,`stint`),
  KEY `battingtoteams_idx` (`teamID`,`yearID`),
  CONSTRAINT `battingtopeople` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerid`),
  CONSTRAINT `battingtoteams` FOREIGN KEY (`teamID`, `yearID`) REFERENCES `teams` (`teamid`, `yearid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `Fielding` (
  `playerID` varchar(12) NOT NULL,
  `yearID` varchar(6) NOT NULL,
  `stint` int(11) NOT NULL,
  `teamID` varchar(8) NOT NULL,
  `lgID` varchar(2) DEFAULT NULL,
  `POS` varchar(6) NOT NULL,
  `G` text,
  `GS` text,
  `InnOuts` text,
  `PO` int(11) DEFAULT NULL,
  `A` int(11) DEFAULT NULL,
  `E` text,
  `DP` int(11) DEFAULT NULL,
  `PB` text,
  `WP` text,
  `SB` text,
  `CS` text,
  `ZR` text,
  PRIMARY KEY (`playerID`,`teamID`,`yearID`,`POS`,`stint`),
  KEY `fieldingtoteams_idx` (`teamID`,`yearID`),
  CONSTRAINT `fieldingtopeople` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerid`),
  CONSTRAINT `fieldingtoteams` FOREIGN KEY (`teamID`, `yearID`) REFERENCES `teams` (`teamid`, `yearid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE `Managers` (
  `playerID` varchar(12) NOT NULL,
  `yearID` varchar(6) NOT NULL,
  `teamID` varchar(6) NOT NULL,
  `lgID` text,
  `inseason` varchar(6) NOT NULL,
  `G` text,
  `W` text,
  `L` text,
  `rank` text,
  `plyrMgr` text,
  PRIMARY KEY (`playerID`,`teamID`,`yearID`,`inseason`),
  KEY `managerstoteams_idx` (`teamID`,`yearID`),
  CONSTRAINT `managerstopeople` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerid`),
  CONSTRAINT `managerstoteams` FOREIGN KEY (`teamID`, `yearID`) REFERENCES `teams` (`teamid`, `yearid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE `People` (
  `playerID` varchar(12) NOT NULL,
  `birthYear` text,
  `birthMonth` text,
  `birthDay` text,
  `birthCountry` text,
  `birthState` text,
  `birthCity` text,
  `deathYear` text,
  `deathMonth` text,
  `deathDay` text,
  `deathCountry` text,
  `deathState` text,
  `deathCity` text,
  `nameFirst` text,
  `nameLast` text,
  `nameGiven` text,
  `weight` text,
  `height` text,
  `bats` text,
  `throws` text,
  `debut` text,
  `finalGame` text,
  `retroID` text,
  `bbrefID` text,
  PRIMARY KEY (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `Teams` (
  `yearID` varchar(6) NOT NULL,
  `lgID` text,
  `teamID` varchar(8) NOT NULL,
  `franchID` text,
  `divID` text,
  `Rank` text,
  `G` text,
  `Ghome` text,
  `W` text,
  `L` text,
  `DivWin` text,
  `WCWin` text,
  `LgWin` text,
  `WSWin` text,
  `R` text,
  `AB` text,
  `H` text,
  `2B` text,
  `3B` text,
  `HR` text,
  `BB` text,
  `SO` text,
  `SB` text,
  `CS` text,
  `HBP` text,
  `SF` text,
  `RA` text,
  `ER` text,
  `ERA` text,
  `CG` text,
  `SHO` text,
  `SV` text,
  `IPouts` text,
  `HA` text,
  `HRA` text,
  `BBA` text,
  `SOA` text,
  `E` text,
  `DP` text,
  `FP` text,
  `name` text,
  `park` text,
  `attendance` text,
  `BPF` text,
  `PPF` text,
  `teamIDBR` text,
  `teamIDlahman45` text,
  `teamIDretro` text,
  PRIMARY KEY (`teamID`,`yearID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


