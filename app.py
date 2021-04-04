import streamlit as st
import pandas as pd
import yfinance as yf 
st.title('Stocks')
st.title('Category')



#option = st.sidebar.selectbox("Which Dashboard?", ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'pattern'), 3)

#if option == 'chart':
#    symbol = st.sidebar.text_input("Symbol", value='MSFT', max_chars=None, key=None, type='default')
#    df = pd.read_csv('ETF.csv')
#    st.dataframe(df.style.highlight_max())
    
    
#st.header(option)

option = st.sidebar.selectbox("Which Dashboard?", ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'pattern'), 3)

st.header(option)


if option == 'chart':
    symbol = st.sidebar.text_input("Symbol", value='MSFT', max_chars=None, key=None, type='default')

    data = yf.Ticker(symbol)
    data = data.history(period="1y")
    #st.subheader(symbol.upper())

    #fig = go.Figure(data=[go.Candlestick(x=data['day'],
    #                open=data['open'],
    #                high=data['high'],
    #                low=data['low'],
    #                close=data['close'],
    #                name=symbol)])
    #fig = data.plot()
    #fig.update_xaxes(type='category')
    #fig.update_layout(height=700)

    st.line_chart(data.Close)

    st.write(data)