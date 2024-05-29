import json
import socket
import os
from dotenv import load_dotenv
import subprocess
import threading
import sys

load_dotenv()  # take environment variables from .env.
port = int(os.getenv('PORT'))

def receive_message(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"Receiver listening on port {port}...")
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024).decode()
            print(f"Receiver received: {data}")

def run_file(file_path, conn):
    try:
        # "capture_output=True" disables the print of the received file
        result = subprocess.run([sys.executable, file_path], capture_output=True, check=True)
        output = result.stdout.decode()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        output = f"File {file_path} not found."
    except subprocess.CalledProcessError as e:
        print(f"Error running {file_path}: {e}")
        output = f"Error running {file_path}: {e}"
    except Exception as e:
        print(f"Unexpected error: {e}")
        output = f"Unexpected error: {e}"

    # # Send the output back to the sender
    # conn.sendall(len(output).to_bytes(4, 'big'))  # Send the length of the output string
    # conn.sendall(output.encode())  # Send the output string

def receive_file(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"Receiver listening on port {port}...")
        while True:
            conn, addr = s.accept()
            with conn:
                # Receive the length of the variable string
                variable_str_length = int.from_bytes(conn.recv(4), 'big')
                # Receive and deserialize the variable string
                variable_str = conn.recv(variable_str_length).decode()
                run = json.loads(variable_str)
                #print(f"run: {run}")

                # Receive the length of the filename
                filename_length = int.from_bytes(conn.recv(4), 'big')
                # Receive the filename
                filename = conn.recv(filename_length).decode()
                # Get the directory of the current script
                dir_path = os.path.dirname(os.path.realpath(__file__))
                # Join the directory with the filename
                file_path = os.path.join(dir_path, filename)
                with open(file_path, 'wb') as f:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        f.write(data)
                print(f"Receiver received: {file_path}")

            if run:
                run_file(file_path, conn)


if __name__ == "__main__":
    receive_file(port)