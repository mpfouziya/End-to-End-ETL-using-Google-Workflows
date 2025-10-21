WITH first_touch AS (
SELECT
    event_date,
    first_touch_date,
    user_pseudo_id,
    user_id,
    event_name,
    platform,
    app_version,
    country,
    session_id,
    session_number,
    currency,
    quantity,
    product_name
  FROM fact.event
  WHERE event_date>= from_date)

SELECT * FROM first_touch
LEFT JOIN dim.date d ON first_touch.first_touch_date = d.date
)



