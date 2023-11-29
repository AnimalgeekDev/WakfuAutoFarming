import cv2
import numpy as np
from time import time
from mss import mss

loop_time = time()

with mss() as sct:
    monitor = sct.monitors[1:][0]

    print("loop")

    while(True):
        with mss() as sct:
            print("screenshot")
            screenshot = np.array(sct.grab(monitor))

            print("print screen")
            cv2.imshow('screen', cv2.resize(screenshot, (screenshot.shape[1]//4, screenshot.shape[0]//4)))

            print('FPS {}'.format(1 / (time() - loop_time)))
            loop_time = time()

            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break

print('Done.')