from pathlib import Path


class GameDay:
    def __init__(self):
        self.create_header_file = Path(__file__).parent.parent / 'sql' / 'CreateHeader.sql'

        self.header_file = Path(__file__).parent.parent / 'sql' / 'Header.sql'
        self.game_day_query_file = Path(__file__).parent.parent / 'sql' / 'GameDay.sql'


    def game_day_create(self) -> str:
        try:
            query = self.create_header_file.read_text()
            query += '\n'
            query += self.game_day_query_file.read_text()
            print(query)
            return query

        except Exception as e:
            return f'events :{str(e)}'

    def get_game_day_data(self, days_to_delete):
        try:
            query = self.header_file.read_text().format(days_to_delete=days_to_delete)
            query += '\n'
            query += self.game_day_query_file.read_text()
            print(query)
            return query

        except Exception as e:
            return f'events :{str(e)}'





