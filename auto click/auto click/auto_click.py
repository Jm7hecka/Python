from pynput.keyboard import Key, Controller , Listener
from pynput.mouse import Button, Controller
import time
keyboard = Controller()

def on_press(key):
    if key.char == 's':
          while True:
              keyboard.press(Button.left)
              keyboard.release(Button.left)
              if key.char == 'x':
                  break


with Listener(on_press = on_press) as listener:
    listener.join()
listener.start()
