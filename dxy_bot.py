import os
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CEILING = 101.001

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=20)

def get_dxy_price():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB"
    params = {"range": "5d", "interval": "1h"}
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, params=params, headers=headers, timeout=20)
    data = r.json()
    result = data['chart']['result'][0]
    closes = result['indicators']['quote'][0]['close']
    opens = result['indicators']['quote'][0]['open']
    for i in range(len(closes)-1, -1, -1):
        if closes[i] is not None and opens[i] is not None:
            return closes[i], opens[i]
    return None, None

last_price, open_price = get_dxy_price()
if last_price:
    is_green = last_price > open_price
    color = "GREEN 🟢" if is_green else "RED 🔴"
    print(f"{datetime.now()}: DXY {last_price:.3f} {color}")
    if last_price > CEILING and is_green:
        send_telegram(f"🚀 BREAKOUT DXY {last_price:.3f} > {CEILING} {color}\nBUY USDCAD 0.02")
    elif last_price >= (CEILING - 0.15) and not is_green:
        send_telegram(f"🔴 REJECTION at {CEILING}\nDXY {last_price:.3f} {color}\nSELL USDCAD / BUY EURUSD 0.02")