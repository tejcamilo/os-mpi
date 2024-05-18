import socket
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
source_ip = os.getenv('SOURCE_IP')
dest_ip = os.getenv('DESTINATION_IP')



def send_message(message, source_ip, dest_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.bind((source_ip, 0))  # Bind to the source IP address
        s.connect((dest_ip, port))
        s.sendall(message.encode())
        print(f"Sender sent: {message}")

if __name__ == "__main__":
    port = 6042  # Choose a port to listen on
    message = "Hello from Sender!"
    send_message(message, source_ip, dest_ip, port)