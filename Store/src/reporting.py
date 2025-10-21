from src.utils.store_daily import Store
from src.utils.bigquery import BigQuery
import requests

from src.config import API_KEY

store_daily = Store()
bq = BigQuery()


def convert_currency():
    url= f'http://data.fixer.io/api/latest?access_key={API_KEY}'

    response = requests.get(
                  url)
    result = response.json()['rates']

    return result


def get_exchange_rate(currency_list):
    print(currency_list)
    all_exchange_rate = convert_currency()
    exchange_rate_usd = all_exchange_rate['USD']
    exchange_rate_dict = {}
    try:
        for each in currency_list:
            if each != None:
                exchange_rate = all_exchange_rate[each]
                exchange_rate_dict[each] = exchange_rate_usd/exchange_rate
        exchange_rate_dict['USD'] = all_exchange_rate['USD']/exchange_rate_usd
        exchange_rate_dict[None] = 0.0
    except Exception as e:
        print('convert_currency error')
        exchange_rate_dict = {None: 0.0, 'SAR': 0.266667, 'AED': 0.27229, 'EGP': 0.032361, 'KRW': 0.000769,'CAD': 0.74,
                              'IQD': 0.00077, 'QAR': 0.27472, 'GBP': 1.22, 'MYR': 0.21, 'ILS': 0.26, 'USD': 1}
    print(exchange_rate_dict)
    return exchange_rate_dict


def process_and_upload(query) :
    df = bq.run_query(query)
    currency_list = df['customer_currency'].unique().tolist()
    exchange_rate_dict = get_exchange_rate(currency_list)

    df['usd_exchange_rate'] = df['customer_currency'].map(exchange_rate_dict)
    df['usd_customer_price'] = df['customer_price'] * df['usd_exchange_rate']
    df['usd_developer_proceeds'] = df['developer_proceeds'] * df['usd_exchange_rate']
    df['usd_revenue'] = df['usd_customer_price'] * df['units']
    df['usd_total_dev_proceeds'] = df['usd_developer_proceeds'] * df['units']

    bq.upload_dataframe(df, 'fact', 'store')
    print(df)

def reporting(days):

    try:
        query = store_daily.get_store_data(days)
        process_and_upload(query)

    except Exception as e:
        if 'Not found' in e.message:
            query = store_daily.store_create()
            process_and_upload(query)
        else:
            print(e.message)


    




