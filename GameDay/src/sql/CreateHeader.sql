DECLARE from_date DEFAULT (SELECT DATE('2024-10-01'));

DROP TABLE IF EXISTS datastudio.game_day;

CREATE TABLE datastudio.game_day
PARTITION BY date
AS (