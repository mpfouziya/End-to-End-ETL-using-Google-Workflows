DECLARE from_date DEFAULT (SELECT CURRENT_DATE('Asia/Riyadh') - {days_to_delete});

DELETE FROM `datastudio.game_day`
WHERE date >= from_date;

INSERT INTO `datastudio.game_day`(