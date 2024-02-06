from tkinter import *
from PIL import ImageTk, Image
from urllib.request import urlopen
import requests
import io
import webbrowser

class NewsApp:
    def __init__(self):
        # Fetch data
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=07ce6431517e45c5b04b589c36e5bed6').json()
        self.total_news = len(self.data['articles'])
        self.current_index = 0

        # Initial GUI load
        self.load_gui()
        # Load the 1st news item
        self.load_news_item()

    def load_gui(self):
        self.root = Tk()
        self.root.geometry('350x600')
        self.root.resizable(0, 0)
        self.root.title('New Express')

        # Create a canvas widget for the gradient background
        canvas = Canvas(self.root, width=350, height=600, highlightthickness=0)
        canvas.pack()

        # Define gradient colors
        start_color = "#0080FF"  # Light blue
        end_color = "#FFFFFF"    # White

        # Convert start and end colors to integers
        start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))

        # Draw gradient rectangle on the canvas
        for i in range(600):
            # Calculate the gradient color at each point
            r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / 600
            g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / 600
            b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / 600
            color = "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))

            # Draw a line of the gradient rectangle
            canvas.create_line(0, i, 350, i, fill=color)

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_item(self):
        # Clear the screen for the new news item
        self.clear()

        # Image
        try:
            img_url = self.data['articles'][self.current_index]['urlToImage']
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)

        label = Label(self.root, image=photo, bg='#FFFFFF')
        label.pack()

        heading = Label(self.root, text=self.data['articles'][self.current_index]['title'], bg='#FFFFFF', fg='#000000',
                        wraplength=350, justify='center', font=('Helvetica', 15, 'bold'))
        heading.pack(pady=(10, 20))

        details = Label(self.root, text=self.data['articles'][self.current_index]['description'], bg='#FFFFFF', fg='#000000',
                         wraplength=350, justify='center', font=('Helvetica', 12))
        details.pack(pady=(2, 20))

        frame = Frame(self.root, bg='#FFFFFF')
        frame.pack(expand=True, fill=BOTH)

        label.bind("<Button-1>", self.swipe_callback)

        read = Button(frame, text='Read More', width=16, height=3,
                      command=lambda: self.open_link(self.data['articles'][self.current_index]['url']), bg='#0080FF', fg='#FFFFFF', bd=0, font=('Helvetica', 12))
        read.pack()

        self.root.mainloop()

    def swipe_callback(self, event):
        if event.x > 200:  # Swipe to the right
            self.current_index = (self.current_index + 1) % self.total_news
        else:  # Swipe to the left
            self.current_index = (self.current_index - 1) % self.total_news
        self.load_news_item()

    def open_link(self, url):
        webbrowser.open(url)

# Test the NewsApp
obj = NewsApp()
