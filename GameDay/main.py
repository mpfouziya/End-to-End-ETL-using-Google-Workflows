from src.reporting import reporting

if __name__ == '__main__':
    try:

        reporting(10)
    except Exception as e:
        print(e)