import tkinter as tk
import webbrowser
from PIL import ImageFont

TICKER_HEIGHT=40


class Ticker():
    def __init__(self, root, feed):
        self.root = root
        self.feed = feed

        # Initialize some useful constants and variables
        self.refreshed = False
        self.w, h = getdims()
        self.h = TICKER_HEIGHT
        self.x = 0
        self.y = 0
        self.index = 0
        n = 1000
        self.font_width = int(GetFontWidth(13, 'resources\\lucon.tff', 'a'*n)[0]/n)

        # make widgets. Just an exit button and text for now
        self.root.geometry(f'{int(self.w)}x{self.h}')
        self.root.overrideredirect(1) 
        # self.root.attributes("-topmost", True)
        self.init_widgets()
        self.hyperlink = HyperlinkManager(self.text)

        self.get_text()
        self.shift()
    
    def init_widgets(self):
        button = tk.Button(self.root, text='X', command=self.root.quit)
        button.pack(side=tk.LEFT)
        button.configure(font=("Lucida Console", 18, "bold"))

        #TODO: fix width and height so as not to hard code
        text_frame = tk.Frame(self.root, width=1900, height=28)
        text_frame.pack(side=tk.LEFT, padx=5)
        # text_frame.grid(row=0, column=1, padx=20)
        # text_frame.columnconfigure(0, weight=1)
        # text_frame.grid_propagate(False)

        self.text = tk.Text(text_frame, wrap=tk.NONE, pady=6, width=200)
        self.text.grid(stick='we')
        self.text.configure(font=("Lucida Console", 13))

    def shift(self):
        """this function shifts the text to the left. It's pretty hackish, and 
        works by moving to the left one pixel until it eliminates one character.
        It assumes monospaced font, and uses self.font_width as the width for 
        every character. Once the character has been shifted away, it resets the x
        pixel displacement back to 0 while shifting the index of the text box one 
        character to the right.

        Once it reaches the end of the original text, it resets the index back to 0.
        It looks seamless because we padded the end of the original text with some
        text from the beginning.  So yeah, pretty fuckin' hackish
        """
        self.x = self.x - 1
        
        if abs(self.x) == self.font_width + 2:
            self.x = 0
            self.index += 1
            # self.text.configure(state=tk.NORMAL)
            self.text.delete(1.0)
            # self.text.configure(state=tk.DISABLED)

        if self.index >= self.last_index*.75 and not self.refreshed:
            self.refreshed = True
            self.refresh_data()

        if self.index == self.last_index - 1:
            self.refreshed = False
            self.get_text()
            self.index = 0

        self.text.place(x=self.x, y=self.y)
        self.root.after(7, self.shift)

    def refresh_data(self):
        self.feed.get_data()

        # Pad the end so when we reset the ticker for the new data,
        # it doesn't go from blank to full all of a sudden
        # self.text.configure(state=tk.NORMAL)
        for d in self.feed.data[:2]:
            if d['description']:
                desc = d['description'].strip('.') + ': '
            else:
                desc = 'No description available: '
            self.text.insert(tk.END, desc)
            if d.get('title'):
                self.text.insert(tk.END, d['title'], self.hyperlink.add(self.attach_hyperlink(d['link'])))
            self.text.insert(tk.INSERT, ' | ')
        
        # self.text.configure(state=tk.DISABLED)


    def get_text(self, n=30): 
        """This function resets the text back to the beginning.
        When I implement this as an RSS feed, I'll probably use this 
        function to get new RSS feed data. 

        Args:
            n (int, optional): number of stories. Defaults to 50.
        """
        # self.text.configure(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)

        for d in self.feed.data[:n]:
            if d['description']:
                desc = d['description'].strip('.') + ': '
            else:
                desc = 'No description available: '
            self.text.insert(tk.END, desc)
            if d.get('title'):
                self.text.insert(tk.END, d['title'], self.hyperlink.add(self.attach_hyperlink(d['link'])))
            self.text.insert(tk.INSERT, ' | ')
        # t = 'abcdefg'
        # for i in range(3):
        #     self.text.insert("end", t*(i+1) + ' | ')

        self.last_index = len(self.text.get('1.0', tk.END))
        self.text.see('1.0')
        self.text.configure(width=200)

        # self.text.configure(state=tk.DISABLED)
    
    def attach_hyperlink(self, link):
        return lambda: webbrowser.open(link, new=0, autoraise=True)


class HyperlinkManager:

    def __init__(self, text):

        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return


def GetFontWidth(point, font, char='a'):
    """Finds the pixel width of a character.

    Args:
        point (int): font size
        font (string): common font, requires .tff
        char (string): chars you'd like to know dimensions of. Default 'a'
    """
    font = ImageFont.truetype(font, point)
    size = font.getsize(char)
    return size


def getdims():
    try:
        from win32api import GetSystemMetrics
        w = GetSystemMetrics(0)
        h = GetSystemMetrics(1)
        return (w, h)
    except:
        print('need to add functionality for non-windows users')


if __name__=='__main__':
    print(GetFontWidth(18, 'resources\\lucon.tff', 'a'*1000))
