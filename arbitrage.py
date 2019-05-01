import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Arbitrage:
    def __init__(self, file_path = 'C:\\chromedriver.exe'):
        self.file_path = file_path
        print('Scraping rates')
        self.getRates()


    def startDriver(self):
        option = webdriver.ChromeOptions()
        option.add_argument(" — incognito")
        browser = webdriver.Chrome(executable_path=self.file_path)
        browser.get("https://coinmarketcap.com/exchanges/bitmax/")
        self.browser = browser


    def getRates(self):
        exchange_lists = []
        self.startDriver()
        curr_tab = self.browser.find_elements_by_xpath('//table[@id="exchange-markets"]/tbody/tr')
        for tr in curr_tab:
            single_exchange = []
            td = tr.find_elements_by_tag_name("td")
            for i in range(1,6):
                if len(td[i].find_elements_by_class_name("price")) == 0:
                    single_exchange.append(td[i].get_attribute("data-sort"))
                else:
                    single_exchange.append(td[i].find_element_by_class_name("price").get_attribute("data-native"))
                    single_exchange.append(td[i].get_attribute("data-sort"))
            exchange_lists.append(single_exchange)
        df = pd.DataFrame(exchange_lists, columns = ["Currency", "Pair", "Volume", "Rate", "PriceUSD", "VolumePerc"])
        df.Rate = df.Rate.astype(float)
        df[['Numerator','Denumerator']] = df["Pair"].str.split("/",expand=True,)
        self.df = df


    def prepareData(self, df, initialCoin = 'BTC'):
        # INVERSE RATES CREATION
        # append copy of dataframe to create inverse rates
        df2 = df.copy()
        df2.Rate = list(map(lambda x: float(1/x), df2.Rate))
        df2 = df2.rename(columns={'Numerator':'Denumerator','Denumerator':'Numerator'})

        df = (df
                .append(df2, sort=False)
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


    def getUSDPrices(self):
        prices = (self.df[self.df.Currency.isin(['Bitcoin', 'Paxos Standard Token', 'USD Coin', 'Ethereum'])]
               .groupby('Numerator')['PriceUSD']
               .max()
               .to_dict())
        self.pricesUSD = prices


    def findArbitrage(self, quantity = 1):
        baseCoins = ['BTC', 'PAX', 'ETH', 'USDC']
        self.getUSDPrices()
        transactionList = []
        print('Searching for arbitrage opportunities')
        for coin in baseCoins:
            transactionList.append(str(f" Arbitrage using {quantity} {coin}"))
            df = self.df.copy()
            df, pairList = self.prepareData(df = df, initialCoin = coin)
            suma = 0
            n = 1
            quantity = quantity
            for i in pairList:
                add = self.triangularArbitrage(df = df, inputSet = (quantity, coin),
                                               firstTransaction = i[0], secondTransaction = i[1], fee = 0.0004)
                if add > 0:
                    suma += add
                    quantity += add
                    transactionList.append(str(f'        {n} operation: {coin} -> {i[0]} -> {i[1]} -> {coin}: {round(add, 5)} {coin}'))
                    n += 1
            if round(suma * float(self.pricesUSD[coin]), 2) > 0:
                transactionList.append(str(""))
                transactionList.append(str(f' Obtained: {round(suma * float(self.pricesUSD[coin]), 2)} USD by {n} triangular transactions using cummulated {coin} asset'))
                transactionList.append(str(""))
                transactionList.append(str('--------------------------------------'))
                transactionList.append(str(""))

        return transactionList


# # Instantiate an object of type Arbitrage (with path to chromedriver.exe on your machine)
# kA = Arbitrage('C:\\chromedriver.exe')
# # look for arbitrage opportunities on BitMax exchange (set the desired, initial quantity of currencies)
# kA.findArbitrage(quantity = 100)
