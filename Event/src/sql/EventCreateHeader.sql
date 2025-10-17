DECLARE from_date DEFAULT (SELECT DATE('2024-10-01'));

DROP TABLE IF EXISTS fact.event;

CREATE TABLE fact.event
PARTITION BY event_date
CLUSTER BY event_name
AS (