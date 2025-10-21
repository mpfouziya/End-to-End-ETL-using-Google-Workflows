from pathlib import Path


class GaEvent:
    def __init__(self):
        self.event_create_header_file = Path(__file__).parent.parent / 'sql' / 'EventCreateHeader.sql'

        self.event_header_file = Path(__file__).parent.parent / 'sql' / 'EventHeader.sql'
        self.event_query_file = Path(__file__).parent.parent / 'sql' / 'Event.sql'

 
    def event_create(self) -> str:
        try:        
            query = self.event_create_header_file.read_text()
            query += '\n'
            query += self.event_query_file.read_text()
            print(query)
            return query
    
        except Exception as e:
            return f'events :{str(e)}'

    def get_event_data(self, days_to_delete):
        try:        
            query = self.event_header_file.read_text().format(days_to_delete=days_to_delete)
            query += '\n'
            query += self.event_query_file.read_text()
            print(query)
            return query
        
        except Exception as e:
            return f'events :{str(e)}'

   

    

