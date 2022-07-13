try:
    import socket
    import mss as mss
    from zlib import compress
    import subprocess
    import time
except:
    import subprocess
    list = ['mss' 'socket', 'zlib']
    num = 0
    print('Installing module')
    while num < 2:
        subprocess.run('python -m pip install {module}'.format(module  = list[num]))
        num +=1
class scrsharing():
    def __init__(self, port):
        self.ip = '192.0.0.1'
        self.port = port
        self.myip = socket.gethostbyname(socket.gethostname())
    def connect(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        while True:
            s.recv(1024)
            while True:
                    s.recv(1024)
                    scr = mss.mss()
                    monitor = scr.monitors[1]
                    while True:
                        try:
                            img = scr.grab(monitor)
                            data = mss.tools.to_png(img.rgb, img.size)
                            size = str(len(data)).encode()
                            size_len = len(size)
                            s.send(str(size_len).encode())
                            s.send(size)
                            x = s.sendall(data)
                        except:
                            self.connect()
    

if __name__== '__main__':
        shar = scrsharing(8080)
        shar.connect()
