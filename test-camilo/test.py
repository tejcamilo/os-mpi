import socket

def get_local_ip():
    # This approach connects to an external address (like Google's DNS server) to get the local IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This doesn't actually send any data; it's just a trick to get the local IP address
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        print(f"Could not determine local IP address: {e}")
        local_ip = None
    finally:
        s.close()
    return local_ip

if __name__ == "__main__":
    local_ip = get_local_ip()
    if local_ip:
        print(f"Server's local IP address is: {local_ip}")
    else:
        print("Could not determine the local IP address")
