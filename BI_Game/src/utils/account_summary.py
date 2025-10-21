from pathlib import Path


class ActSummary:
    def __init__(self):
        self.create_header_file = Path(__file__).parent.parent / 'sql' / 'account_summary' / 'CreateHeader.sql'

        self.header_file = Path(__file__).parent.parent / 'sql' / 'account_summary' / 'Header.sql'
        self.account_type_summary_query_file = Path(__file__).parent.parent / 'sql' / 'account_summary' / 'AccountTypeSummary.sql'


    def create(self) -> str:
        try:
            query = self.create_header_file.read_text()
            query += '\n'
            query += self.account_type_summary_query_file.read_text()
            print(query)
            return query

        except Exception as e:
            return f'events :{str(e)}'

    def get_data(self):
        try:
            query = self.header_file.read_text()
            query += '\n'
            query += self.account_type_summary_query_file.read_text()
            print(query)
            return query

        except Exception as e:
            return f'events :{str(e)}'





