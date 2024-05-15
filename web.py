import socket
import threading


def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")

    headers = request.split('\n')
    filename = headers[0].split()[1]

    if filename == '/':
        filename = '/index.html'

    try:
        fin = open('www' + filename)
        content = fin.read()
        fin.close()

        response = 'HTTP/1.1 200 OK\n'
        response += 'Content-Type: text/html\n'
        response += '\n'
        response += content
    except FileNotFoundError:
        response = 'HTTP/1.1 404 Not Found\n'
        response += 'Content-Type: text/html\n'
        response += '\n'
        response += '<html><body><h1>404 Not Found</h1></body></html>'

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 2222)) # ip address, port
    server_socket.listen(5)
    print("Server berjalan.....")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Terkoneksi: {addr}")
        # memisahkan koneksi user yang banyak (ini soal nomor 2)
        client_handler = threading.Thread(target=handle_request, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()


# buat folder www trus masukin aja cok index.html trus abis itu lu cek kalo 100 user request bakal bentrok gak. pake postman ae

