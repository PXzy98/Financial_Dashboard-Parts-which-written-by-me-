import yfinance as yf
from datetime import date
import matplotlib.dates as mdate
from matplotlib.pyplot import MultipleLocator
from dateutil.relativedelta import relativedelta
import pandas as pd
import matplotlib.pyplot as plt


def getMonthTrans(code):
    list_of_months = []
    today = date.today()
    today = today.replace(day=1)
    lastYear = today - relativedelta(years = 1)
    starttime = lastYear.strftime("%Y-%m-%d")
    endtime = today.strftime("%Y-%m-%d")
    data = yf.download(code, start=starttime, end=endtime, group_by='tickers')
    if data.empty:
        return []
    allInfoMonthlist = data.values.tolist()
    dateofstats = data.index.tolist()
    for i in range(len(allInfoMonthlist)):
        list_of_months.append([dateofstats[i],allInfoMonthlist[i][3]])
    # .strftime("%Y-%m-%d")
    return list_of_months

def getWeekTrans(code):
    list_of_week = []
    today = date.today()
    lastMonth = today - relativedelta(weeks = 1)
    starttime = lastMonth.strftime("%Y-%m-%d")
    endtime = today.strftime("%Y-%m-%d")
    data = yf.download(code, start=starttime, end=endtime, group_by='tickers')
    if data.empty:
        return None
    allInfoweeklist = data.values.tolist()
    dateofstats = data.index.tolist()
    for i in range(len(allInfoweeklist)):
        list_of_week.append([dateofstats[i],allInfoweeklist[i][3]])

    return list_of_week

def getnewestInfo(code):
    newestInfoList = []
    today = date.today()
    lastMonth = today - relativedelta(months = 1)
    starttime = lastMonth.strftime("%Y-%m-%d")
    endtime = today.strftime("%Y-%m-%d")
    try:
        data = yf.download(code, start=starttime, end=endtime, group_by='tickers')

        if data.tail(1).empty :
            return None
        else:
            new = data.tail(1).values.tolist()
            for i in range(6):
                newestInfoList.append(new[0][i])
            return newestInfoList
    except KeyError:
        return None


def getRequiredData(code,starttime,endtime):
    data = yf.download(code, start=starttime, end=endtime, group_by='tickers')
    if data.empty:
        return None
    list_of_months = []
    allInfoMonthlist = data.values.tolist()
    for i in range(len(allInfoMonthlist)):
        list_of_months.append(allInfoMonthlist[i][3])

    return list_of_months


def SheetContent(codeList):
    contentList = []
    for i in range(len(codeList)):
        singlecontent = []
        if getnewestInfo(codeList[i][1]) is None:
            singlecontent.append(codeList[i][0])
            print(getnewestInfo(codeList[i][1]),"is None")
            for n in range(5):
                singlecontent.append("network issue")
            contentList.append(singlecontent)
        else:
            singlecontent.append(codeList[i][0])
            for n in getnewestInfo(codeList[i][1]):
                singlecontent.append(n)
            contentList.append(singlecontent)
    return contentList


def createMonthplot(list,title):
    if len(list) == 0:
        return None
    x= []
    y = []
    for i in range(len(list)) :
        x.append(list[i][0])
        y.append(list[i][1])
    fig1 = plt.figure(figsize=(10,7))
    locator = mdate.MonthLocator()
        # .YearLocator()
    ax1 = fig1.add_subplot(1,1,1)
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(locator)
    # x_major_locator=MultipleLocator(5)

    # y_major_locator=MultipleLocator(10)
    # ax=plt.gca()
    # ax1.xaxis.set_major_locator(x_major_locator)
    # ax.xaxis.set_major_formatter
    # ax.yaxis.set_major_locator(y_major_locator)
    xticklabels=1
    plt.title(title)
    plt.plot(x,y)
    plt.xticks(rotation=90,fontsize = 10)
    plt.subplots_adjust(left=0.1, bottom=0.2, right=None, top=0.9, wspace=None, hspace=0.5)
    plt.show()

def createWeekplot(list,title):
    if len(list) == 0:
        return None
    x= []
    y = []
    for i in range(len(list)) :
        x.append(list[i][0])
        y.append(list[i][1])
    fig1 = plt.figure(figsize=(10,7))
    locator = mdate.DayLocator()
        # .YearLocator()
    ax1 = fig1.add_subplot(1,1,1)
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(locator)
    # x_major_locator=MultipleLocator(5)

    # y_major_locator=MultipleLocator(10)
    # ax=plt.gca()
    # ax1.xaxis.set_major_locator(x_major_locator)
    # ax.xaxis.set_major_formatter
    # ax.yaxis.set_major_locator(y_major_locator)
    xticklabels=1
    plt.title(title)
    plt.plot(x,y)
    plt.xticks(rotation=90,fontsize = 10)
    plt.subplots_adjust(left=0.1, bottom=0.2, right=None, top=0.9, wspace=None, hspace=0.5)
    plt.show()
