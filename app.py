import streamlit as st
import pandas as pd
import yfinance as yf 
import plotly.graph_objects as go
import math as m
import finviz
#st.title('Stocks')
#st.title('Category')



#option = st.sidebar.selectbox("Which Dashboard?", ('twitter', 'wallstreetbets', 'stocktwits', 'chart', 'pattern'), 3)

#if option == 'chart':
#    symbol = st.sidebar.text_input("Symbol", value='MSFT', max_chars=None, key=None, type='default')
#    df = pd.read_csv('ETF.csv')
#    st.dataframe(df.style.highlight_max())
    
    
#st.header(option)

option = st.sidebar.selectbox("Which Dashboard?", ('Stock Data','Balance Sheet','Income Statement','Cash Flow', 'stocktwits', 'chart', 'pattern'), 3)

st.header(option)


if option == 'chart':
    
    symbol = st.sidebar.text_input("Symbol", value='MSFT', max_chars=None, key=None, type='default')
    
    data = yf.Ticker(symbol)
    df = data.history(period="3mo")
    
    
    df['exp1'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['exp2'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['exp1']-df['exp2']
    df['exp3'] = df['macd'].ewm(span=9, adjust=False).mean()
    
    previous_15 = df['exp3'].shift(1)
    previous_45 = df['macd'].shift(1)
    Golden = df[((df['exp3'] <= df['macd']) & (previous_15 >= previous_45))]#.shift(1)
    #Golden['Average'] = (Golden['macd'] + Golden['exp3'])/2
    Death = df[((df['exp3'] >= df['macd']) & (previous_15 <= previous_45))]#.shift(1)
    #new = pd.DatetimeIndex(Golden.index) + pd.DateOffset(-1) 
    #Golden  = df[df.index.isin(new)]
    #Golden['Average'] = (Golden['macd'] + Golden['exp3'])/2
    #Death.index = pd.DatetimeIndex(Death.index) + pd.DateOffset(-1)
    
    fig = go.Figure()
    #fig.add_trace(go.Candlestick(x=df.index,open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],name = 'CandleStick')) #CandleStick
    fig.add_trace(go.Scatter(y = df['macd'], x = df.index,marker_color='red',name='Selling'))
    fig.add_trace(go.Scatter(y = df['exp3'], x = df.index,marker_color='green',name='Buying'))
    fig.add_trace(go.Scatter(x = Golden.index,y = Golden['macd'],mode='markers',marker_line_width=2, marker_size=10,name='Golden'))
    fig.add_trace(go.Scatter(x = Death.index,y = (Death['exp3']),mode='markers',marker_line_width=2, marker_size=10,name='Death'))
    fig.update_layout(autosize=False,width=1000)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Candlestick(x=df.index,open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],name = 'CandleStick'))
    fig2.update_layout(autosize=True,width=1000,yaxis_title='{} Stock'.format(symbol),xaxis_title='{} Price'.format(symbol))
    
    fig2.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), #hide weekends
                 dict(values=["2015-12-25", "2016-01-01"])])  # hide Christmas and New Year's]
    """fig2.show(config={'modeBarButtonsToAdd':['drawline',
                                        'drawopenpath',
                                        'drawclosedpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                       ]})"""
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x = df.index,y = df['Volume']))
    fig3.update_layout(autosize=True,width=1000,yaxis_title='{} Volume'.format(symbol),xaxis_title='{} Dates'.format(symbol))
    fig3.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"]), #hide weekends
                 dict(values=["2015-12-25", "2016-01-01"])])
    
    
    st.plotly_chart(fig2)#use_container_width = True)
    st.title('MACD')
    st.plotly_chart(fig)
    st.title('Volume')
    st.plotly_chart(fig3)
    #st.line_chart(df.Close)
    st.write(data)

