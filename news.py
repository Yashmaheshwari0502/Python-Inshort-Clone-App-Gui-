
import requests
from tkinter import *
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
import webbrowser


class NewsApp:
    def __init__(self):
        # Fetch data
        self.data = requests.get(
            'https://newsapi.org/v2/top-headlines?country=us&apiKey=db0a42ac9ff24bc0890f97c480916acb'
        ).json()

        if self.data.get('status') != 'ok':
            print(self.data)
            return

        # Initial GUI load
        self.root = Tk()
        self.root.geometry('350x600')
        self.root.resizable(0, 0)
        self.root.configure(background='black')
        self.root.title('B2Czone ')

        # Load the first news item
        self.load_news_item(0)

        self.root.mainloop()

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_item(self, index):

        if index < 0 or index >= len(self.data['articles']):
            return

        self.clear()

        article = self.data['articles'][index]

        # Load image
        img_url = article['urlToImage']

        if img_url:
            try:
                raw_data = urlopen(img_url).read()
                im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
                self.photo = ImageTk.PhotoImage(im)

                label = Label(self.root, image=self.photo)
                label.pack()

            except Exception as e:
                print("Image Error:", e)

        # Heading
        heading = Label(
            self.root,
            text=article['title'],
            bg='black',
            fg='white',
            wraplength=350,
            justify='center'
        )
        heading.pack(pady=(10, 20))
        heading.config(font=('verdana', 15))

        # Details
        details = Label(
            self.root,
            text=article['description'] or 'No description available',
            bg='black',
            fg='white',
            wraplength=350,
            justify='center'
        )
        details.pack(pady=(2, 20))
        details.config(font=('verdana', 12))

        # Buttons frame
        frame = Frame(self.root, bg='black')
        frame.pack(expand=True, fill=BOTH)

        # Previous button
        if index != 0:
            prev = Button(
                frame,
                text='Prev',
                width=10,
                height=3,
                command=lambda: self.load_news_item(index - 1)
            )
            prev.pack(side=LEFT)

        # Read More button
        read = Button(
            frame,
            text='Read More',
            width=10,
            height=3,
            command=lambda: self.open_link(article['url'])
        )
        read.pack(side=LEFT)

        # Next button
        if index != len(self.data['articles']) - 1:
            next = Button(
                frame,
                text='Next',
                width=10,
                height=3,
                command=lambda: self.load_news_item(index + 1)
            )
            next.pack(side=LEFT)

    def open_link(self, url):
        webbrowser.open(url)


obj = NewsApp()




#devops engineer 



