from src.reporting import sales_reporting,specific_day_sales_reporting

if __name__ == '__main__':
    try:
        sales_reporting(10)
        #specific_day_sales_reporting()
    except Exception as e:
        print(e)