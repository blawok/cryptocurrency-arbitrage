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

class CryptoArbitrage(Frame):

    def __init__(self, master=None, file_path="C:\\chromedriver.exe"):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.file_path = file_path

    def init_window(self):

        self.master.title("Cryptocurrency arbitrage")
        self.pack(fill=BOTH, expand=1)

        load = Image.open("trading.png")
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
        load = Image.open("trading.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        kA = Arbitrage(self.file_path)
        transactionList = kA.findArbitrage(quantity = 100)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        listbox = Listbox(self, width=90, height=25, yscrollcommand=scrollbar.set)
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
        load = Image.open("trading.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        testObject = CryptoHistory(file_path = self.file_path)
        testObject.historyToDataFrames()

        self.df_prices = testObject.df_prices
        self.df_volumes = testObject.df_volumes

        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().pack()
        self.df_prices.plot(title='Currency rates', ax=ax1)

        button = Button(self, text="Show volumes graph", command=self.showVolumeGraph)
        button.place(relx = 0.1, rely = 0.3, anchor="center")
        button.pack()

        button = Button(self, text="Clear", command=self.clearOutput)
        button.place(relx = 0.1, rely = 0.3, anchor="center")
        button.pack()


    def showVolumeGraph(self):
        for widget in self.winfo_children():
            widget.destroy()

        load = Image.open("trading.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().pack()
        self.df_volumes.plot(title='Currency volumes', ax=ax1)

        button = Button(self, text="Show rates graph", command=self.showRatesGraph)
        button.place(relx = 0.1, rely = 0.3, anchor="center")
        button.pack()

        button = Button(self, text="Clear", command=self.clearOutput)
        button.place(relx = 0.1, rely = 0.3, anchor="center")
        button.pack()


    def showRatesGraph(self):
        for widget in self.winfo_children():
            widget.destroy()

        load = Image.open("trading.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().pack()
        self.df_prices.plot(title='Currency rates', ax=ax1)

        button = Button(self, text="Show volumes graph", command=self.showVolumeGraph)
        button.place(relx = 0.1, rely = 0.3, anchor="center")
        button.pack()

        button = Button(self, text="Clear", command=self.clearOutput)
        button.place(relx = 0.1, rely = 0.3, anchor="center")
        button.pack()

    def clearOutput(self):
        for widget in self.winfo_children():
            widget.destroy()

        load = Image.open("trading.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        button = Button(self, text="Find triangular arbitrage", command=self.showText)
        button.place(relx = 0.1, rely = 0.3, anchor="center")
        button.pack()


top = Tk()
top.geometry("1000x700")
app = CryptoArbitrage(top, "C:\\chromedriver.exe")
top.mainloop()
