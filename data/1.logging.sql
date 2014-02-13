DROP TABLE IF EXISTS `logging`;
CREATE TABLE `logging` (
    `id` INTEGER PRIMARY KEY,
    `message` VARCHAR(5000) NOT NULL,
    `solved` INTEGER default 0,
    `timestamp` DATETIME default current_timestamp
);
