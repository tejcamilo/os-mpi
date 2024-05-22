from screener import Screener
from mpi import MPI

def run_mpi(rank, size, ip_list):
    symbol = "AAPL"
    screener = "america"
    exchange = "NASDAQ"
    intervals = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1W", "1M"]

    mpi = MPI(rank, size, ip_list)
    if rank != 0:
        mpi.connect()
    
    mpi.send(f"Ready from Process {rank}!")
    if rank == 0:
        mpi.recv()
    
    asset = Screener(symbol, screener, exchange)
    asset.interval = intervals[rank]
    result = asset.detailed_search()

    print(f"Process {rank} - Interval: {intervals[rank]}")
    print(result)
    print()

if __name__ == "__main__":
    num_processes = 2  # Adjust based on your setup
    ip_list = [""]  # Replace with your actual IP addresses
    rank = int(input("Enter the rank of this device (0 or 1): "))
    run_mpi(rank, num_processes, ip_list)


# Ejecucción en varias máquinas
    '''
    num_processes = 2  # Ajustar
    ip_list = ['192.168.1.100', '192.168.1.101']  # IPs
    rank = int(input("Enter the rank of this device (0 or 1): "))
    run_mpi(rank, num_processes, ip_list)
    '''
