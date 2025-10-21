from pathlib import Path
from src.utils.game_data import GameData
from src.utils.bigquery import BigQuery

gd = GameData()
bq = BigQuery()

def friends() -> str:
    try:
        query_file = Path(__file__).parent/'FriendsQuery.sql'
        query = query_file.read_text()
        data = gd.run_query(query)
        print(data.shape)
        data = data.astype({'id': 'Int64', 'user_id': 'Int32', 'friend_id': 'Int32','status': 'object', 'created_at':'datetime64[ns]', 'updated_at':'datetime64[ns]'})

        result = bq.upload_dataframe(data, 'game_data','friends')
        print(f'friends : {str(result)}')
        gd.close_tunnel()

    except Exception as err:
        print(f'friends : {str(err)}')