from pathlib import Path
from src.utils.game_data import GameData
from src.utils.bigquery import BigQuery

gd = GameData()
bq = BigQuery()

def competitions() -> str:
    try:
        query_file = Path(__file__).parent/'CompetitionsQuery.sql'
        query = query_file.read_text()
        data = gd.run_query(query)
        print(data.shape)
        data = data.astype({'id': 'Int64', 'name': 'object','status': 'object',
                            'active': 'object', 'sponsor_name': 'object', 'start_date': 'object',
                            'end_date': 'object', 'fees': 'int32', 'min_level': 'int32',
                            'conditions':'object','created_at':'datetime64[ns]', 'updated_at':'datetime64[ns]'})


        result = bq.upload_dataframe(data, 'game_data','competitions')

        print(f'competitions : {str(result)}')

    except Exception as err:
        print(f'competitions : {str(err)}')