from pathlib import Path


class Competitions:
    def __init__(self):

        self.competitions_query_file = Path(__file__).parent.parent / 'sql' / 'competitions' / 'Competitions.sql'


    def create(self) -> str:
        try:
            query = self.competitions_query_file .read_text()
            print(query)
            return query

        except Exception as e:
            return f'events :{str(e)}'







