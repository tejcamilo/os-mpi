import socket
import threading

class MPI:
    def __init__(self, rank, size):
        self.rank = rank
        self.size = size
        self.port = 12345
        self.host = 'localhost'
        self.sockets = []

        # Initialize sockets for communication
        for _ in range(size):
            self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        
        # Bind sockets to ports and listen
        if rank == 0:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener.bind((self.host, self.port))
            self.listener.listen(size - 1)

    def send(self, dest, data):
        # Connect to destination and send data
        self.sockets[dest].connect((self.host, self.port))
        self.sockets[dest].sendall(data.encode())

    def recv(self, source):
        # Accept connection from source and receive data
        connection, _ = self.listener.accept()
        data = connection.recv(1024).decode()
        connection.close()
        return data

    def barrier(self):
        # Simple barrier implementation using send/receive
        for i in range(self.size):
            if i != self.rank:
                self.send(i, "barrier")
            else:
                for j in range(self.size - 1):
                    self.recv(j)

# Example usage
def example_mpi(rank, size):
    mpi = MPI(rank, size)
    print(f"Process {rank}: Initialized")
    mpi.barrier()
    print(f"Process {rank}: Passed barrier")
    mpi.send((rank + 1) % size, f"Hello from Process {rank}!")
    data = mpi.recv((rank - 1) % size)
    print(f"Process {rank}: Received '{data}' from Process {(rank - 1) % size}")

if __name__ == "__main__":
    num_processes = 4
    threads = []
    for i in range(num_processes):
        thread = threading.Thread(target=example_mpi, args=(i, num_processes))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
