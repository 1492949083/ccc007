import win32gui, win32ui, win32con, win32api
import os
from PIL import Image
import numpy as np

class Screenshot:
    def __init__(self, filename=None, filepath=None):
        self.screenshot(filename, filepath)        


    def screenshot(self, filename=None, filepath=None):
        hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 获取监控器信息
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        w = MoniterDev[0][2][2]
        h = MoniterDev[0][2][3]
        # print w,h　　　#图片大小
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从左上角（0，0）长宽为（w，h）的图片
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
        if filename and filepath:
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            full_path = os.path.join(filepath, filename)
            saveBitMap.SaveBitmapFile(saveDC, full_path)
        elif filename:
            saveBitMap.SaveBitmapFile(saveDC, filename)
        # Convert bitmap to numpy array
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )
        arr = np.array(img)
        return arr
    
    def width(self):
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        return MoniterDev[0][2][2]
    
    def height(self):
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        return MoniterDev[0][2][3]
    

