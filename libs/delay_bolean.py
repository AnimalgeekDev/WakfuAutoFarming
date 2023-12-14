import time

from time import time

class DelayBolean:
    loop_time = 0
    seconds = 0

    def __init__(self):
        self.loop_time = time()

    def set_seconds(self, seconds):
        self.loop_time = time()
        self.seconds = seconds

    def wait(self):
        timer = time()
        if timer - self.loop_time > self.seconds:
            return True
        
        return False

def main():
    app = DelayBolean()

    print('Start')

    app.set_seconds(5)

    while(True):
        if app.wait():
            print('OK')
            break

if __name__ == "__main__":
    main()