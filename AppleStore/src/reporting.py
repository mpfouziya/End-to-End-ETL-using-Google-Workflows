from pathlib import Path
from datetime import date, timedelta
import datetime as DT

from google.api_core.exceptions import NotFound
from src.utils.apple_store import AppleStore
from src.utils.bigquery import BigQuery

apple_store = AppleStore()
bq = BigQuery()

sales_ddl_query_file = Path(__file__).parent / 'sql' / 'sales_ddl.sql'
finance_ddl_query_file = Path(__file__).parent / 'sql' / 'finance_ddl.sql'

def sales_reporting(days):
    today = DT.date.today()
    yesterday = today - DT.timedelta(days=1)
    delta = timedelta(days=1)
    try:
        bq.run_query(f'DELETE FROM apple_store.sales_data WHERE begin_date >= CURRENT_DATE("Asia/Riyadh") - {days}')
        start_date = today - DT.timedelta(days=days)

    except NotFound:
        bq.run_query(sales_ddl_query_file.read_text())
        start_date = date(2024, 10, 1)

    while start_date <= yesterday:
        print(start_date)
        try:
            df_ios = apple_store.fetch_sales_report(date=start_date)
            bq.upload_dataframe(df_ios, 'apple_store', 'sales_data')
            print(df_ios)
            start_date += delta
        except Exception as e:
            print(e)
            start_date += delta


def finance_reporting():
    today = DT.date.today()
    yesterday = today - DT.timedelta(days=1)
    try:
        bq.run_query('DELETE FROM apple_store.finance_data WHERE date >= CURRENT_DATE("Asia/Riyadh") - 10')
        start_date = today - DT.timedelta(days=10)

    except NotFound:
        bq.run_query(finance_ddl_query_file.read_text())
        start_date = date(2022, 10, 1)

    df_ios = apple_store.get_finance_data(start_date)
    print(df_ios)
    bq.upload_dataframe(df_ios, 'apple_store', 'finance_data')

def specific_day_sales_reporting():
    start_date = date(2023, 7, 26)
    last_date = date(2023, 7, 26)
    delta = timedelta(days=1)
    while start_date <= last_date:
        print(start_date)
        try:
            df_ios = apple_store.get_sales_data(start_date)
            print(df_ios)
            bq.upload_dataframe(df_ios, 'apple_store', 'sales_data')
            start_date += delta
        except Exception as e:
            start_date += delta


def specific_txt_reporting():
    df_ios = apple_store.get_specific_data()
    bq.upload_dataframe(df_ios, 'apple_store', 'sales_data')

