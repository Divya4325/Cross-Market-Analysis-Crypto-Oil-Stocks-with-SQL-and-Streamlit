import streamlit as st
import sqlite3
import pandas as pd
def show():
    st.title("🪙Top 3 Crypto Analyasis")
    st.caption("Daily price analysis for top cryptocurrencies")
    conn=sqlite3.connect("Real_database.db")
    st.subheader("Select a Cryptocurrency")
    coin_list=pd.read_sql("SELECT DISTINCT coin_id FROM crypto_prices;",conn)
    selected_coin=st.selectbox("Top 3 Coin List",coin_list["coin_id"])
    col1,col2=st.columns(2)
    with col1:
         start_date=st.date_input(
     "Start Date")
    with col2:
        end_date=st.date_input(
       "End date"
     )
    if start_date and end_date:
        query=f"""
           SELECT date,price_inr
           FROM crypto_prices
           WHERE coin_id=('{selected_coin}')
           AND date BETWEEN '{start_date}' AND '{end_date}'
           ORDER BY date;
        """   
        df=pd.read_sql(query,conn) 
        if df.empty:
            st.warning("No data found for selected range")
        else:
          df["date"]=pd.to_datetime(df["date"])
          df=df.set_index("date")
          df["price_inr"]=df["price_inr"]
          df=df.reset_index()
          df.rename(columns={"index":"date"},inplace=True)
          df["date"]=df["date"].dt.strftime("%Y-%m-%d")
          st.dataframe(df)  