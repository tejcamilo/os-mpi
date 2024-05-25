import socket

class MPI:
    def __init__(self, rank, size, ip_list):
        self.rank = rank
        self.size = size
        self.port = 12345
        self.ip_list = ip_list
        self.listener = None
        self.connection = None

        # Initialize sockets for communication
        self.sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(size)]
        
        # Bind sockets to ports and listen if rank is 0
        if rank == 0:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener.bind((ip_list[rank], self.port))
            self.listener.listen(size - 1)
            print(f"Process {rank} initialized on {ip_list[rank]}")

    def connect(self):
        # Connect to the listener socket of rank 0
        if self.rank != 0:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.ip_list[0], self.port))
            print(f"Process {self.rank} connected to rank 0 on {self.ip_list[0]}")

    def send(self, data):
        # Send data to rank 0
        if self.rank != 0:
            self.connection.sendall(data.encode())

    def recv(self):
        # Receive data from rank 0
        if self.rank == 0:
            connection, _ = self.listener.accept()
            data = connection.recv(1024).decode()
            connection.close()
            return data

# Example usage
if __name__ == "__main__":
    num_processes = 2  # Example number of processes
    ip_list = ['192.168.20.22', '192.168.20.37']  # Replace with your actual IP addresses
    rank = int(input("Enter the rank of this device (0 or 1): "))
    mpi = MPI(rank, num_processes, ip_list)
    if rank != 0:
        mpi.connect()
    mpi.send(f"Hello from Process {rank}!")
    if rank == 0:
        data = mpi.recv()
        print(f"Process {rank}: Received '{data}'")
