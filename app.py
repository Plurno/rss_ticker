import tkinter as tk

from utils.text_utils import Ticker, getdims, TICKER_HEIGHT
from utils.feed_reader import FeedReader
import win32gui

def enumHandler(hwnd, lParam):
    try:
        x,y,w,z = win32gui.GetWindowRect(hwnd)
        if win32gui.IsWindowVisible(hwnd):
            if 'Command Prompt' in win32gui.GetWindowText(hwnd):
                pass
            else:
                y = TICKER_HEIGHT
                x = 0
                h = 1080-2*y
                w = 1920

                win32gui.MoveWindow(hwnd, x, y, w, h, True)
    except Exception as e:
        # print(e)
        pass

if __name__=='__main__':
    win32gui.EnumWindows(enumHandler, None)
    fr = FeedReader('./resources/rss_feeds.txt')
    
    root = tk.Tk()
    t = Ticker(root, fr)

    root.mainloop()
    root.destroy()
