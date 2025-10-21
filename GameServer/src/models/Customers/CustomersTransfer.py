from pathlib import Path
from src.utils.game_data import GameData
from src.utils.bigquery import BigQuery

gd = GameData()
bq = BigQuery()

def customers() -> str:
    try:
        query_file = Path(__file__).parent/'CustomersQuery.sql'
        query = query_file.read_text()
        data = gd.run_query(query)
        print(data.shape)
        data = data.astype({'id': 'Int64', 'username': 'object', 'name':'object', 'email':'object' , 'uid':'object', 'facebookId':'object',
                            'gmailId':'object', 'appleId':'object', 'accountType':'object', 'messagingToken':'object', 'points':'int64', 'grade':'int32',
                            'coins':'int32', 'coins_weekly':'int32', 'coins_monthly':'int32', 'lastOpen':'datetime64[ns]', 'level':'int32',
                            'levelPercent':'int32', 'wins': 'int32', 'loses': 'Int32', 'isVip':'object', 'active':'object', 'blocked':'object',
                            'remember_token':'object', 'created_at': 'datetime64[ns]', 'updated_at':'datetime64[ns]', 'seeks':'int32',
                            'subscription_date':'object', 'gems':'int32', 'gender':'object','birth_date':'object'})


        result = bq.upload_dataframe(data, 'game_data','customers')

        print(f'customers : {str(result)}')

    except Exception as err:
        print(f'customers : {str(err)}')