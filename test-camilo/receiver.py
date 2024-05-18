import socket
import os
from dotenv import load_dotenv
import subprocess

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

def receive_file(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"Receiver listening on port {port}...")
        conn, addr = s.accept()
        with conn:
            # Receive the filename
            filename = conn.recv(1024).decode()
            with open(filename, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print(f"Receiver received: {filename}")

    # Run the received file
    try:
        subprocess.run(["python", filename], check=True)
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {filename}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    #receive_message(port)
    receive_file(port)
