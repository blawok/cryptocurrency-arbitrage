from tkinter import *
import pandas as pd
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from arbitrage import Arbitrage

class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):

        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        #reference to the master widget, which is the tk window
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()


    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        edit = Menu(menu)

        edit.add_command(label="Find triangular arbitrage", command=self.showText)
        #added "file" to our menu
        menu.add_cascade(label="Find arbitrage", menu=edit)

        button = Button(self, text="Find triangular arbitrage", command=self.showText)
        button.place(x=10, y=100)
        button.pack()

    def prepareData(self, df, initialCoin = 'BTC'):
        # INVERSE RATES CREATION
        # append copy of dataframe to create inverse rates
        df2 = df.copy()
        df2.Rate = list(map(lambda x: float(1/x), df2.Rate))
        df2 = df2.rename(columns={'Numerator':'Denumerator','Denumerator':'Numerator'})

        df = (df
                .append(df2, sort=False)
                .drop(columns=['Unnamed: 0'])
                .reset_index()
                .drop(columns=['index'])
             )

        # POSSIBLE PAIRS CREATION
        pairList = []
        # for every denumerator that has BTC as numerator
        for i in list(df.Denumerator[df['Numerator'] == initialCoin]):
            # for every denumerator that has i as numerator
            for j in list(set((df.Denumerator[(df['Numerator'] == i) & (df['Numerator'] != initialCoin) & (df['Denumerator'] != initialCoin)]))):
                if j in list(df.Denumerator[df['Numerator'] == initialCoin]):
                    pairList.append([i,j])

        return df, pairList

    def triangularArbitrage(self, df, inputSet, firstTransaction, secondTransaction, fee):
        # first transaction
        output1 = inputSet[0]/df.Rate.loc[(df['Numerator'] == inputSet[1]) & (df['Denumerator'] == firstTransaction)].values[0]
        output1 = output1 - fee*output1

        # second transaction
        output2 = output1/df.Rate.loc[(df['Numerator'] == firstTransaction) & (df['Denumerator'] == secondTransaction)].values[0]
        output2 = output2 - fee*output2

        # third transaction
        output3 = output2/df.Rate.loc[(df['Numerator'] == secondTransaction) & (df['Denumerator'] == inputSet[1])].values[0]
        output2 = output2 - fee*output2

        return float(output3 - inputSet[0])

    def showText(self):
        load = Image.open("dolla.png")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        # read data
        df = pd.read_csv('testData.csv')
        # transform dataframe
        initialCoin = 'BTC'
        df, pairList = self.prepareData(df = df, initialCoin = initialCoin)

        suma = 0
        n = 1
        btcQuantity = 1
        transactionList = []
        for i in pairList:
            add = self.triangularArbitrage(df = df, inputSet = (btcQuantity, initialCoin), firstTransaction = i[0], secondTransaction = i[1], fee = 0.0004)
            if add > 0:
                suma += add
                btcQuantity += add
                transactionList.append(str(f'{n} operation: {initialCoin} -> {i[0]} -> {i[1]} -> {initialCoin}: {round(add, 5)} {initialCoin}'))
                n += 1

        text = Label(self, text=f'Obtained: {round(suma * 20143.63, 2)} PLN by {n} triangular transactions using cummulated {initialCoin} asset')
        text.pack()


        Lb1 = Listbox(self, width=60, height=20)
        for listId, transaction in enumerate(transactionList):
            Lb1.insert(listId, transaction)
        Lb1.place(relx = 0.1, rely = 0.3, anchor="center")
        Lb1.pack()



# top = Tk()

# top.geometry("500x500")

# photo=PhotoImage(file="test.png")
# l=Label(top,image=photo)

# #creation of an instance
# app = Window(top)


# #mainloop
# top.mainloop()

# Instantiate an object of type Arbitrage (with path to chromedriver.exe on your machine)
kA = Arbitrage('C:\\chromedriver.exe')
# look for arbitrage opportunities on BitMax exchange (set the desired, initial quantity of currencies)
kA.findArbitrage(quantity = 100)
