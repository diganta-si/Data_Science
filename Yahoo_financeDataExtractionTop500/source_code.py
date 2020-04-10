
# '@author Diganta Si (horritz)'


import requests as rqst
import pandas as pd

wikiURL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
wikiResponse = rqst.get(wikiURL)

data = {"Company": []}

wikiFirstParse = wikiResponse.text.split("0001555280")[0]
wikiDataTable = wikiFirstParse.split("component stocks")[3]
hyperLinkSplitWiki = wikiDataTable.split("href=")

start = 4
for position in range(len(hyperLinkSplitWiki)):
    if position > start:
        if "nyse" in hyperLinkSplitWiki[position]:
            if "quote" in hyperLinkSplitWiki[position]:
                tempData = hyperLinkSplitWiki[position].split('">')[1].split("</")[0]
                data["Company"].append(tempData)
        elif "nasdaq" in hyperLinkSplitWiki[position]:
            if "symbol" in hyperLinkSplitWiki[position]:
                tempData = hyperLinkSplitWiki[position].split('">')[1].split("</")[0]
                data["Company"].append(tempData)

Indicators = {"Previous Close": [],
              "Open": [],
              "Bid": [],
              "Ask": [],
              "Volume": [],
              "Avg. Volume": [],
              "Market Cap": [],
              "Beta (5Y Monthly)": [],
              "PE Ratio (TTM)": [],
              "EPS (TTM)": [],
              "Earnings Date": [],
              "Ex-Dividend Date": [],
              "1y Target Est": []}

Indicators_part = {"Day&#x27;s Range": [],
                   "52 Week Range": [],
                   "Forward Dividend &amp; Yield": []}

for tickerSymbol in data["Company"]:
    url = ("https://finance.yahoo.com/quote/"+tickerSymbol+"?p="+tickerSymbol)
    response = rqst.get(url)
    htmlText = response.text
    for indicator in Indicators:
        try:
            splitList = htmlText.split(indicator)
            afterFirstSplit = splitList[1].split("\">")[2]
            afterSecondSplit = afterFirstSplit.split("</span>")
            dataValue = afterSecondSplit[0]
            if dataValue == '<td class="C($primaryColor) W(51%)" data-reactid="27' or dataValue == '<td class="C($primaryColor) W(51%)" data-reactid="31' or dataValue == '<td class="C($primaryColor) W(51%)" data-reactid="78' or dataValue == '<td class="C($primaryColor) W(51%)" data-reactid="86' or dataValue == '<td class="C($primaryColor) W(51%)" data-reactid="87' or dataValue == '<td class="C($primaryColor) W(51%)" data-reactid="89':
                afterFirstSplit = splitList[1].split("\">")[1]
                afterSecondSplit = afterFirstSplit.split("</td>")
                dataValue = afterSecondSplit[0]
            Indicators[indicator].append(dataValue)
        except:
            Indicators[indicator].append("N/A")
    for indicator in Indicators_part:
        try:
            splitList = htmlText.split(indicator)
            afterFirstSplit = splitList[1].split("\">")[1]
            afterSecondSplit = afterFirstSplit.split("</td>")
            dataValue = afterSecondSplit[0]
            Indicators_part[indicator].append(dataValue)
        except:
            Indicators_part[indicator].append("N/A")


Indicators.update(Indicators_part)
data.update(Indicators)

df = pd.DataFrame(data)

print(data)
print(len(data['Ex-Dividend Date']))
print(len(data["Company"]))
print(data.keys())
print(df.head())
print(df.tail())

writer = pd.ExcelWriter('Stock_data.xlsx')
df.to_excel(writer, 'market_values')
writer.save()
print("Data frame is saved successfully!")
