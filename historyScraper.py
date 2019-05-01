import pandas as pd
from selenium import webdriver
import itertools
import time
import re
import matplotlib.pyplot as plt

class CryptoHistory():
    def __init__(self, file_path = 'C:\\chromedriver.exe'):
        self.file_path = file_path
        self.startDriver()
        self.getUrls()

    def striplist(self, list):
        return([x.replace(' ', '') for x in list])

    def startDriver(self):
        option = webdriver.ChromeOptions()
        option.add_argument(" — incognito")
        browser = webdriver.Chrome(executable_path=self.file_path)
        browser.get("https://coinmarketcap.com/exchanges/bitmax/")
        self.browser = browser

    def getUrls(self):
        urls = []
        infos = self.browser.find_elements_by_class_name('margin-left--lv1')
        urls = [(url.get_attribute("href") + "historical-data") for url in infos]
        mainUrls = []
        for item in urls:
            if re.search("bitcoin/|paxos|ethereum/|usd-coin", item):
                mainUrls.append(item)
        mainUrls = set(mainUrls)
        self.urls = mainUrls
        currencyNames = []
        for item in mainUrls:
            currencyNames.append((re.findall('currencies/(\w+-?\w+-?\w+)/historical-data', item)[0]))
        self.currencyNames = currencyNames

    def currHistory(self, url):
        self.browser.get(url)
#         time.sleep(5)
        exchange_lists = []
        curr_tab = self.browser.find_elements_by_xpath('//table[@class="table"]//tr')
        exchange_lists = [(td.text for td in tr.find_elements_by_xpath(".//*[self::td or self::th]")) for tr in curr_tab]
        df = pd.DataFrame(exchange_lists)
        df.columns = df.iloc[0]
        df = df.reindex(df.index.drop(0))
        df.sort_index(inplace = True, ascending = False)

        high_price = self.striplist(list(df.iloc[:,2].transpose()))
        volume = self.striplist(list(df.iloc[:,5].transpose()))
        return high_price, volume

    def historyToDataFrames(self):
        prices = []
        volumes = []

        for url in self.urls:
            price, volume = self.currHistory(url)
            prices.append(price)
            volumes.append(volume)

        df_prices = pd.DataFrame(prices).transpose()
        ratesColnames = [s + ' rate' for s in self.currencyNames]
        df_prices.columns = ratesColnames
        df_volumes = pd.DataFrame(volumes).transpose()
        volumesColnames = [s + ' volume' for s in self.currencyNames]
        df_volumes.columns = volumesColnames

        df_prices = df_prices.apply(lambda x: x.str.replace(',','.').astype(float))
        self.df_prices = df_prices
        df_volumes = df_volumes.apply(lambda x: x.str.replace(',','.').astype(float))
        self.df_volumes = df_volumes

    def plotHistoryData(self):
        self.df_prices.plot(title = 'Currency rates')
        plt.show()
        self.df_volumes.plot(title = 'Currency volumes')
        plt.show()

# testObject = CryptoHistory(file_path = 'C:\\chromedriver.exe')
# testObject.historyToDataFrames()
# testObject.plotHistoryData()
