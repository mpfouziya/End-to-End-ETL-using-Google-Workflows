DECLARE from_date DEFAULT (SELECT DATE('2023-07-14'));
DECLARE apple_app STRING DEFAULT '123456789';
DECLARE google_app STRING DEFAULT 'com.whist.whistapp';


DROP TABLE IF EXISTS fact.store;

CREATE TABLE fact.store
--PARTITION BY date
(   source                    STRING,
    platform                  STRING,
    date                      DATE,
    sku                       STRING,
    app_name                  STRING,
    country_code              STRING,
    units                     INTEGER,
    customer_currency         STRING,
    customer_price            FLOAT64,
    developer_proceeds        FLOAT64,
    usd_exchange_rate         FLOAT64,
    usd_customer_price        FLOAT64,
    usd_developer_proceeds    FLOAT64,
    usd_revenue               FLOAT64,
    usd_total_dev_proceeds    FLOAT64
);