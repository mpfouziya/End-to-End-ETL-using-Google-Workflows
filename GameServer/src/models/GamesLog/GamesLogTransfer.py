from pathlib import Path
from src.utils.game_data import GameData
from src.utils.bigquery import BigQuery

gd = GameData()
bq = BigQuery()

def games_log() -> str:
    try:
        query_file = Path(__file__).parent/'GamesLogQuery.sql'
        query = query_file.read_text()
        data = gd.run_query(query)
        print(data.shape)
        data = data.astype({'id': 'Int64', 'game_id': 'object',
                            'game_type': 'object', 'created_at':'datetime64[ns]', 'updated_at':'datetime64[ns]'})


        result = bq.upload_dataframe(data, 'game_data','games_log')

        print(f'games_log : {str(result)}')

    except Exception as err:
        print(f'games_log : {str(err)}')