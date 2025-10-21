WITH event_data AS (
SELECT DATE(TIMESTAMP_MICROS(event_timestamp), 'Asia/Riyadh') AS event_date,
       DATETIME(TIMESTAMP_MICROS(event_timestamp), 'Asia/Riyadh') AS event_datetime,
       DATE(TIMESTAMP_MICROS(user_first_touch_timestamp), 'Asia/Riyadh') AS first_touch_date,
       event_timestamp,
       user_first_touch_timestamp,
       user_pseudo_id,
       user_id,
       event_name,
       device.language                     AS device_language,
       device.mobile_brand_name            AS device_brand_name,
       device.mobile_model_name            AS device_model_name,
       device.mobile_os_hardware_model     AS device_os_hardware_model,
       device.operating_system             AS device_operating_system,
       device.operating_system_version     AS device_operating_system_version,
       device.vendor_id                    AS device_vendor_id,
       device.is_limited_ad_tracking       AS is_limited_ad_tracking,
       geo.continent                       AS continent,
       geo.country                         AS event_country,
       geo.region                          AS region,
       geo.city                            AS city,
       geo.sub_continent                   AS sub_continent,
       app_info.id                         AS app_id,
       app_info.version                    AS app_version,
       app_info.install_source             AS install_source,
       traffic_source.name                 AS traffic_source_name,
       traffic_source.medium               AS traffic_source_medium,
       traffic_source.source               AS traffic_source_source,
       event_value_in_usd,
       LOWER(platform) AS platform,
       (SELECT value.int_value FROM UNNEST(event_params) WHERE key = "ga_session_id") AS session_id,
       (SELECT value.int_value FROM UNNEST(event_params) WHERE key = "ga_session_number") AS session_number,
       (SELECT value.string_value FROM UNNEST(event_params) WHERE key = "firebase_screen_class") AS firebase_screen_class,
       (SELECT value.string_value FROM UNNEST(event_params) WHERE key = "firebase_previous_class") AS firebase_previous_class,
       (SELECT value.int_value FROM UNNEST(event_params) WHERE key = "engagement_time_msec") AS engagement_time_msec,
       (SELECT value.int_value FROM UNNEST(event_params) WHERE key = "entrances") AS entrances,
       (SELECT value.int_value FROM UNNEST(event_params) WHERE key = "previous_first_open_count") AS previous_first_open_count,
       (SELECT value.int_value FROM UNNEST(event_params) WHERE key = "update_with_analytics") AS update_with_analytics,
       (SELECT value.string_value FROM UNNEST(event_params) WHERE key = "previous_app_version") AS previous_app_version,
       (SELECT value.string_value FROM UNNEST(event_params) WHERE key = "currency") AS currency,
       (SELECT value.string_value FROM UNNEST(event_params) WHERE key = "message_name") AS message_name,
       (SELECT value.string_value FROM UNNEST(event_params) WHERE key = "message_type") AS message_type,
       (SELECT value.int_value FROM UNNEST(event_params) WHERE key = "quantity") AS quantity,
       (SELECT value.int_value FROM UNNEST(event_params) WHERE key = "validated") AS validated,
       (SELECT value.string_value FROM UNNEST(event_params) WHERE key = "product_id") AS product_id,
       (SELECT value.string_value FROM UNNEST(event_params) WHERE key = "product_name") AS product_name,
       (SELECT value.string_value FROM UNNEST(event_params) WHERE key = "term") AS term,
       FROM `<GCP_PROJECT_ID>.analytics_232931779.events_*`
       WHERE   _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', from_date)),

event AS (SELECT *,
                 DATETIME_DIFF(event_datetime ,LAG(event_datetime, 1)OVER (PARTITION BY session_id ORDER BY event_datetime),SECOND) event_time_seconds
FROM event_data),

country_code AS (
  SELECT country_name,
         alpha_2_code AS country
  FROM dim.country_codes
)

SELECT * FROM event
LEFT JOIN country_code ON event.event_country = country_code.country_name
LEFT JOIN dim.date d ON event.event_date = d.date
)