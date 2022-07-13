import socket   
import time
import os 
import cv2 
from zlib import decompress
import numpy
class scrsharing():
    def __init__(self, port):
        self.ip = str(socket.gethostbyname(socket.gethostname()))
        self.port = port
    def connect(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        print('Connecting')
        s.listen(2)
        while True:
            addr, client = s.accept()
            self.addr = addr
            addr.send('package'.encode())
            print('Connected')
            x = input('Press Enter to Start screen sharing')
            addr.send('start'.encode())
            while True:
                print('Screen sharing started')
                print('Press Q to pause')
                oldtime = time.time()
                while True:
                        size_len = int(addr.recv(1).decode())
                        print(size_len)
                        try:
                            size = int(addr.recv(size_len).decode())
                            img = self.recvall(size)
                            timetaken = time.time() - oldtime
                            print('received. Time taken:{timetaken}'.format(timetaken = timetaken) )
                            oldtime = time.time()
                            addr.send('recved'.encode())
                            z = numpy.frombuffer(img, dtype=numpy.uint8)
                            img2 = cv2.imdecode(z, cv2.IMREAD_COLOR)
                            img2 = cv2.resize(img2,(800, 500))
                            cv2.imshow('img', img2)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                cv2.destroyAllWindows()
                                print('Screen sharing paused')
                                x = input('Press E to continue/ Press Q to leave')
                                if x == 'E':
                                    addr.send('continue'.encode())
                                    pass
                                else:
                                    print('Connection disconnected')
                        except:
                            print('Connection Error')
                        
    def recvall(self, length):
        addr = self.addr
        buf = b''
        while len(buf) < length:
            data = addr.recv(length - len(buf))
            print(length - len(buf))
            if not data:
                return data
            buf += data
        return buf
if __name__ == '__main__':
    print('Connecting to main computer')
    scr = scrsharing(8080)
    x = input('Press Enter to connect')
    while True:
        scr.connect()