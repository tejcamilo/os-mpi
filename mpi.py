import socket
import threading

class MPI:
    def __init__(self, rank, size, ip_list):
        self.rank = rank
        self.size = size
        self.port = 12345
        self.ip_list = ip_list
        self.listener = None

        # Initialize sockets for communication
        self.sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(size)]
        
        # Bind sockets to ports and listen
        if rank == 0:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener.bind((ip_list[rank], self.port))
            self.listener.listen(size - 1)
        
        print(f"Process {rank} initialized on {ip_list[rank]}")

    def send(self, dest, data):
        # Connect to destination and send data
        self.sockets[dest].connect((self.ip_list[dest], self.port))
        self.sockets[dest].sendall(data.encode())
        self.sockets[dest].close()

    def recv(self):
        # Accept connection from any source and receive data
        connection, _ = self.listener.accept()
        data = connection.recv(1024).decode()
        connection.close()
        return data

    def barrier(self):
        # Simple barrier implementation using send/receive
        if self.rank == 0:
            # Rank 0 will receive messages from all other ranks
            for _ in range(self.size - 1):
                self.recv()
            # Rank 0 will send acknowledgment to all other ranks
            for i in range(1, self.size):
                self.send(i, "barrier")
        else:
            # All other ranks will send message to rank 0 and wait for acknowledgment
            self.send(0, "barrier")
            self.recv()

# Example usage
if __name__ == "__main__":
    num_processes = 2  # Example number of processes
    ip_list = ['192.168.1.100', '192.168.1.101']
    rank = int(input("Enter the rank of this device (0 or 1): "))
    mpi = MPI(rank, num_processes, ip_list)
    mpi.barrier()
    print(f"Process {rank}: Passed barrier")
    if rank == 0:
        mpi.send(1, f"Hello from Process {rank}!")
    else:
        data = mpi.recv()
        print(f"Process {rank}: Received '{data}'")
