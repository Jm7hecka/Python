import socket
import os
import sys
import time
class server:
    def __init__(self,port):
        self.ip =socket.gethostbyname(socket.gethostname())
        self.port = port
        self.bufferSize = 10240

    def start(self):
         s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
         try:
           print('waiting for connection.')
           s.bind((self.ip, self.port))
           s.listen(5)  
           while True:
               try:
                 addr, client = s.accept()
                 print('client connected.')
                 while True:
                     file = input('Enter file you want to send:')
                     s.send(file)
                     f = open(file,'rb')
                     data = f.read(self.bufferSize)
                     s.send(data)

                     if not data:
                         break
               except socket.error as e:
                     print(e)
                     sys.exit()
         except socket.error  as e:
            print(e)
            sys.exit()
    def run(self):
        print('your IP address is:'+self.ip)
        num = 0
        input('Press Enter to continue...')
        while True:
            print('waiting for connection.')
            time.sleep(1)
            os.system('cls')
            print('waiting for connection..')
            time.sleep(1)
            os.system('cls')
            print('waiting for connection...')
            time.sleep(1)
            os.system('cls')
            num += 1
            if num == 3:
                break


if __name__ == '__main__':
    s = server(80)
    s.run()
    s.start()

