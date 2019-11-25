import socket
import sys
import codecs
import threading
from time import ctime

#create the response HTTP header

encoding = "utf-8"

def response_HTTP_header(data):
    header = '''
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: '''+str(len(data.encode(encoding=encoding)))+'''\nContent-Type: text/html\n\n'''
    return header

# split the request

def split_method(b):
    str = b.decode()
    try:
        method = str.split(' ')[0]
        return method
    except:
        return 1

def split_path(b):
    str = b.decode()
    try:
        path_temp = str.split(' ')[1]
        path_temp = path_temp[1:]
        # path = path_temp.replace("/", "//")
        result =path_temp[0] + ":" + path_temp[1:]
        return result
    except:
        return 1


def ensure_file_exist(path):
    try:
        file = open(path, "r", encoding=encoding)
        str = file.read()
        file.close()
        return True
    except:
        return False


def read_file(path):
    try:
        file = codecs.open(path, 'r', encoding)
        str = file.read()
        file.close()
    except:
        str = False
    finally:
        return str


class Server:

    def __init__(self, localhost ,port):
        # timeout = 20
        addr = (localhost, port)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.setdefaulttimeout(timeout)
        server_socket.bind(addr)
        server_socket.listen(5)
        self.server_socket = server_socket

    # receive connection request from client

    def receive_connection_request(self):
        print("\r\nwaiting for requests...")
        new_client_socket, client_port = self.server_socket.accept()
        if new_client_socket:
            print("successfully connected\r\nthe ip port is ", client_port)
            return [True, new_client_socket, client_port]
        else:
            return False

    # receive the new client's request and deal

    def start_deal(self, new_client_socket, client_port):
        while True:
            request = new_client_socket.recv(1024)
            if request == 'exit':
                print("the link break. client port number ", client_port, ctime())
                break
            method = split_method(request)
            path = split_path(request)
            if not request:
                new_client_socket.send("error: didn't receive data.".encode(encoding))
                print("Didn't receive any data from client. client ip and port number ", client_port, ctime())
            if method == 'GET':
                if path == 1:
                    new_client_socket.send('404 Bad Request, the format you input is wrong.'.encode(encoding))
                    print("the format from client that he input is wrong. client ip and port number ", client_port, ctime())
                elif not ensure_file_exist(path):
                    new_client_socket.send("404 Not Found, Server can't find the file you request.".encode(encoding))
                    print("Server can't find the file the client request. client ip and port number ", client_port, ctime())
                else:
                    data_from_file = read_file(path)
                    response_message = response_HTTP_header(data_from_file) + data_from_file
                    response_message = response_message.encode('utf-8')
                    new_client_socket.send(response_message)
            elif method == "POST":
                form = request.split('\r\n')
                entry = form[-1]
                response_message = response_HTTP_header(entry) + entry
                response_message = response_message.encode('utf-8')
                response_message += '<br /><font color="green" size="7">post success!</p>'
                new_client_socket.send(response_message)
        new_client_socket.close()


def main():
    if len(sys.argv) != 3:
        print("argv input the wrong format.")
        return
    if not sys.argv[2].isdigit:
        print("please input the right port number.")
        return

    localhost = str(sys.argv[1])
    port_number = int(sys.argv[2])
    server = Server(localhost, port_number)

    while True:

        connection_list = server.receive_connection_request()
        if connection_list[0]:
            t = threading.Thread(target=server.start_deal, args=(connection_list[1], connection_list[2]))
            t.isDaemon()
            t.start()
            # t.exit()
        else:
            break


if __name__ == '__main__':
    main()
