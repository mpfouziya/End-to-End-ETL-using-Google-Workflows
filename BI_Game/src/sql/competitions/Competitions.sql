DROP TABLE IF EXISTS `datastudio.competitions`;

CREATE TABLE `datastudio.competitions`
PARTITION BY start_date
AS (

SELECT 	cn.id competition_id,
    cn.name AS competition_name,
    cn.status,
    cn.active,
    cn.sponsor_name,
    DATE(SPLIT(cn.start_date, 'T')[OFFSET(0)]) start_date,
    DATE(SPLIT(cn.end_date, 'T')[OFFSET(0)]) end_date,
    cn.fees,
    cn.min_level,
    cn.conditions,
    cr.player_id,
    cr.score,
    cs.username,
    cs.name,
    cs.email

FROM `game_data.competitions` cn
LEFT JOIN `game_data.competitors` cr ON cn.id = cr.competition_id
LEFT JOIN `game_data.customers` cs ON cr.player_id = cs.id
)