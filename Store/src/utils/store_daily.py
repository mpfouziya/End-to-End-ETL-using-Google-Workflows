from pathlib import Path


class Store:
    def __init__(self):
        self.create_header_file = Path(__file__).parent.parent / 'sql' / 'CreateHeader.sql'

        self.header_file = Path(__file__).parent.parent / 'sql' / 'Header.sql'
        self.apple_store_query_file = Path(__file__).parent.parent / 'sql' / 'AppleStore.sql'
        self.google_play_query_file = Path(__file__).parent.parent / 'sql' / 'GooglePlay.sql'
        self.union_query_file = Path(__file__).parent.parent / 'sql' / 'Union.sql'

    def store_create(self) -> str:
        try:
            query = self.create_header_file.read_text()
            query += '\n'
            query += self.apple_store_query_file.read_text()
            query += '\n'
            query += self.google_play_query_file.read_text()
            query += '\n'
            query += self.union_query_file.read_text()
            print(query)
            return query

        except Exception as e:
            return f'events :{str(e)}'

    def get_store_data(self, days_to_delete):
        try:
            query = self.header_file.read_text().format(days_to_delete=days_to_delete)
            query += '\n'
            query += self.apple_store_query_file.read_text()
            query += '\n'
            query += self.google_play_query_file.read_text()
            query += '\n'
            query += self.union_query_file.read_text()
            print(query)
            return query

        except Exception as e:
            return f'events :{str(e)}'





