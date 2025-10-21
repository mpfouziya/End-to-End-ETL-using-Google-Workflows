DECLARE from_date DEFAULT (SELECT CURRENT_DATE('Asia/Riyadh') - {days_to_delete});
DECLARE apple_app STRING DEFAULT <APPLE_APP_ID>;
DECLARE google_app STRING DEFAULT <GOOGLE_APP_ID>>;


DELETE FROM `fact.store`
WHERE date >= from_date;


