from datetime import date, timedelta
from pathlib import Path
from google.api_core.exceptions import NotFound
import datetime as DT
import pandas as pd

from src.utils.ad_mob import AdMob
from src.utils.bigquery import BigQuery

am = AdMob()
bq = BigQuery()

ad_mob_ddl_query_file = Path(__file__).parent / 'sql' / 'ad_mob_ddl.sql'

def reporting(days):
    today = DT.date.today()
    yesterday = today - DT.timedelta(days=1)

    try:
        bq.run_query(f'DELETE FROM ad_mob.earnings_data WHERE reporting_date >= CURRENT_DATE("Asia/Riyadh") - {days}')
        start_date = today - DT.timedelta(days=days)
    #
    except NotFound:
        bq.run_query(ad_mob_ddl_query_file.read_text())
        start_date = date(2024, 10, 1)

    try:
        ad_mob_list = am.fetch_admob_earnings(start_date, yesterday)
        df_ad_mob = pd.DataFrame(ad_mob_list)
        bq.upload_dataframe(df_ad_mob, 'ad_mob', 'earnings_data')
        print(df_ad_mob)

    except Exception as e:
        print(e)






