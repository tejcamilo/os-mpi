from screener import Screener
from mpi import MPI
import threading

def run_mpi(rank, size):
    symbol = "AAPL"
    screener = "america"
    exchange = "NASDAQ"
    intervals = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1W", "1M"]

    mpi = MPI(rank, size)
    mpi.barrier()

    asset = Screener(symbol, screener, exchange)
    asset.interval = intervals[rank]
    result = asset.detailed_search()

    mpi.barrier()
    
    print(f"Process {rank} - Interval: {intervals[rank]}")
    print(result)
    print()

if __name__ == "__main__":
    num_processes = 10
    threads = []
    for i in range(num_processes):
        thread = threading.Thread(target=run_mpi, args=(i, num_processes))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
