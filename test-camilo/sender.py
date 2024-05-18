import socket
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
source_ip = os.getenv('SOURCE_IP')
dest_ip = os.getenv('DESTINATION_IP')
port = int(os.getenv('PORT'))

def send_message(message, source_ip, dest_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.bind((source_ip, 0))  # Bind to the source IP address
        s.connect((dest_ip, port))
        s.sendall(message.encode())
        print(f"Sender sent: {message}")

def send_file(filename, source_ip, dest_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((source_ip, 0))  # Bind to the source IP address
        s.connect((dest_ip, port))

        # Open the file in binary mode and send its contents
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.sendall(data)

        print(f"Sender sent: {filename}")        

#send_file("test.txt", source_ip, dest_ip, 6042)

if __name__ == "__main__":
    # message = "Hello from Sender!"
    # send_message(message, source_ip, dest_ip, port)
    filename = "/Users/ctejada/Desktop/os-proyecto/os-mpi/test-camilo/receiver.py"
    send_file(filename, source_ip, dest_ip, port)
    