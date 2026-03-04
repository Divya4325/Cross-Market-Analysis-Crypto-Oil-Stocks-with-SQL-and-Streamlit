import streamlit as st
import sqlite3
import pandas as pd
def show():
   st.title("🔍SQL QUERY RUNNER")
   st.write("Predefined analtical SQL queries")
   conn=sqlite3.connect("Real_database.db")  
   queries={ 
      "Find the top 3 cryptocurrencies by market cap":
        "SELECT name,symbol FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3;",
      "List all coins where circulating supply exceeds 90% of total supply":
        "SELECT name,symbol FROM cryptocurrencies WHERE total_supply>0 AND (circulating_supply*1.0/total_supply)>=0.9;",
       "Get coins that are within 10% of their all-time-high (ATH)":
         "SELECT name,symbol FROM cryptocurrencies WHERE ath>0 AND current_price>=ath*0.9;",
       "Find the average market cap rank of coins with volume above $1B":
         "SELECT AVG(market_cap_rank) FROM cryptocurrencies WHERE total_volume>100000000;",
      "Get the most recently updated coin": 
         "SELECT name,symbol FROM cryptocurrencies ORDER BY datetime(date) LIMIT 1",
       "Find the highest daily price of Bitcoin in the last 365 days":
         "SELECT MAX(price_inr) AS highest_price FROM crypto_prices WHERE coin_id='bitcoin'AND date BETWEEN DATE('2026-02-22','-1 year')  AND '2026-02-22'",
       "Calculate the average daily price of Ethereum in the past 1 year":
          "SELECT AVG(price_inr) FROM crypto_prices WHERE coin_id='ethereum' AND date BETWEEN DATE('2026-02-22','-1 year') AND '2026-02-22'",
       "Show the daily price trend of Bitcoin in March 2025":
          "SELECT date,price_inr AS bitcoin_price FROM crypto_prices WHERE coin_id='bitcoin'AND date BETWEEN'2025-03-01'AND'2025-03-31'ORDER BY date",
       "Find the coin with the highest averagean price over 1 year":
          "SELECT coin_id,AVG(price_inr) AS avg_price FROM crypto_prices WHERE date>= DATE('now','-1 year') GROUP BY coin_id ORDER BY avg_price DESC LIMIT 1",
        "Get the % change in Bitcoin's price between May 2024 and May 2025":
           "SELECT ((price_inr_may2025-price_inr_may2024)*100.0/ price_inr_may2025) AS percent_change FROM ( SELECT (SELECT price_inr FROM crypto_prices WHERE coin_id='bitcoin'AND date BETWEEN '2025-05-01'AND '2025-05-30'ORDER BY date DESC LIMIT 1) AS price_inr_may2025,(SELECT price_inr FROM crypto_prices WHERE coin_id='bitcoin'AND date BETWEEN '2024-05-01'AND '2024-05-31' ORDER BY date DESC LIMIT 1) AS price_inr_may2024) AS subquery_prices",
        "Find the highest oil price in the last 5 years":
           "SELECT MAX(price_inr) AS highest_price FROM oil_prices WHERE date>= DATE('now','-5 years')",
        "Get the average oil price per year":
           "SELECT strftime('%Y',date) AS year, AVG(price_inr) AS avg_price FROM oil_prices GROUP BY year ORDER BY year",
        "Show oil prices during COVID crash (March TO April 2020)":
            "SELECT date,price_inr FROM oil_prices WHERE date BETWEEN '2020-03-01' AND '2020-04-30'ORDER BY date",
        "Find the lowest price of oil in the last 10 years":
            "SELECT MIN(price_inr) AS lowest_price FROM oil_prices WHERE date>= DATE('now','-10 years')",
        "Calculate the volatility of oil prices (max-min difference per year)":    
            "SELECT strftime('%Y',date) AS year,MAX(price_inr)-MIN(price_inr) AS volatility FROM oil_prices GROUP BY year ORDER BY year",
        "Get all stock prices for a given ticker":
            "SELECT date,open,high,low,close,volume FROM stock_prices WHERE ticker='^IXIC'ORDER BY date",
        "Find the highest closing price for NASDAQ (^IXIC)":     
            "SELECT MAX(close) AS high_close_price FROM stock_prices WHERE ticker='^IXIC'",
        "List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)":
            "SELECT date,(high-low) AS intraday_diff FROM stock_prices WHERE ticker='^GSPC'ORDER BY intraday_diff DESC LIMIT 5",
        "Get monthly average closing price for each ticker":
            "SELECT ticker, strftime('%Y-%m',date) AS year_month,AVG(close) AS avg_close FROM stock_prices GROUP BY ticker,year_month ORDER BY ticker,year_month",
        "Get average trading volume of NSEI in 2024":
            "SELECT AVG(volume) AS avg_volume FROM stock_prices WHERE ticker='^NSEI'AND date BETWEEN '2024-01-01' AND '2024-12-31'",
        "Compare Bitcoin vs Oil average price in 2025":
            "SELECT ROUND(AVG(c.price_inr),2) AS bitcoin_avg_2025,ROUND(AVG(o.price_inr),2) AS oil_avg_2025 FROM crypto_prices c JOIN oil_prices o ON c.date=o.date WHERE c.coin_id='bitcoin'AND strftime('%Y',c.date)='2025'",
        "Compare Ethereum and NASDAQ daily prices for 2025":
            "SELECT  c.date, c.price_inr AS ethereum_price,s.close AS nasdaq_close FROM crypto_prices c JOIN stock_prices s  ON c.date=s.date WHERE c.coin_id='ethereum'  AND s.ticker='^IXIC'AND strftime('%Y',c.date)='2025'ORDER BY c.date",
        "Find days when oil price spiked and compare with Bitcoin price change":
            "WITH oil_changes AS(SELECT date, price_inr,ROUND((price_inr-LAG(price_inr) OVER (ORDER BY date))*100.0/LAG(price_inr) OVER (ORDER BY date),2) AS oil_pct_change FROM oil_prices),btc_changes AS( SELECT date, price_inr,ROUND((price_inr-LAG(price_inr)OVER(ORDER BY date))*100.0/LAG(price_inr) OVER (ORDER BY date),2) AS btc_pct_change FROM crypto_prices WHERE coin_id='bitcoin') SELECT o.date, o.oil_pct_change,b.btc_pct_change FROM oil_changes o JOIN btc_changes b ON o.date=b.date WHERE o.oil_pct_change >3 ORDER BY o.date ",
        "Compare top 3 coins daily price trend vs Nifty (^NSEI)":
            "SELECT c.date, c.price_inr AS crypto_price,s.close AS nifty_price FROM crypto_prices c JOIN stock_prices s ON c.date=s.date WHERE c.coin_id IN ('bitcoin','ethereum','tether') AND s.ticker='^NSEI' ORDER BY c.date",
        "Compare stock prices (^GSPC) with crude oil prices on the same dates":
            "SELECT s.date,s.close AS sp500_price,o.price_inr AS crude_oil_price FROM stock_prices s JOIN oil_prices o ON s.date=o.date  WHERE s.ticker='^GSPC' ORDER BY s.date",
        "Compare NASDAQ (^IXIC) with Ethereum price trends":
            "SELECT s.date, s.close AS nasdaq_price, c.price_inr AS ethereum_price FROM stock_prices s JOIN crypto_prices c ON s.date=c.date WHERE s.ticker='^IXIC' AND c.coin_id='ethereum' ORDER BY s.date",
        "Join top 3 crypto coins with stock indices for 2025":
            "SELECT c.date AS crypto_date,c.coin_id,c.price_inr AS coin_price,s.date AS stock_date,s.close AS stock_close_price FROM crypto_prices c JOIN stock_prices s ON c.date=s.date WHERE c.coin_id IN ('bitcoin','ethereum','tether') AND s.ticker IN ('^GSPC','^IXIC','^NSEI') AND strftime('%Y',c.date)='2025'ORDER BY c.date",
        "Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison":
            "SELECT s.date,s.close AS stock_price, o.price_inr as oil_price,c.price_inr AS bitcoin_price FROM stock_prices s JOIN oil_prices o ON s.date=o.date JOIN crypto_prices c ON s.date=c.date  WHERE s.ticker ='^GSPC' AND c.coin_id ='bitcoin' ORDER BY s.date",    
      }
   st.subheader("Select a query")
   selected_query=st.selectbox("Total 30 queries",list(queries.keys())+
                               [
                                "Check if Bitcoin moves with S&P 500 (correlation idea)",
                                "Correlate Bitcoin closing price with crude oil closing price (same date)"      
                               ])
   if st.button("Run Query"):  
      try:
        if selected_query in queries:
           query=queries[selected_query]
           df=pd.read_sql(query,conn)
           if df.empty:
            st.warning("No data found")
           else:
            st.dataframe(df)
            st.success("Query executed Successfully")
            st.info("💡These queries are executed directly on the SQL database")
        elif selected_query == "Check if Bitcoin moves with S&P 500 (correlation idea)":
           query ="""
           SELECT c.date,
           c.price_inr AS bitcoin_price,
           s.close AS sp500_price FROM crypto_prices c 
           JOIN stock_prices s ON c.date=s.date 
           WHERE c.coin_id='bitcoin' 
           AND s.ticker='^GSPC'ORDER BY c.date
          """
           df=pd.read_sql(query,conn)
           correlation=df["bitcoin_price"].corr(df["sp500_price"])
           if pd.isna(correlation):
              st.warning("Correlation result is NaN")
           else:
             st.success(f"Correlation:{round(correlation,3)}")
             st.dataframe(df)
        elif selected_query =="Correlate Bitcoin closing price with crude oil closing price (same date)":
          query="""
           SELECT c.date,
           c.price_inr AS bitcoin_price,
           o.price_inr AS oil_price FROM crypto_prices c 
           JOIN oil_prices o 
           ON c.date=o.date 
           WHERE c.coin_id='bitcoin'ORDER BY c.date """  
          df=pd.read_sql(query,conn)
          correlation=df["bitcoin_price"].corr(df["oil_price"])
          if pd.isna(correlation):
              st.warning("Correlation result is NaN")
          else:               
            st.success(f"Correlation:{round(correlation,3)}") 
            st.dataframe(df) 
      except Exception as e:
          st.error(f"Error:{e}")
                 
            
    
                            
                            



     

