DECLARE from_date DEFAULT (SELECT CURRENT_DATE('Asia/Riyadh') - {days_to_delete});

DELETE FROM `fact.first_touch_event`
WHERE event_date >= from_date;

INSERT INTO `fact.first_touch_event`(