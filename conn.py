from flask import Flask, render_template, request
import socket

app = Flask(__name__)

# TCP client function for temperature conversion
def temperature_client_tcp(server_addr, value, unit_from, unit_to):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_addr)
        message = f"{value} {unit_from} {unit_to}"
        print(message)
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        return data.decode()

# UDP client function for temperature conversion
def temperature_client_udp(server_addr, value, unit_from, unit_to):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"{value} {unit_from} {unit_to}"
    print("udp")
    print(message)
    client_socket.sendto(message.encode(), server_addr)
    data, _ = client_socket.recvfrom(1024)
    client_socket.close()
    return data.decode()

# Default route
@app.route('/')
def index():
    return render_template('index.html')

# Route for temperature conversion
@app.route('/convert', methods=['POST'])
def convert():
    print("Received conversion request")
    value = request.form['value']
    unit_from = request.form['unit_from']
    unit_to = request.form['unit_to']
    protocol = request.form['protocol']

    server_ip = '10.1.74.109'  # Replace with your server's IP
    server_port = 12345  # Replace with your server's port
    server_addr = (server_ip, server_port)

    # Send the request based on the protocol
    if protocol == 'TCP':
        response = temperature_client_tcp(server_addr, value, unit_from, unit_to)
    else:
        response = temperature_client_udp(server_addr, value, unit_from, unit_to)

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
