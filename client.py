import requests
import sys
import os
import socket
import time
import requests
import json
import urllib.request
import os

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# HOST = "10.11.178.217"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def tcp_short_request():
    global HOST
    global PORT

    num = 1
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
        client_socket.connect((HOST, PORT))  # connect to the server
        print("No.{0}".format(num))
        num += 1

        message = "hello"
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        # message = input(" -> ")  # again take input
        time.sleep(1)

    client_socket.close()  # close the connection

def tcp_long_request():
    global HOST
    global PORT

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((HOST, PORT))  # connect to the server

    num = 1
    while True:
        print("No.{0}".format(num))
        num += 1

        message = "hello"
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        # message = input(" -> ")  # again take input
        time.sleep(1)

    client_socket.close()  # close the connection

""" 
@Des: When you want to capture the package of udp_response by Pktmon, the function should be executed in another computer, 
for there are no ETW providers about capturing package of UDP, the package is transmitted through network adapter.
"""
def udp_request():
    global HOST
    global PORT

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (HOST, PORT)
    message = b'This is the message.  It will be repeated.'

    num = 1
    while True:
        print("No.{0}".format(num))
        num += 1
        try:

            # Send data
            print('sending "%s"' % message)
            sent = sock.sendto(message, server_address)

            # Receive response
            print('waiting to receive')
            data, server = sock.recvfrom(4096)
            print('received "%s"' % data)

        except Exception as e:
            print("Error")
            sock.close()
            exit(-1)

        time.sleep(1)

def http_request():
    global PORT

    conn = requests.session()
    # url = 'http://www.gsdata.cn/member/login'
    url = 'http://localhost:' + str(PORT)
    postdata = {
        "PID": "1234561213141314334534535636356",
        "CARDNO": "6222623434343465645",
        "PST_CDE": "200000",
        "PST_ADR":"shanghia chuanshan ybocomm 13232 room",
        "PNM":"Lin Zhen",
        "MOB_NUM":"13332333445",
    }
    print("conn: {0}".format(conn))
    num = 1
    while True:
        headers = {'content-type': "application/json", 'Authorization': 'APP appid = 4abf1a,token = 9480295ab2e2eddb8'}
        rep = conn.post(url, data=postdata, headers=headers)
        print("No.{0}".format(num))
        num += 1
        time.sleep(1)

def https_request():
    pass

def main():
    print("client pid: {}".format(os.getpid()))
    # tcp_short_request()
    # tcp_long_request()
    http_request()
    # udp_request()

if __name__ == "__main__":
    main()