import requests
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib
import os
import socket
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

data = {
    'result': 'this is a test',
    'RSP_HEAD': {'TRAN_SUCCESS': '1'}, 
    'RSP_BODY': {
        'rspCode': '200',
        'pid': 'CN11048023010321250000030000010',
        'CFCNO': '03',
        "AgentNo": "03",
        "PIDSts": "30",
        }
    }
host = ('localhost', PORT)

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        print("to get something......")
        d = self.headers
        # get_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        print(d)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
 
    def do_POST(self):
        print("to parse post......")
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        # You now have a dictionary of the post data
        print(post_data)
        # self.wfile.write("Lorem Ipsum".encode("utf-8"))
        self.send_response(200)
        # self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


def tcp_long_response():
    global HOST
    global PORT

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((HOST, PORT))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected {0} : {1}".format(address, str(data)))
        # data = input(' -> ')
        data = "hi"
        time.sleep(1)
        conn.send(data.encode())  # send data to the client
    conn.close()  # close the connection

def tcp_short_response():
    global HOST
    global PORT

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((HOST, PORT))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected {0} : {1}".format(address, str(data)))
        # data = input(' -> ')
        data = "hi"
        time.sleep(1)
        conn.send(data.encode())  # send data to the client
        conn.close()  # close the connection

        
""" 
@Des: When you want to capture the package of udp_response by Pktmon, the function should be executed in another computer, 
for there are no ETW providers about capturing package of UDP, the package is transmitted through network adapter.
"""
def udp_response():
    global HOST
    global PORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = (HOST, PORT)
    print('starting up on %s port %s' % server_address, sock.bind(server_address))
    
    while True:
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(4096)
        
        print('received %s bytes from %s' % (len(data), address))
        print(data)
        
        if data:
            sent = sock.sendto(data, address)
            print('sent %s bytes back to %s' % (sent, address))

def http_response():
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

def https_response():
    pass


def main():
    print("server pid: {}".format(os.getpid()))
    # tcp_short_response()
    # tcp_long_response()
    http_response()
    # udp_response()

if __name__ == "__main__":
    main()