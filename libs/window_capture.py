import cv2
import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:
    w = 0
    h = 0
    hwnd = None
    window_name=''

    def __init__(self, window_name):
        self.window_name = window_name
        self.hwnd = win32gui.FindWindow(None, self.window_name)

        if not self.hwnd:
            raise Exception("Window not found")
        
        self.w = 1920
        self.h = 1080
    
    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0), (self.w,self.h), dcObj, (0,0), win32con.SRCCOPY)

        signedInstAray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedInstAray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]

        img = np.ascontiguousarray(img)

        return img

def main():
    app = WindowCapture("WAKFU")

    while(True):
        img = app.get_screenshot()

        cv2.imshow(app.window_name, img)

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()