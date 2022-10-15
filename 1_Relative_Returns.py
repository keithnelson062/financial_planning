import streamlit as st
import pandas as pd 
import yfinance as yf
import plotly.express as px
import requests as req

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)

st.sidebar.success("Select a page above.")



# import plotly.graph_objects as go
# get the tickers of commonly known stocks from the wedb and store them in a list all capitalized
def get_tickers():
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv')
    tickers = df['Symbol'].tolist()
    tickers = [ticker.upper() for ticker in tickers]
    index_sector = ['XLK', 'XLF', 'XLY', 'XLP', 'XLE', 'XLB', 'XLI', 'XLV', 'XLU', 'XLRE']

    tickers = tickers + index_sector 
    # reomve duplicates
    tickers = list(dict.fromkeys(tickers))
    return tickers


st.title('Stock Market Analysis')
start_date = st.date_input('Start Date', pd.to_datetime('2010-01-01'))
end_date = st.date_input('End Date', pd.to_datetime('today'))
dropmenu = st.multiselect('Select the stocks you want to analyze', get_tickers())

def relative_return(df):
    
    df = df['Adj Close'].pct_change()
    cumret = (1 + df).cumprod()-1
    cumret = cumret.fillna(0)
    # combine all dataframes into one
    
    return cumret


@st.cache
def get_data(ticker):

    data = yf.download(ticker, start = start_date, end = end_date)
    return data

def get_news(tickers):
    news = []
    for ticker in tickers:
        # get company name from ticker
        company = yf.Ticker(ticker)
        company_name = company.info['longName']

    # use the requests module to get recent news based on the ticker data
        # get the current date: YYYY-MM-DD
        today = pd.to_datetime('today').strftime('%Y-%m-%d') 
        url = f'https://newsapi.org/v2/everything?q={company_name}&from={today}&sortBy=publishedAt&apiKey=cead143d5bdf4446aa18a8a3a26b2607'
        response = req.get(url)
        data = response.json()
        news.append(data)
    return news
    
    
    # create a dataframe from the news list

if len(dropmenu) > 0:
    data = get_data(dropmenu)
    st.header("Relative Returns")
    # display charts with 1.5 width and center the x placement
    # change plotly chart y axis title to relative returns
    st.plotly_chart(px.line(relative_return(data), title = 'Relative Returns', labels = {'value': 'Relative Returns', 'variable': 'Date'}), use_container_width = True, width = 1.5)
    # use the get_news function to get the news for the tickers selected and display them
    news = get_news(dropmenu)
    for ticker in news:
            st.write( dropmenu[news.index(ticker)] + ' : '+ ticker['articles'][0]['description'])

else:
    st.write('Select the stocks you want to analyze')


    

