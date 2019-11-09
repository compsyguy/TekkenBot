import win32.user32 as user32
import threading

###Testing imports
import time

class KeyboardListener():
    def __init__(self, char: str):
        if len(char) > 1:
            raise Exception('char must be 1 character')
        self.Char = ord(char)
        self.Listen = False
        
    def ListenThread(self):
        print("In Listen Thread")
        while(self.Listen):
             #if user32.get_async_key_state(user32.VK_CONTROL) & 0x8000 and (user32.get_async_key_state(0x57) & 0x1):
             if user32.get_async_key_state(user32.VK_CONTROL) & 0x8000 and (user32.get_async_key_state(self.Char) & 0x1):
                print("stuff")
                
    def run(self):
        thread = threading.Thread(target=self.ListenThread, name='Listener')
        thread.start()
                
    

    
if __name__ == "__main__":

    a = KeyboardListener('W')
    a.Listen = True
    a.run()    

    for i in range(10):
        print(i)
        time.sleep(1)
        
    a.Listen = False