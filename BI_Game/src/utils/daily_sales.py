from pathlib import Path


class DailySales:
    def __init__(self):

        self.daily_sales_query_file = Path(__file__).parent.parent / 'sql' / 'daily_sales' / 'DailySales.sql'


    def create(self) -> str:
        try:
            query = self.daily_sales_query_file.read_text()
            print(query)
            return query

        except Exception as e:
            return f'events :{str(e)}'







