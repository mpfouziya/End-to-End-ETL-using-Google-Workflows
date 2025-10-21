WITH account_data AS (
  SELECT id,
       accountType,
       IF(facebookId IS NOT NULL OR accountType = 'Facebook','Facebook','-') AS has_facebook,
       IF(gmailId IS NOT NULL OR accountType = 'Gmail','Gmail','-') AS has_gmail,
       IF(appleId IS NOT NULL OR accountType = 'Apple','Apple','-') AS has_apple,
       IF(DATE(lastOpen)>=CURRENT_DATE('Asia/Riyadh') -7, id, NULL) d7_active,
       IF(DATE(lastOpen)>=CURRENT_DATE('Asia/Riyadh') -30, id, NULL) d30_active,
       IF(DATE(created_at)>=CURRENT_DATE('Asia/Riyadh') -7, id, NULL) d7_created,
       IF(DATE(created_at)>=CURRENT_DATE('Asia/Riyadh') -30, id, NULL) d30_created,

FROM `whist-3ca02.game_data.customers`
WHERE accountType!='test')

SELECT accountType,
       has_facebook,
       has_gmail,
       has_apple,
       COUNT(DISTINCT id) total_users,
       COUNT(DISTINCT d7_active) total_d7_users,
       COUNT(DISTINCT d30_active) total_d30_users,
       COUNT(DISTINCT d7_created) total_d7_created,
       COUNT(DISTINCT d30_created) total_d30_created,
       CURRENT_DATE() date
       FROM account_data
       GROUP BY accountType, has_facebook, has_gmail, has_apple

)