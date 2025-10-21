WITH store AS (
SELECT source,
       'N/A' media_source,
       date,
       DATE('2020-01-01') event_date,
       LOWER(platform) platform,
       'N/A' campaign_name,
       'N/A' adgroup_name,
       'N/A' ad_name,
       country_code AS country,
       SUM(IF(app_name = sku, units,0)) installs,
       SUM(IF(app_name != sku,units,0)) orders,
       SUM(usd_revenue) AS revenue,
       SUM(usd_total_dev_proceeds) AS developer_proceeds,
       0 clicks,
       0 impressions,
       0 conversions,
       0 spend,
       0 users,
       0 new_users
FROM fact.store
WHERE date >= from_date
GROUP BY 1,2,3,4,5,6,7,8,9
),

--ads AS (
--SELECT source,
--       'N/A' media_source,
--       date,
--       DATE('2020-01-01') event_date,
--       LOWER(platform) platform,
--       campaign_name,
--       adgroup_name,
--       ad_name,
--       'N/A' event_name,
--       country,
--       0 installs,
--       0 orders,
--       0 revenue,
--       0 developer_proceeds,
--       SUM(clicks) clicks,
--       SUM(impressions) impressions,
--       SUM(conversions) conversions,
--       sum(spend) spend,
--       0 users,
--       0 new_users
--FROM fact.ads
--WHERE date >= from_date
--GROUP BY 1,2,3,4,5,6,7,8,9,10,11
--
--),

mediation AS (
SELECT 'Ad Mob' source,
       ad_source AS media_source,
       reporting_date AS date,
       DATE('2020-01-01') event_date,
       LOWER(platform) platform,
       'N/A' campaign_name,
       'N/A' adgroup_name,
       'N/A' ad_name,
       country_code AS country,
       0 installs,
       0 orders,
       sum(ad_revenue) revenue,
       sum(ad_revenue) developer_proceeds,
       0 clicks,
       0 impressions,
       0 conversions,
       0 spend,
       0 users,
       0 new_users
FROM ad_mob.earnings_data
WHERE reporting_date >= from_date
GROUP BY 1,2,3,4,5,6,7,8,9,10,11

),

event AS (
SELECT 'GA' source,
       'N/A' media_source,
       event_date date,
       first_touch_date,
       LOWER(platform) platform,
       'N/A' campaign_name,
       'N/A' adgroup_name,
       'N/A' ad_name,
       country,
       0 installs,
       0 orders,
       0 revenue,
       0 developer_proceeds,
       0 clicks,
       0 impressions,
       0 conversions,
       0 spend,
       COUNT(DISTINCT(IF(event_name IN('first_open','session_start'), user_pseudo_id,null))) users,
       COUNT(DISTINCT(IF(event_name='first_open', user_pseudo_id,null))) new_users
FROM fact.event
WHERE event_date >= from_date
GROUP BY 1,2,3,4,5,6,7,8,9

),

adjust AS (
SELECT 'Adjust' AS source,
       ad_network AS media_source,
       DATE(install_date) date,
       event_date,
       platform,
       campaign_id AS campaign_name,
       adgroup adgroup_name,
       creative ad_name,
       country,
       SUM(CAST(cohort_users AS NUMERIC)) AS installs,
       0 AS orders,
       SUM(iap_revenue)+ SUM(ads_revenue) AS revenue,
       0 developer_proceeds,
       SUM(IF(days_since_install=0,clicks,0)) clicks,
       SUM(IF(days_since_install=0,impressions,0)) impressions,
       0 AS conversions,
       SUM(ad_spend) spend,
       0 users,
       0 new_users

FROM fact.cohorted_adjust
WHERE install_date >= from_date
GROUP BY 1,2,3,4,5,6,7,8,9
),

--af_agg AS (
--SELECT CASE WHEN media_source_pid = 'googleadwords_int' THEN 'Google Ads'
--            WHEN media_source_pid = 'bytedanceglobal_int' THEN 'Tiktok Ads'
--            ELSE media_source_pid END AS source,
--       CONCAT('AppsFlyer af_agg') media_source,
--       date,
--       CAST(NULL AS DATE) event_date,
--       platform,
--       campaign_c campaign_name,
--       CAST(NULL AS STRING) adgroup_name,
--       CAST(NULL AS STRING) ad_name,
--       CAST(NULL AS STRING) event_name,
--       country,
--       installs,
--       NULL AS orders,
--       NULL AS revenue,
----       af_purchase_event_counter AS orders,
----       af_purchase_sales_in_usd AS revenue,
--       0 developer_proceeds,
--       0 clicks,
--       0 impressions,
--       total_revenue AS conversions,
--       0 spend,
--       0 users,
--       0 new_users
--
--FROM appsflyer.agg_data
--WHERE date >= from_date
--),

--skan_agg AS (
--SELECT CASE WHEN media_source_pid = 'googleadwords_int' THEN 'Google Ads'
--            WHEN media_source_pid = 'bytedanceglobal_int' THEN 'Tiktok Ads'
--            ELSE media_source_pid END AS source,
--       CONCAT('AppsFlyer skan_agg') media_source,
--       date,
--       DATE_ADD(date,INTERVAL 2 DAY) event_date,
--       platform,
--       campaign_c campaign_name,
--       adset adgroup_name,
--       CAST(ad AS STRING) ad_name,
--       CAST(NULL AS STRING) event_name,
--       country,
--       installs,
--       NULL AS orders,
--       total_revenue AS revenue,
--       0 developer_proceeds,
--       0 clicks,
--       0 impressions,
--       total_revenue AS conversions,
--       0 spend,
--       0 users,
--       0 new_users
--
--FROM appsflyer.skan_agg
--WHERE date >= from_date
--AND media_source_pid!='organic'
--),

game_day AS (
  SELECT * FROM store UNION ALL
  --SELECT * FROM ads UNION ALL
  SELECT * FROM mediation UNION ALL
  SELECT * FROM event UNION ALL
  SELECT * FROM adjust --UNION ALL
  --SELECT * FROM af_agg UNION ALL
  --SELECT * FROM skan_agg
)

SELECT
    source,
    media_source,
    gd.date,
    event_date,
    platform,
    campaign_name,
    adgroup_name,
    ad_name,
    country,
    installs,
    orders,
    revenue,
    developer_proceeds,
    clicks,
    impressions,
    conversions,
    spend,
    users,
    new_users,
    week_range
FROM game_day gd
LEFT JOIN dim.date d ON gd.date=d.date
)