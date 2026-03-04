import streamlit as st
import sqlite3
import pandas as pd
conn=sqlite3.connect("Real_database.db")  
import query_runner
import coin
st.set_page_config(
    page_title="Market Analysis Dashboard"
    )
st.sidebar.title("Navigator")
page=st.sidebar.radio(
     "Go to",
     [
         "📊Market Overview",
         "📃SQL QUERY Runner",
         "🪙Top 3 Crypto Analysis"
     ]
)

if page=="📊Market Overview":
  st.title("📊 Cross-Market Overview")
  st.write("Crypto|Oil|Stock Market|SQL-powered analytics")
  col1,col2=st.columns(2) 
  with col1:
      start_date=st.date_input(
     "Start Date"
     )
  with col2:
      end_date=st.date_input(
       "End date"
     )
  if start_date and end_date:
      start_date=str(start_date)
      end_date=str(end_date)  
      query=f"""
        SELECT
     DATE(cp.date) as date,
     cp.price_inr as bitcoin_price,
     op.price_inr as oil_price,
     sp1.close as sp500,
     sp2.close as nifty
    FROM crypto_prices cp
    JOIN cryptocurrencies c
     ON cp.coin_id=c.id
    LEFT JOIN oil_prices op
     ON DATE(cp.date)=DATE(op.date)
    LEFT JOIN stock_prices sp1
     ON DATE(cp.date)=DATE(sp1.date) AND TRIM(sp1.ticker)='^GSPC'
    LEFT JOIN stock_prices sp2
     ON DATE(cp.date)=DATE(sp2.date) AND TRIM(sp2.ticker)='^NSEI'
    WHERE c.name='Bitcoin'
    AND DATE(cp.date) BETWEEN DATE('{start_date}') AND DATE('{end_date}')
    ORDER BY DATE(cp.date)DESC
    """
      df=pd.read_sql(query,conn)
      if not df.empty:
        btc_avg=df['bitcoin_price'].dropna().mean()
        oil_avg=df['oil_price'].dropna().mean()
        sp_avg=df['sp500'].dropna().mean()
        nifty_avg=df['nifty'].dropna().mean()
        col1,col2,col3,col4=st.columns(4)
        col1.metric("Bitcoin Avg(Rs)",round(btc_avg,2))
        col2.metric("Oil Avg(Rs)",round(oil_avg,2))
        col3.metric("S&P 500 Avg",round(sp_avg,2))
        col4.metric("NIFTY Avg",round(nifty_avg,2))
        st.subheader("Daily Market Snapshot")
        st.dataframe(df)
elif page=="📃SQL QUERY Runner":
    query_runner.show() 
elif page=="🪙Top 3 Crypto Analysis":
   coin.show()

  
