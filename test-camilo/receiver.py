import socket

def receive_message(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"Receiver listening on port {port}...")
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024).decode()
            print(f"Receiver received: {data}")

if __name__ == "__main__":
    port = 6042  # Choose the same port used by the sender
    receive_message(port)
