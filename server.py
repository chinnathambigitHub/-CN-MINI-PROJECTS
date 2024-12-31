import socket
import math

HOST = '10.1.74.109'  # Listen on all available interfaces
PORT = 12345  # Port to bind to

# Function for temperature conversion
def convert_temperature(value, unit_from, unit_to):
    try:
        value = float(value)
        if unit_from == "C":
            if unit_to == "F":
                return str((value * 9/5) + 32) +" F"
            elif unit_to == "K":
                return str(value + 273.15)+" K"
        elif unit_from == "F":
            if unit_to == "C":
                return str((value - 32) * 5/9)+" C"
            elif unit_to == "K":
                return str((value - 32) * 5/9 + 273.15) +" K"
        elif unit_from == "K":
            if unit_to == "C":
                return str(value - 273.15)+" C"
            elif unit_to == "F":
                return str((value - 273.15) * 9/5 + 32)+" F"
        else:
            return "Invalid temperature unit"
    except ValueError:
        return "Value Error"
    except Exception as e:
        return str(e)

# Function to handle TCP connections
def handle_tcp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"TCP Server is listening on port {PORT}...")

        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print(f"Client is {addr} ")
                        break
                    parts = data.decode().split()
                    if len(parts) == 3:
                        value, unit_from, unit_to = parts
                        response = convert_temperature(value, unit_from, unit_to)
                    else:
                        response = "Error: Invalid input format"
                    conn.sendall(str(response).encode())

# Function to handle UDP connections
def handle_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f"UDP Server is listening on port {PORT}...")

        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"Connected by {addr}")
            parts = data.decode().split()
            if len(parts) == 3:
                value, unit_from, unit_to = parts
                response = convert_temperature(value, unit_from, unit_to)
            else:
                response = "Error: Invalid input format"
            server_socket.sendto(str(response).encode(), addr)

# Main function to run both TCP and UDP servers
if __name__ == '__main__':
    import threading

    # Create threads for TCP and UDP servers
    tcp_thread = threading.Thread(target=handle_tcp)
    udp_thread = threading.Thread(target=handle_udp)

    tcp_thread.start()
    udp_thread.start()

    tcp_thread.join()
    udp_thread.join()
