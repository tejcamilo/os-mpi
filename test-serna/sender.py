import socket
import os
from dotenv import load_dotenv
from tradingview_ta import TA_Handler, Interval

load_dotenv()  # take environment variables from .env.
source_ip = os.getenv('SOURCE_IP')
dest_ip = os.getenv('DESTINATION_IP')
port = int(os.getenv('PORT'))

class Screener():

    def __init__(self, symbol, screener, exchange):
        self.symbol = symbol
        self.screener = screener
        self.exchange = exchange
        self.interval = None
        self.data = None
    
    def detailed_search(self):
        interval_mapping = {
            "1m": Interval.INTERVAL_1_MINUTE,
            "5m": Interval.INTERVAL_5_MINUTES,
            "15m": Interval.INTERVAL_15_MINUTES,
            "30m": Interval.INTERVAL_30_MINUTES,
            "1h": Interval.INTERVAL_1_HOUR,
            "2h": Interval.INTERVAL_2_HOURS,
            "4h": Interval.INTERVAL_4_HOURS,
            "1d": Interval.INTERVAL_1_DAY,
            "1W": Interval.INTERVAL_1_WEEK,
            "1M": Interval.INTERVAL_1_MONTH
        }

        interval_constant = interval_mapping.get(self.interval)
        if interval_constant:
            self.data = TA_Handler(
                symbol=self.symbol,
                screener=self.screener,
                exchange=self.exchange,
                interval=interval_constant
            )

            if self.data:
                return self.data.get_analysis().summary
            else:
                return "No data available"
        else:
            return "Invalid interval specified"
    
    def search(self):
        return f'''
        SUMMARY:
        Asset Picked: {self.symbol}
        Screener: {self.screener}
        Exchange Market: {self.exchange}
        Interval = {self.interval}
        '''

    def show_search(self):
        if self.data:
            return self.data.get_analysis().summary
        else:
            return "No data available"

def send_file(filepath, source_ip, dest_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((source_ip, 0))  # Bind to the source IP address
        s.connect((dest_ip, port))
        filename = os.path.basename(filepath)
        s.sendall(filename.encode())

        # Open the file in binary mode and send its contents
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.sendall(data)

        print(f"Sender sent: {filename}")

def run():
    symbol = input("Choose the ticker for analysis: ")
    screener = input("Choose where the asset is being screened (america, crypto, etc.): ")
    exchange = input("Market of circulation: ")
    interval = input("Time of analysis (1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 1W, 1M): ")

    asset = Screener(symbol, screener, exchange)
    asset.interval = interval
    detailed_summary = asset.detailed_search()
    
    print(asset.search())
    print(detailed_summary)

    try:
        send_file("main.py", source_ip, dest_ip, port)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    run()


    