DECLARE from_date DEFAULT (SELECT DATE('2024-10-01'));

DROP TABLE IF EXISTS fact.first_touch_event;

CREATE TABLE fact.first_touch_event
PARTITION BY first_touch_date
CLUSTER BY event_name
AS (