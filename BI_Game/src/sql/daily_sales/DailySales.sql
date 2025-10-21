DROP TABLE IF EXISTS `datastudio.daily_sales`;

CREATE TABLE `datastudio.daily_sales`
PARTITION BY order_date
AS (
SELECT tr.id AS order_id,
       tr.player_id,
       tr.asset_id,
       tr.type,
       SPLIT(tr.price, ' ')[OFFSET(0)] price,
       SPLIT(tr.price, ' ')[OFFSET(1)] currency,
       tr.status,
       tr.property,
       tr.property_before,
       tr.property_after,
       DATE(tr.created_at) AS order_date,
       tr.created_at AS order_created_at,
       tr.updated_at AS order_updated_at,
       tr.store_transaction_id,
       cs.username,
       cs.name,
       cs.email,
       cs.uid,
       cs.facebookId,
       cs.gmailId,
       cs.appleId,
       cs.accountType,
       cs.points,
       cs.grade,
       cs.coins,
       cs.coins_weekly,
       cs.coins_monthly,
       cs.lastOpen,
       cs.level,
       cs.levelPercent,
       cs.wins,
       cs.loses,
       cs.isVip,
       cs.active,
       cs.blocked,
       cs.created_at AS player_created_at,
       cs.updated_at AS player_updated_at,
       cs.seeks,
       cs.subscription_date,
       cs.gems,
       cs.gender,
       cs.birth_date
    FROM `whist-3ca02.game_data.transactions` tr
    LEFT JOIN `whist-3ca02.game_data.customers` cs
    ON tr.player_id = cs.id
    )