# importing the required module
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from datetime import datetime, date
import pytz
import requests

def convert_date_to_UTCtimestamp(fulldate):
    UTCTime = pytz.timezone('Etc/UTC')
    dateUTC = str(fulldate).split("-")
    dt = datetime(int(dateUTC[0]), int(dateUTC[1]), int(dateUTC[2]), 0, 0, 0)
    cest_local = UTCTime.localize(dt, is_dst=True)
    unixTimestamp = cest_local.timestamp()
    
    return unixTimestamp

def convert_timestamp_to_date(timestamp):
    #Conversion to seconds -> Needed to run datetime function
    timestamp = timestamp/1000
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    return date

def get_coin_data(coin, currency, startTime, EndTime):
    datetime1 = convert_date_to_UTCtimestamp(startTime)
    datetime2 = convert_date_to_UTCtimestamp(EndTime)
    amountOfDays = int((((datetime2-datetime1)/3600)/24))
    URL = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range?vs_currency={currency}&from={datetime1}&to={datetime2}"
    print("Fetching data from: " + URL)
    #print("Days: " + str(amountOfDays))
    r = requests.get(url = URL)
    response = r.json()

    return response, amountOfDays

def parse_response_data(response, amountOfDays):
    timestamps = []
    volume = []
    prices = []

    if amountOfDays == 1:
        timestamps.append(response['total_volumes'][0][0]), volume.append(response['total_volumes'][0][1]), prices.append(response['prices'][0][1])
        timestamps.append(response['total_volumes'][-1][0]), volume.append(response['total_volumes'][-1][1]), prices.append(response['prices'][-1][1])
    elif amountOfDays > 90:
        for i in range(amountOfDays):
            timestamps.append(response['total_volumes'][i][0]), volume.append(response['total_volumes'][i][1]), prices.append(response['prices'][i][1])
    else:
        incrementor = 0
        for i in range(len(response['prices'])):
            if i == 0 or i % ((incrementor * 24) - 1) == 0:
                incrementor += 1
                timestamps.append(response['total_volumes'][i][0]), volume.append(response['total_volumes'][i][1]), prices.append(response['prices'][i][1])
        #Append last price of the coingecko response if it has not been added yet -> Coingecko API doesn't always operate in 24hour intervals, so the for loop can miss the last date
        if prices[-1] != response['prices'][-1][1]:
            timestamps.append(response['total_volumes'][-1][0]), volume.append(response['total_volumes'][-1][1]), prices.append(response['prices'][-1][1])

    return timestamps, volume, prices

def get_best_profit(dailyPrices, dailyTimeStamps):
    smallestPrice = 0
    highestPrice = 0
    smallestCurrentPriceTimeStamp = 0
    smallestPriceTimeStamp = 0
    highestPriceTimeStamp = 0
    bestPercentagePossible = 0
    biggestProfit = 0

    for i in range(len(dailyPrices)):
        #Initialize values incase price only goes up or down
        if i == 0:
            smallestPrice = dailyPrices[i]
            smallestPriceTimeStamp = dailyTimeStamps[i]
            smallestCurrentPriceTimeStamp = dailyTimeStamps[i]
            highestPriceTimeStamp = dailyTimeStamps[i]
        else:
            #Check if daily price is smaller than current smallest price
            if dailyPrices[i] < smallestPrice:
                smallestPrice = dailyPrices[i]
                smallestCurrentPriceTimeStamp = dailyTimeStamps[i]
                #Reset highestPrice
                highestPrice = 0     
            #Check if daily price is smaller than current highest value
            if dailyPrices[i] > highestPrice:
                highestPrice = dailyPrices[i]
                currentBiggestProfit = highestPrice - smallestPrice
                if currentBiggestProfit > biggestProfit:
                    highestPriceTimeStamp = dailyTimeStamps[i]
                    smallestPriceTimeStamp = smallestCurrentPriceTimeStamp
                    biggestProfit = currentBiggestProfit

    return biggestProfit, smallestPriceTimeStamp, highestPriceTimeStamp

#Matplotlib plotting
def annotate_and_plot(text, xTimestamp, yPrice, color, offset = 0, graphSymbol='o'):
    ax.plot([xTimestamp],[yPrice], graphSymbol)
    ax.annotate(text, xy = (xTimestamp, yPrice), xytext = (xTimestamp, yPrice+offset), color=color)

#Matlab function ran when submitting data
def submit(expression):
    #Get all coin information
    coin, currency, startTime, EndTime = expression.split(",")
    response, amountOfDays = get_coin_data(coin, currency, startTime, EndTime)
    dailyTimeStamps, dailyVolumes, dailyPrices = parse_response_data(response, amountOfDays)
    biggestProfit, smallestPriceTimeStamp, highestPriceTimeStamp = get_best_profit(dailyPrices, dailyTimeStamps)

    #Clear and reset matplotlib chart when sending a new request for data
    ax.clear()
    ax.set_title(f'{coin} Chart')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Price')

    #Create plot with timestamp and price data
    x = dailyTimeStamps
    y = dailyPrices
    l, = ax.plot(x, y)

    if biggestProfit != 0:
        buyPrice = dailyPrices[dailyTimeStamps.index(smallestPriceTimeStamp)]
        sellPrice = dailyPrices[dailyTimeStamps.index(highestPriceTimeStamp)]
        buyText = f' BuyPoint \n {convert_timestamp_to_date(smallestPriceTimeStamp)}, {str(int(buyPrice))} {currency}'
        sellText = f' SellPoint \n {convert_timestamp_to_date(highestPriceTimeStamp)}, {str(int(sellPrice))} {currency}'
        biggestProfitText = f' Profit {int((sellPrice/buyPrice-1)*100)}%'
        annotate_and_plot(buyText, smallestPriceTimeStamp, buyPrice,"red")
        annotate_and_plot(sellText, highestPriceTimeStamp, sellPrice,"green")
        annotate_and_plot(biggestProfitText, dailyTimeStamps[0], dailyPrices[-1], "green", graphSymbol="-")
    else:
        noProfitText = "No profit to be made"
        annotate_and_plot(noProfitText, smallestPriceTimeStamp, dailyPrices[-1],"red")

    plt.draw()

#Matplotlib
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)

axbox = fig.add_axes([0.1, 0.02, 0.8, 0.075])
text_box = TextBox(axbox, "Chart: ")
text_box.on_submit(submit)
text_box.set_val("bitcoin,eur,2020-3-1,2020-8-1")
plt.show()
