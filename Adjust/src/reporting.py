from datetime import date, timedelta
from pathlib import Path
from google.api_core.exceptions import NotFound
import datetime as DT
import pandas as pd

from src.utils.adjust import Adjust
from src.utils.bigquery import BigQuery

ad = Adjust()
bq = BigQuery()

ad_mob_ddl_query_file = Path(__file__).parent / 'sql' / 'ad_mob_ddl.sql'

def reporting(start_date, end_date):
    try:
        cohort_data = ad.get_adjust_data(start_date, end_date)
        processed_data = ad.process_adjust_data(cohort_data, end_date)
        bq.upload_dataframe(cohort_data, 'adjust', 'cohorted_metrics')
        bq.upload_dataframe(processed_data, 'fact', 'cohorted_adjust')
    #
    except Exception as e:
        print(e.message)








