from src.utils.game_day import GameDay
from src.utils.bigquery import BigQuery


game_day = GameDay()
bq = BigQuery()

def reporting(days):
    try:
        query = game_day.get_game_day_data(days)
        bq.run_query(query)


    except Exception as e:
        if 'Not found' in e.message:
            query = game_day.game_day_create()
            bq.run_query(query)
        else:
            print(e.message)

    




