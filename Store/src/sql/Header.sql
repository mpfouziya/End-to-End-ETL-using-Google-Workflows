DECLARE from_date DEFAULT (SELECT CURRENT_DATE('Asia/Riyadh') - {days_to_delete});
DECLARE apple_app STRING DEFAULT '123456789';
DECLARE google_app STRING DEFAULT 'com.whist.whistapp';


DELETE FROM `fact.store`
WHERE date >= from_date;