if option == 'Stock Data':
    try:
        symbol = st.sidebar.text_input("Symbol", value='MSFT', max_chars=None, key=None, type='default')
        data = yf.Ticker(symbol)
        fin = finviz.get_stock(symbol)
        div = data.dividends
        div = pd.DataFrame(div)
        #div1 = div.T
        holder = data.institutional_holders
        col1, col2 = st.beta_columns(2)
        #print(len(div))
        #st.title('Dividend History')
        if len(div) != 0:
            col1.subheader('Dividend History')
            col2.title('')
            col1.bar_chart(div)
            col2.dataframe(div)
        else: 
            st.title('Dividend History')
            st.write('Company does not pay dividends')
        
        #st.bar_chart(div)
        #st.title('Dividend History')
        #st.dataframe(div)
        st.title('Instutional Holders')
        st.table(holder)
        
        #FinViz Information
        df = pd.DataFrame.from_dict(fin,orient ='index')
        df = df[0]
        df1 = pd.DataFrame(df)
        #df1.index = 'Info'
        df1.columns = ['Information']
        st.table(df1)
        #st.bar_chart(div)
    except:
        st.write('Please enter a valid input')
        
if option == 'Balance Sheet':
    ticker = st.sidebar.text_input("Symbol", value='MSFT', max_chars=None, key=None, type='default')
    df = pd.read_html('https://www.marketwatch.com/investing/stock/{}/financials/balance-sheet'.format(ticker))
    df1 =  pd.concat([df[4],df[5]])
    
    #Fixes the double name thing
    df2 = df1['Item  Item'].str.split(expand=True).reset_index()
    newnames = []
    for i in range(0,len(df1)):
        x = m.ceil(len(df2.loc[i].dropna())/2)
        s = df2.loc[i][1:x].tolist()
        newname = ' '.join(map(str, s))
        newnames.append(newname)
    df1['Item  Item'] = newnames
    df1.rename(columns = {"Item  Item": "Item"}, 
            inplace = True)
    
    maindf = df1
    maindf = maindf.set_index('{}'.format(maindf.columns[0])) #Makes first column the index 
    maindf = maindf.drop(columns = maindf.columns[len(maindf.columns)-1]) # Gets rid of last colsumn 
    maindf = maindf.replace('-',0)
    
    st.table(maindf)
    
if option == 'Income Statement':
    ticker = st.sidebar.text_input("Symbol", value='MSFT', max_chars=None, key=None, type='default')
    df = pd.read_html('https://www.marketwatch.com/investing/stock/{}/financials/cash-flow'.format(ticker))
    df1 =  pd.concat([df[4],df[5],df[6]])
    
    #Fixes the double name thing
    df2 = df1['Item  Item'].str.split(expand=True).reset_index()
    newnames = []
    for i in range(0,len(df1)):
        x = m.ceil(len(df2.loc[i].dropna())/2)
        s = df2.loc[i][1:x].tolist()
        newname = ' '.join(map(str, s))
        newnames.append(newname)
    df1['Item  Item'] = newnames
    df1.rename(columns = {"Item  Item": "Item"}, 
            inplace = True)
    
    maindf = df1
    maindf = maindf.set_index('{}'.format(maindf.columns[0])) #Makes first column the index 
    maindf = maindf.drop(columns = maindf.columns[len(maindf.columns)-1]) # Gets rid of last colsumn 
    maindf = maindf.replace('-',0)
    
    st.table(maindf)
if option == 'Cash Flow':
    ticker = st.sidebar.text_input("Symbol", value='MSFT', max_chars=None, key=None, type='default')
    df = pd.read_html('https://www.marketwatch.com/investing/stock/{}/financials/cash-flow'.format(ticker))
    df1 =  pd.concat([df[4],df[5],df[6]])
    
    df2 = df1['Item  Item'].str.split(expand=True).reset_index()
    newnames = []
    for i in range(0,len(df1)):
        x = m.ceil(len(df2.loc[i].dropna())/2)
        s = df2.loc[i][1:x].tolist()
        newname = ' '.join(map(str, s))
        newnames.append(newname)
    df1['Item  Item'] = newnames
    df1.rename(columns = {"Item  Item": "Item"}, 
            inplace = True)
    
    maindf = df1
    maindf = maindf.set_index('{}'.format(maindf.columns[0])) #Makes first column the index 
    maindf = maindf.drop(columns = maindf.columns[len(maindf.columns)-1]) # Gets rid of last colsumn 
    maindf = maindf.replace('-',0)
    
    st.table(maindf)