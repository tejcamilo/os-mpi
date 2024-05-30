import json
import socket
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
source_ip = os.getenv('SOURCE_IP')
dest_ip = [os.getenv('DESTINATION_IP'),"192.168.64.2"]
port = int(os.getenv('PORT'))
port2 = int(os.getenv('PORT2'))

def send_message(message, source_ip, dest_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.bind((source_ip, 0))  # Bind to the source IP address
        s.connect((dest_ip, port))
        s.sendall(message.encode())
        print(f"Sender sent: {message}")

def send_file(filepath, source_ip, dest_ip, port, run=False):
    for ip in dest_ip:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((source_ip, 0))  # Bind to the source IP address
                s.connect((ip, port))

                # Serialize the variable to a string and send it
                variable_str = json.dumps(run)
                s.sendall(len(variable_str).to_bytes(4, 'big'))  # Send the length of the variable string
                s.sendall(variable_str.encode())  # Send the variable string

                filename = os.path.basename(filepath)
                # Send the length of the filename
                s.sendall(len(filename).to_bytes(4, 'big'))
                # Send the filename
                s.sendall(filename.encode())

                # Open the file in binary mode and send its contents
                with open(filepath, 'rb') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        s.sendall(data)

                print(f"Sender sent: {filename}")     
        except Exception as e:
            print(f"Error sending message to {ip}: {e}")

    # Create a new socket to receive the output
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((source_ip, port2))  # Bind to the source IP address
        s.listen()  # Listen for incoming connections
        while True:
            conn, addr = s.accept()  # Accept a connection
            with conn:
                # Receive the length of the output string
                output_str_length = int.from_bytes(conn.recv(4), 'big')
                # Receive and print the output string
                output_str = conn.recv(output_str_length).decode()
                print(f"Output from receiver: {output_str}")


if __name__ == "__main__":
    # message = "Hello from Sender!"
    # send_message(message, source_ip, dest_ip, port)
    filepath = "/Users/ctejada/Desktop/os-proyecto/os-mpi/test-camilo/test1.py"
    try:
        send_file(filepath, source_ip, dest_ip, port, True)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    