from pathlib import Path
from src.utils.game_data import GameData
from src.utils.bigquery import BigQuery

gd = GameData()
bq = BigQuery()

def transactions() -> str:
    try:
        query_file = Path(__file__).parent/'TransactionsQuery.sql'
        query = query_file.read_text()
        data = gd.run_query(query)
        print(data.shape)
        data = data.astype({'id': 'Int64', 'player_id': 'Int32','asset_id': 'Int32', 'type': 'object',
                            'price': 'object', 'status':'object', 'property':'object', 'property_before':'object',
                            'property_after':'object','created_at':'datetime64[ns]', 'updated_at':'datetime64[ns]',
                            'store_transaction_id':'object'})


        result = bq.upload_dataframe(data, 'game_data','transactions')

        print(f'transactions : {str(result)}')

    except Exception as err:
        print(f'transactions : {str(err)}')