#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 19:31:40 2023

@author: lisarose
"""

import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd
import pickle
import requests
from collections import Counter
import csv
import time
import yfinance as yf
import random
import imghdr
from email.message import EmailMessage
import smtplib
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pandas_datareader import data as pdr
from datetime import datetime

# Overall dependencies
yf.pdr_override()

start = dt.datetime(2010, 1, 1)
now = dt.datetime.now()
rnd_sec = random.randrange(1, 3)  # live
Breakout_list = pd.DataFrame(columns=['Stock', "Adj Close", "Current Price", "Target Price", "TP Date"])
alerted_stocks = pd.DataFrame(columns=['Symbols'])
count = 0
BO_count = 0
file_count = 1

df = pd.read_csv('sp500_list.csv')
#df = pd.read_csv('Otc_list.csv')
# df = pd.read_csv('ASE_list.csv')
# df = pd.read_csv('penny_list.csv')

# Risk management dependencies
AvgGain = 10
AvgLoss = 5
smaUsed = [50, 200]
emaUsed = [21]

# EMAIL outside def info
Email_Address = "Crrose1206@gmail.com"
Email_Password = "ddjshvjdddtlklxf"
msg = EmailMessage()
Targt = 50
signal = False
# Email description
msg["Subject"] = "Stock Movement Alert"
msg["From"] = Email_Address
msg["To"] = Email_Address


now = datetime.now()

print(now)

def pivots(stock):

    while stock != "quit":

        df = yf.download(stock, start, now)

        currentClose = df["Adj Close"][-1]

        df["High"].plot(label="high")  # prints out a depiction of the highs
        pivots = []
        dates = []
        counter = 0
        lastPivot = 0

        Range = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        dateRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Replaced for loop with a more efficient approach using iterrows
        for index, row in df.iterrows():
            currentMax = max(Range, default=0)
            value = round(row["High"], 2)

            Range = Range[1:9]  # this value to this value
            Range.append(value)  # appends the values of 10 days
            dateRange = dateRange[1:9]  # this value to this value
            dateRange.append(index)

            if currentMax == max(Range, default=0):
                counter += 1
            else:
                counter = 0
            if counter == 5:  # counts 5 days
                lastPivot = currentMax  # assign last pivot to max
                dateloc = Range.index(lastPivot)
                lastDate = dateRange[dateloc]

                pivots.append(lastPivot)
                dates.append(lastDate)
            print()

        timeD = dt.timedelta(days=30)
        if currentClose > lastPivot - (lastPivot * .05) and lastPivot + (lastPivot * .05) > currentClose:
            print(str(currentClose) + "::CC " + str(lastPivot) + "::LP")

            for index in range(len(pivots)):
                print(str(pivots[index]) + ": " + str(dates[index]))

                plt.title(str(stock), fontdict=None, loc='center', pad=None)
                plt.plot_date([dates[index], dates[index] + timeD],  # x values
                              [pivots[index], pivots[index]], linestyle="-", linewidth=2, marker=",")
            # plt.show()#creates the GUI
            if not os.path.exists('stock_plt'):
                os.makedirs('stock_plt')
            filename = str(stock)
            plt.savefig('stock_plt/{}'.format(filename))
            plt.show()

            return print("plotted!")
        else:

            return print(str(currentClose) + "::Currentclose " + str(lastPivot) + "::lastPivot ")
    
def pivots_call(stocks):
    df = pd.DataFrame(stocks)
    for stock in df["Symbols"][:len(df.index)]:
        print(pivots(stock))
    print("complete")

# Sends Email
def alert_(stock, TargetPrice, alerted):
    global alerted_stocks

    stock_info = yf.Ticker(stock)
    df = yf.download(stock, start, now)
    currentClose = df["Adj Close"][-1]
    print(str(currentClose) + " :: " + str(TargetPrice))
    condition = int(currentClose) > int(TargetPrice)
    TP_perc_upper = TargetPrice + (TargetPrice * .10)
    TP_perc_lower = TargetPrice - (TargetPrice * .10)
    condition = currentClose < TP_perc_upper and currentClose > TP_perc_lower
    if condition and not alerted:
        alerted = True
    
    else:
        print(" ")
        print("Symbol: '"+stock+"'' [Target Price: " + str(TargetPrice) + " Current Price: " + str(currentClose)+"]")
        print("No new alerts or above your PPS")
        time.sleep(5)

    pivots_call(alerted_stocks)
    
# Breakout Pricing
def Breakout_price(stock):
    global Breakout_list
    global count

    while stock != "quit":
        df = yf.download(stock, start, now)
        print("Loading " + stock + ".....")
        # time.sleep(rnd_sec)
        currentclose = df["Adj Close"][-1]
        df.drop(df[df["Volume"] < 1000].index, inplace=True)  # dropping any value that has volume less than 1000 shares a day
        dfDay = df.groupby(pd.Grouper(freq="D"))["High"].max()

        glDate = 0  # green line date of most recent GLV
        lastGLV = 0  # most recent GLV
        currentDate = ""  # curr date of GLV program is keeping track of
        currentGLV = 0  # curr GLV program is keeping track of
        counter = 0

        # ensure number of counters can reach 3
        for index, value in dfDay.items():

            if value > currentGLV:  # compares current GLV to value in index
                currentGLV = value
                currentDate = index
                counter = 0
            if value < currentGLV:
                counter = counter + 1

                if counter == 3:
                    if currentGLV != lastGLV:
                        print("Breakout price:: " + str(currentGLV) + " Breakout Date:: " + str(currentDate))
                        print("Previous Breakout price:: " + str(lastGLV) + " previous Breakout Date:: " + str(glDate))
                        print(" ")

                    glDate = currentDate
                    lastGLV = currentGLV
                    counter = 0

        if lastGLV == 0:
            message = stock + " has not formed a green line yet"
        else:
            message = (stock + " Current price " + str(currentclose) + " [Breakout_price: " + str(lastGLV) + " on " + str(glDate) + "]")

        # when merged " return lastGLV"
        count += 1

        Breakout_list = Breakout_list.append({'Stock': stock, "Current Price": currentclose, "Target Price": lastGLV, "TP Date": glDate}, ignore_index=True)

        return Breakout_list
        stock = "quit"

# Breakout caller
def stock_list(file, items):
    global alerted_stocks
    global BO_count

    max_price = 10
    df = pd.read_csv(file)
    num = int(items)

    for stock in df['Stock'][:items]:
        print("getting break out for: " + stock)
        if stock in alerted_stocks.values:
            print("list already has stock alert")
            print(alerted_stocks)
        else:
            Breakout_price(stock)

    file_name = "Breakout_list_" + str(BO_count) + ".csv"
    BO_count += 1
    df = pd.DataFrame(Breakout_list)
    try:
        df.to_csv(file_name)
    except:
        pass

    i = 0
    for stock in df['Stock'][:len(df.index)]:
        targ = df['Target Price'][i]
        curr = df['Current Price'][i]

        if curr > targ and curr < max_price:
            alerted_stocks = alerted_stocks.append({'Symbols': stock}, ignore_index=True)
            alert_(stock, int(targ), False)
        else:
            print("Current price is < Target or > Max price for: " + stock)
            print(str(curr) + "::Curr " + str(targ) + "::Targ " + str(max_price) + " ::Max Price")
        print(alerted_stocks)
        i += 1
# def Repeated_stocks(stock):

# Marks Mark Minervini’s trading strategy won him the U.S. investing championship (9 Conditions)
def Mark_Ms_Trend(stocklist):

    list_count = 1

    exportList = pd.DataFrame(columns=['Stock', "Adj Close", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])

    index_size = len(stocklist.index)

    count = 0
    for i in stocklist.index[:int(index_size)]:
        stock = str(stocklist["Symbols"][i])

        # Create an RS indicator to get the ratings
        RS_Rating = 71  # <---stocklist["RS Rating"][i]

        try:
            df = yf.download(stock, start, now)
            rnd_sec = random.randrange(1, 3)  # live
            count += 1
            print("Loading " + stock + "....." + str(count) + ":" + str(index_size))

            # Alternative
            # df = pdr.get_data_yahoo(stock,start,now)

            # Calculating these 3 different SMAs
            smaUsed = [50, 150, 200]
            for x in smaUsed:
                sma = x
                df["SMA_" + str(sma)] = round(df.iloc[:, 4].rolling(window=sma).mean(), 2)  # calculating all 3 very quickly

            currentClose = df["Adj Close"][-1]
            moving_avg_50 = df["SMA_50"][-1]
            moving_avg_150 = df["SMA_150"][-1]
            moving_avg_200 = df["SMA_200"][-1]
            low_of_52week = min(df["Adj Close"][-260:])  # taking the last 260 adj close and finding the min value
            high_of_52week = max(df["Adj Close"][-260:])  # taking the last 260 adj close and finding the max value
            high_of_month = max(df["Adj Close"][-20:])
            try:
                moving_avg_200_20past = df["SMA_200"][-20]

            except Exception:
                moving_avg_200_20past = 0

            try:
                high_of_month = max(df["Adj Close"][-20:])

            except Exception:
                high_of_month = 0

            # Condition 1: Current Price > 150 SMA and > 200 SMA
            if currentClose > moving_avg_150 and currentClose > moving_avg_200:
                cond_1 = True
            else:
                cond_1 = False
            print(cond_1)
            # Condition 2: 150 SMA and > 200 SMA
            if moving_avg_150 > moving_avg_200:
                cond_2 = True
            else:
                cond_2 = False
            # Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
            try:
                if moving_avg_200 > moving_avg_200_20past:
                    cond_3 = True
                else:
                    cond_3 = False
            except:
                cond_3 = False
            # Condition 4: 50 SMA > 150 SMA and 50 SMA > 200 SMA
            if moving_avg_50 > moving_avg_150 and moving_avg_50 > moving_avg_200:
                cond_4 = True
            else:
                cond_4 = False
            # Condition 5: Current Price > 50 SMA
            if currentClose > moving_avg_50:
    
                cond_5 = True
            else:
                cond_5 = False
            # Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)
            if currentClose >= (1.3 * low_of_52week):  # 1.3 is 30 percent
                cond_6 = True
            else:
                cond_6 = False
            # Condition 7: Current Price is within 25% of 52 week high
            if currentClose >= (.75 * high_of_52week):
                cond_7 = True
            else:
                cond_7 = False
            # Condition 8: IBD RS rating > 70 and the higher the better
            if RS_Rating > 70:
                cond_8 = True
            else:
                cond_8 = False
            # Condition 9: Current Price is trading above the 50 SMA as the stock is coming out of a base
            try:
                if currentClose > moving_avg_50 and currentClose >= high_of_month:
                    cond_9 = True
                else:
                    cond_9 = False
            except:
                cond_9 = False
    
            if cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6 and cond_7 and cond_8 and cond_9:
  # add cond_8 back when fixed
                exportList = exportList.append({'Stock': stock, "Adj Close": currentClose, "50 Day MA": moving_avg_50,
                                                "150 Day Ma": moving_avg_150, "200 Day MA": moving_avg_200,
                                                "52 Week Low": low_of_52week, "52 week High": high_of_52week, "High of Month": high_of_month}, ignore_index=True)
        except Exception:
            print("No data on " + stock)

    print(exportList)
    
    file_name = "list_" + str(list_count) + ".csv"
    df = pd.DataFrame(exportList)
    df.to_csv(file_name)
    
    #stock_list(file_name, len(df.index))
    
    
# Exponential moving average
#EMA = (Current price * (2 / (n + 1))) + (Previous EMA * (1 - (2 / (n + 1))))
def EMA_Reader(list_symb):
    global file_count
    bullish_symbols = pd.DataFrame(columns=['Symbols'])
    bearish_symbols = pd.DataFrame(columns=['Symbols'])
    consol_symbols = pd.DataFrame(columns=['Symbols'])
    df = list_symb  # symbol list
    cntr = 0
    file = 'Symbols_'+ str(file_count)
    amnt = len(list_symb.index)

    try:
        for stock in df.iloc[:amnt]['Symbols'].unique():
            stock = stock.upper()
            if '^' in stock:
                continue
            else:
                symbol = yf.Ticker(stock)

            startyear = 2010
            startmonth = 1
            startday = 1

            start = dt.datetime(startyear, startmonth, startday)
            now = dt.datetime.now()

            df_stock = yf.download(stock, start, now)

            print("Loading "+stock+".....")

            emasUsed = [3, 5, 8, 10, 12, 15, 30, 40, 45, 50, 60]

            if not os.path.exists('stock_EMAs'):
                os.makedirs('stock_EMAs')

            for x in emasUsed:
                ema = x
                df_stock['EMA_' + str(ema)] = round(df_stock.iloc[:, 4].ewm(span=ema, adjust=False).mean(), 2)

            df_stock = df_stock.iloc[60:]

            try:
                for i in df_stock.index:
                    cmin = min(df_stock['EMA_3'][i], df_stock['EMA_5'][i], df_stock['EMA_8'][i], df_stock['EMA_10'][i], df_stock['EMA_12'][i], df_stock['EMA_15'][i])
                    cmax = max(df_stock['EMA_30'][i], df_stock['EMA_40'][i], df_stock['EMA_45'][i], df_stock['EMA_50'][i], df_stock['EMA_60'][i])
                    close = df_stock['Adj Close'][i]
                    Open = df_stock['Open'][i]
        
                if (cmin > cmax):
                    print("BULLISH market for: " + stock)
                    print("[open: " + str(Open) + " current: " + str(close) + "]")
                    print(" ")
                    bullish_symbols = pd.concat([bullish_symbols, pd.DataFrame({'Symbols': [stock]})], ignore_index=True)
        
                elif (cmin < cmax):
                    print("BEARISH market for: " + stock)
                    print("[open: " + str(Open) + " current: " + str(close) + "]")
                    print(" ")
                    bearish_symbols = pd.concat([bearish_symbols, pd.DataFrame({'Symbols': [stock]})], ignore_index=True)
        
                elif (cmin == cmax):
                    print("CONSOLIDATING market for: " + stock)
                    print("[open: " + str(Open) + " current: " + str(close) + "]")
                    print(" ")
                    consol_symbols = pd.concat([consol_symbols, pd.DataFrame({'Symbols': [stock]})], ignore_index=True)
            except:
                print("stock passed!")
                pass
            print(str(cntr) + "::" + str(len(list_symb.index)))
            cntr += 1
            
            
    except:
        print("ERROR within For loop on: " )
        pass

    print("Bullish[ " + str(bullish_symbols) + "]")
    print(" ")
    print("loading...")
    
  

    Mark_Ms_Trend(bullish_symbols)
    
   


# Volume
def volume_indicator(list_symb):
    global file_count
    increase_symbols = pd.DataFrame(columns=['Symbols'])
    decrease_symbols = []
    neutral_symbols = []

    count_inc = 0
    count_dec = 0
    count_neu = 0
    amnt = len(list_symb.index)
    count = 1
    file = pd.read_csv('sp500_list.csv')

    for stock in file['Symbols'][:200]:
        try:
            print(str(count) + "::" + str(amnt))
            
            stock = stock.upper()
            if '^' in stock:
                continue
            else:
                stock_info = yf.Ticker(stock)
                hist = stock_info.history(period='3mo')
                print("Loading " + stock + " history....")
                rnd_sec = random.randrange(1, 2)
                time.sleep(rnd_sec)

                previous_avg_vol = hist['Volume'].mean()
                std_dev_vol = hist['Volume'].std()
                yesterdays_vol = hist['Volume'][-2]
                todays_vol = hist['Volume'][-1]
                day_vol = todays_vol

                inc_thresh = previous_avg_vol + .5 * std_dev_vol
                dec_thresh = previous_avg_vol - .5 * std_dev_vol

                count += 1

                # increased
                if yesterdays_vol > inc_thresh:
                    increase_symbols = pd.concat([increase_symbols, pd.DataFrame({'Symbols': [stock]})], ignore_index=True)
                    diff = yesterdays_vol - previous_avg_vol
                    perc_diff = diff / previous_avg_vol
                    count_inc += 1
                    print(stock + " has been appened for increase, [previous_avg: " + str(previous_avg_vol) + " day_avg: " + str(day_vol) + "]")
                    print("difference:" + str(diff) + " perc_change:" + str(perc_diff))
                    print(" ")

                # decreased
                elif yesterdays_vol< dec_thresh:
                    decrease_symbols.append(stock)
                    diff = previous_avg_vol - yesterdays_vol
                    perc_diff = diff / previous_avg_vol
                    count_dec += 1
                    print(stock + " has been appened for decreased, [previous_avg: " + str(previous_avg_vol) + " day_avg: " + str(day_vol) + "]")
                    print("difference:" + str(diff) + " perc_change:" + str(perc_diff))
                    print(" ")

                # neutral
                else:
                    neutral_symbols.append(stock)
                    print(stock + " has been appened for neutral")
                    print("[previous_avg: " + str(previous_avg_vol) + " yesterdays_avg: " + str(day_vol) + "]")
                    diff = previous_avg_vol - yesterdays_vol
                    if yesterdays_vol > previous_avg_vol:
                        perc_diff = (day_vol - previous_avg_vol) / previous_avg_vol
                    else:
                        perc_diff = diff / previous_avg_vol
                    print("perc_change: " + str(perc_diff))
                    count_neu += 1
                    print(" ")

        except:
            print("passed!")
            pass
            print("")


    print(str(count_inc) + " symbols")
    file_count += 1
    EMA_Reader(increase_symbols)

volume_indicator(df)

    
 