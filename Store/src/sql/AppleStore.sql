WITH apple_store AS
(
       SELECT 'Apple Store' source,
              'IOS' platform,
              begin_date date,
              sku,
              IF(parent_identifier=' ', sku, parent_identifier) app_name,
              country_code,
              units,
              customer_currency,
              customer_price,
              developer_proceeds
       FROM apple_store.sales_data
       WHERE begin_date >= from_date
       AND product_type_identifier != '7'
       AND (parent_identifier = apple_app
           OR sku = apple_app)
),