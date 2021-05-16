/* database */
CREATE DATABASE IF NOT EXISTS athens;
USE athens;

/* members table */
CREATE TABLE IF NOT EXISTS members (
	userID VARCHAR(25) NOT NULL,
	username TEXT NOT NULL,
	name TEXT NOT NULL,
	keyrole VARCHAR(10) NOT NUll,
	PRIMARY KEY (userID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* tasks table */
CREATE TABLE IF NOT EXISTS tasks (
	taskID INT(10) NOT NULL AUTO_INCREMENT,
	requestLink TEXT NOT NULL,
	requestedDate DATETIME NOT NULL,
	content TEXT NOT NULL,
	status VARCHAR(10) NOT NULL,
	requesterID VARCHAR(25) NOT NULL,
	PRIMARY KEY (taskID),
	CONSTRAINT requester FOREIGN KEY (requesterID) 
		REFERENCES members(userID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* posts table */
CREATE TABLE IF NOT EXISTS posts (
	taskID INT(10) NOT NULL,
	completeLink TEXT NOT NULL,
	completedDate DATETIME NOT NULL,
	completerID VARCHAR(25) NOT NULL,
	PRIMARY KEY (taskID),
	CONSTRAINT completer FOREIGN KEY (completerID)
		REFERENCES members(userID)
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT postTask FOREIGN KEY (taskID)
		REFERENCES tasks(taskID)
		ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* controller table */
CREATE TABLE IF NOT EXISTS trackers (
    taskID INT(10) NOT NULL,
    link TEXT NOT NULL,
    PRIMARY KEY (taskID),
    CONSTRAINT tracker_link FOREIGN KEY (taskID)
        REFERENCES tasks(taskID)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
