import socket

def send_message(message, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode())
        print(f"Sender sent: {message}")

if __name__ == "__main__":
    host = '201.234.181.230'  # Replace with the IP address of the receiver
    port = 60042  # Choose a port to listen on
    message = "Hello from Sender!"
    send_message(message, host, port)
