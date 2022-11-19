'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 
This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def Get_Stock_API(StockSymbol,TimeSeries):

    #Convert Time Series number into str for api to use
    TimeSeries = int(TimeSeries)
    if(TimeSeries == 1):
        function = "TIME_SERIES_INTRADAY"
    elif(TimeSeries == 2):
        function = "TIME_SERIES_DAILY_ADJUSTED"
    elif(TimeSeries == 3):
        function = "TIME_SERIES_WEEKLY"
    elif(TimeSeries == 4):
        function = "TIME_SERIES_MONTHLY"

    url = "https://www.alphavantage.co/query?function="+function+"&symbol="+StockSymbol+"&outputsize=full&interval=30min&apikey=RZM5VGNEZOCKLLTT"

    r = requests.get(url).json()
    return r

def GenerateChart(symbol,chart_type,time_series,start_date,end_date):
    data = Get_Stock_API(symbol,time_series)

    TimeDateList = []
    OpenList = []
    HighList = []
    LowList = []
    CloseList = []
    
    try:
        if(time_series == '1'): 
            for i in data['Time Series (30min)']:
                current_date = convert_date(i[:10])
                if((current_date>=start_date)&(current_date<=end_date)):
                    TimeDateList.append(i)
                    OpenList.append(float(data['Time Series (30min)'][i]['1. open']))
                    HighList.append(float(data['Time Series (30min)'][i]['2. high']))
                    LowList.append(float(data['Time Series (30min)'][i]['3. low']))
                    CloseList.append(float(data['Time Series (30min)'][i]['4. close']))
        elif(time_series == '2'): 
            for i in data['Time Series (Daily)']:
                current_date = convert_date(i[:10])
                if((current_date>=start_date)&(current_date<=end_date)):
                    TimeDateList.append(i)
                    OpenList.append(float(data['Time Series (Daily)'][i]['1. open']))
                    HighList.append(float(data['Time Series (Daily)'][i]['2. high']))
                    LowList.append(float(data['Time Series (Daily)'][i]['3. low']))
                    CloseList.append(float(data['Time Series (Daily)'][i]['4. close']))
        elif(time_series == '3'): 
            for i in data['Weekly Time Series']:
                current_date = convert_date(i[:10])
                if((current_date>=start_date)&(current_date<=end_date)):
                    TimeDateList.append(i)
                    OpenList.append(float(data['Weekly Time Series'][i]['1. open']))
                    HighList.append(float(data['Weekly Time Series'][i]['2. high']))
                    LowList.append(float(data['Weekly Time Series'][i]['3. low']))
                    CloseList.append(float(data['Weekly Time Series'][i]['4. close']))
        else:
            for i in data['Monthly Time Series']:
                current_date = convert_date(i[:10])
                if((current_date>=start_date)&(current_date<=end_date)):
                    TimeDateList.append(i)
                    OpenList.append(float(data['Monthly Time Series'][i]['1. open']))
                    HighList.append(float(data['Monthly Time Series'][i]['2. high']))
                    LowList.append(float(data['Monthly Time Series'][i]['3. low']))
                    CloseList.append(float(data['Monthly Time Series'][i]['4. close']))
    except KeyError:
        line_chart = pygal.Line()
        line_chart.title = "ERROR: Stock name not in API"
        return line_chart.render_data_uri()

    
    TimeDateList.reverse()
    OpenList.reverse()
    HighList.reverse()
    LowList.reverse()
    CloseList.reverse()

    if(chart_type == '2'):
        line_chart = pygal.Line()
        line_chart.title = "Stock Data for " + symbol +": " + start_date.strftime("%Y-%m-%d") + " to " + end_date.strftime("%Y-%m-%d")
        line_chart.x_labels = TimeDateList
        line_chart.add("Open", OpenList)
        line_chart.add("High", HighList)
        line_chart.add("Low", LowList)
        line_chart.add("Close", CloseList)
        return line_chart.render_data_uri()
    else:
        bar_chart = pygal.Bar()
        bar_chart.title = "Stock Data for " + symbol +": " + start_date.strftime("%Y-%m-%d") + " to " + end_date.strftime("%Y-%m-%d")
        bar_chart.x_labels = TimeDateList
        bar_chart.add("Open", OpenList)
        bar_chart.add("High", HighList)
        bar_chart.add("Low", LowList)
        bar_chart.add("Close", CloseList)
        return bar_chart.render_data_uri()