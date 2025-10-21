google_store_iap AS (

       SELECT 'Google Store'     source,
              'Android'          platform,
              Order_Charged_Date date,
              SKU_ID             sku,
              Product_ID         app_name,
              Country_of_Buyer   country_code,
              1                  units,
              Currency_of_Sale   customer_currency,
              Charged_Amount     customer_price,
              Charged_Amount*0.7 developer_proceeds

       FROM google_play_dt.p_Sales_gp
       WHERE Order_Charged_Date >= from_date
       AND Product_ID = google_app
       AND Financial_Status != 'Refund'

),

google_store_units AS (
       SELECT 'Google Store'        source,
              'Android'             platform,
              date,
              Package_Name          sku,
              Package_Name          app_name,
              Country               country_code,
              Daily_Device_Installs units,
              CAST(NULL AS STRING)  customer_currency,
              0.0                   customer_price,
              0.0                   developer_proceeds
       FROM google_play_dt.p_Installs_country_gp
       WHERE date >= from_date
       AND package_name = google_app
)