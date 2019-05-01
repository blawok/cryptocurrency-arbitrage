from tkinter import *
import pandas as pd
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import itertools
import time
import re
import matplotlib.pyplot as plt

from arbitrage import Arbitrage
from historyScraper import CryptoHistory

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):

        self.master.title("Cryptocurrency arbitrage")
        self.pack(fill=BOTH, expand=1)

        load = Image.open("dolla.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)
        edit = Menu(menu)
        edit.add_command(label="Browse currency history", command=self.showHistory)
        menu.add_cascade(label="Options", menu=edit)

        button = Button(self, text="Find triangular arbitrage", command=self.showText)
        button.place(relx = 0.1, rely = 0.3, anchor="center")
        button.pack()

    def showText(self):
        load = Image.open("dolla.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        kA = Arbitrage('C:\\chromedriver.exe')
        transactionList = kA.findArbitrage(quantity = 100)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        listbox = Listbox(self, width=90, height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        for listId, transaction in enumerate(transactionList):
            listbox.insert(listId, transaction)
        listbox.place(relx = 0.1, rely = 0.3, anchor="center")
        listbox.pack()

        button = Button(self, text="Clear", command=self.clearOutput)
        button.place(relx = 0.1, rely = 0.3, anchor="center")
        button.pack()

    def showHistory(self):
        load = Image.open("dolla.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        testObject = CryptoHistory(file_path = 'C:\\chromedriver.exe')
        testObject.historyToDataFrames()
        # testObject.plotHistoryData()

        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().pack()
        testObject.df_prices.plot(title='Currency rates', ax=ax1)
        # testObject.plotHistoryData()

    def clearOutput(self):
        for widget in self.winfo_children():
            widget.destroy()

        load = Image.open("dolla.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        button = Button(self, text="Find triangular arbitrage", command=self.showText)
        button.place(relx = 0.1, rely = 0.3, anchor="center")
        button.pack()


top = Tk()
top.geometry("700x500")
#creation of an instance
app = Window(top)
top.mainloop()
