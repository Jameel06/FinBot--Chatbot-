from groq import Groq
import os
from dotenv import load_dotenv
import yfinance as yf
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are FinBot, an expert AI assistant specialized in personal finance for Indian users.

You help users with:
- Mutual Funds and SIP (Systematic Investment Plan)
- Stock Market basics and investing tips
- Personal budgeting and saving strategies
- Tax planning and GST basics
- Fixed Deposits, PPF, NPS and other investment options
- Insurance and financial planning

Rules:
- Always give answers in simple, easy to understand language
- Use Indian context (₹, Indian tax laws, NSE/BSE, SEBI)
- Keep answers concise but complete
- If asked non-finance questions, politely redirect to finance topics
- Always add a small disclaimer for investment advice
- If user asks for live stock price, the system will automatically fetch it
"""

# Map common Indian stock names to Yahoo Finance tickers
STOCK_MAP = {
    "tcs": "TCS.NS",
    "tata consultancy": "TCS.NS",
    "infosys": "INFY.NS",
    "infy": "INFY.NS",
    "reliance": "RELIANCE.NS",
    "hdfc bank": "HDFCBANK.NS",
    "hdfc": "HDFCBANK.NS",
    "icici bank": "ICICIBANK.NS",
    "icici": "ICICIBANK.NS",
    "wipro": "WIPRO.NS",
    "sbi": "SBIN.NS",
    "state bank": "SBIN.NS",
    "bajaj finance": "BAJFINANCE.NS",
    "bajaj": "BAJFINANCE.NS",
    "adani": "ADANIENT.NS",
    "kotak": "KOTAKBANK.NS",
    "axis bank": "AXISBANK.NS",
    "axis": "AXISBANK.NS",
    "larsen": "LT.NS",
    "l&t": "LT.NS",
    "maruti": "MARUTI.NS",
    "asian paints": "ASIANPAINT.NS",
    "hul": "HINDUNILVR.NS",
    "hindustan unilever": "HINDUNILVR.NS",
    "itc": "ITC.NS",
    "titan": "TITAN.NS",
    "nestle": "NESTLEIND.NS",
    "ongc": "ONGC.NS",
    "ntpc": "NTPC.NS",
    "powergrid": "POWERGRID.NS",
    "sunpharma": "SUNPHARMA.NS",
    "sun pharma": "SUNPHARMA.NS",
    "drreddy": "DRREDDY.NS",
    "dr reddy": "DRREDDY.NS",
    "cipla": "CIPLA.NS",
    "ultratech": "ULTRACEMCO.NS",
    "nifty": "^NSEI",
    "sensex": "^BSESN",
}

def detect_stock(user_message):
    """Detect if user is asking about a stock price"""
    msg = user_message.lower()
    
    # Check if message is about price
    price_keywords = ["price", "rate", "trading", "stock price", "share price",
                  "current price", "latest price", "today price", "how much",
                  "latest", "current", "today", "now", "live"]
    is_price_query = any(kw in msg for kw in price_keywords)
    
    if not is_price_query:
        return None
    
    # Match stock name
    for name, ticker in STOCK_MAP.items():
        if name in msg:
            return ticker
    return None

def get_live_price(ticker):
    """Fetch live stock price from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        name = info.get("longName") or info.get("shortName") or ticker
        change = info.get("regularMarketChangePercent", 0)
        
        if price:
            direction = "📈" if change >= 0 else "📉"
            return (f"**{name}** ({ticker})\n\n"
                   f"💰 Current Price: ₹{price:,.2f}\n"
                   f"{direction} Change: {change:+.2f}%\n\n"
                   f"*Live data from NSE via Yahoo Finance*\n\n"
                   f"⚠️ Disclaimer: Stock prices fluctuate. Please do your own research before investing.")
        return None
    except:
        return None

def get_response(messages):
    """Get AI response, with live stock price if needed"""
    
    # Check last user message for stock price query
    last_message = messages[-1]["content"] if messages else ""
    ticker = detect_stock(last_message)
    
    if ticker:
        live_data = get_live_price(ticker)
        if live_data:
            return live_data
    
    # Otherwise get normal AI response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        temperature=0.7,
        max_tokens=1024
    )
    return response.choices[0].message.content