from src.utils.account_summary import ActSummary
from src.utils.daily_sales import DailySales
from src.utils.competitions import Competitions
from src.utils.bigquery import BigQuery


act_summary = ActSummary()
sales = DailySales()
competition = Competitions()
bq = BigQuery()

def reporting():

#Creating sales data
    try:
        query = sales.create()
        bq.run_query(query)

    except Exception as e:
        print(e.message)


#Creating competitions data
    try:
        query = competition.create()
        bq.run_query(query)

    except Exception as e:
        print(e.message)


#Account Summary details
    try:
        query = act_summary .get_data()
        bq.run_query(query)


    except Exception as e:
        if 'Not found' in e.message:
            query = act_summary .create()
            bq.run_query(query)
        else:
            print(e.message)




    




