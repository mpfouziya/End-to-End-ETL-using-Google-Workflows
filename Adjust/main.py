from src.reporting import reporting
from datetime import datetime, timedelta

if __name__ == '__main__':
    try:
        start_date = '2024-11-20'
        end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        reporting(start_date, end_date)
    except Exception as e:
        print(e)