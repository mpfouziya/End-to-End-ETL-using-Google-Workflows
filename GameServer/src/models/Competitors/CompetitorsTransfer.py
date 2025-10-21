from pathlib import Path
from src.utils.game_data import GameData
from src.utils.bigquery import BigQuery

gd = GameData()
bq = BigQuery()

def competitors() -> str:
    try:
        query_file = Path(__file__).parent/'CompetitorsQuery.sql'
        query = query_file.read_text()
        data = gd.run_query(query)
        print(data.shape)
        data = data.astype({'id': 'Int32', 'competition_id': 'Int32','player_id': 'Int32',
                            'score': 'Int32', 'created_at':'datetime64[ns]', 'updated_at':'datetime64[ns]'})


        result = bq.upload_dataframe(data, 'game_data','competitors')

        print(f'competitors : {str(result)}')

    except Exception as err:
        print(f'competitors : {str(err)}')