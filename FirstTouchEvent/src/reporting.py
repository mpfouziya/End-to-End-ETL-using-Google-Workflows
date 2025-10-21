from src.utils.ga_event import GaEvent
from src.utils.bigquery import BigQuery

ga_event = GaEvent()
bq = BigQuery()

def reporting():
    try:
        query = ga_event.get_event_data(10)
        bq.run_query(query)

    except Exception as e:
        if 'Not found' in e.message:
            query = ga_event.event_create()
            bq.run_query(query)
        else:
            print(e.message)

    




