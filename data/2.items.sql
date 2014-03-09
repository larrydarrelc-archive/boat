DROP TABLE IF EXISTS `items`;
CREATE TABLE `items` (
    `id` INTEGER NOT NULL,
    /* 0 is normal, 1 is warning */
    `status` INTEGER NOT NULL default 0,
    `data` VARCHAR(512) NOT NULL default "",
    `meta` VARCHAR(1024),

    `created_at` DATETIME default current_timestamp,
    `updated_at` DATETIME default current_timestamp
);

DROP TABLE IF EXISTS `logging`;
CREATE TABLE `logging` (
    `id` INTEGER PRIMARY KEY,
    `item_id` INTEGER NOT NULL,
    /* 0 is triggered, 1 is confirmed, 2 is disappeared */
    `status` INTEGER NOT NULL default 0,

    `triggered_at` DATETIME default NULL,
    `confirmed_at` DATETIME default NULL,
    `disappeared_at` DATETIME default NULL
);
