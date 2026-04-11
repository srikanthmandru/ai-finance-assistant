from datetime import datetime, timezone
from typing import Dict, List

import yfinance as yf

from src.tools.cache_manager import CacheManager


class MarketDataTool:
    def __init__(self, ttl_seconds: int = 1800):
        self.cache = CacheManager(ttl_seconds=ttl_seconds)

    def _extract_ticker(self, query: str) -> str:
        tokens = query.upper().split()
        for token in tokens:
            clean = token.strip(",.?!")
            if 1 <= len(clean) <= 5 and clean.isalpha():
                return clean
        raise ValueError("Could not identify ticker symbol from query.")

    def _build_summary(self, data: Dict) -> str:
        return (
            f"{data['ticker']} price is ${data['current_price']:.2f}. "
            f"Day change is {data['change_percent']:.2f}%. "
            f"Data source: yFinance. "
            f"Last updated: {data['fetched_at']} UTC."
        )

    def get_quote(self, ticker: str) -> Dict:
        cache_key = f"quote:{ticker}"
        cached = self.cache.get(cache_key)
        if cached:
            cached["from_cache"] = True
            return cached

        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")

        if hist.empty:
            raise ValueError(f"No market data found for ticker: {ticker}")

        current_price = float(hist["Close"].iloc[-1])
        prev_close = float(hist["Close"].iloc[-2]) if len(hist) > 1 else current_price
        change_percent = ((current_price - prev_close) / prev_close * 100) if prev_close else 0.0

        result = {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "previous_close": round(prev_close, 2),
            "change_percent": round(change_percent, 2),
            "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "from_cache": False,
        }
        result["summary"] = self._build_summary(result)

        self.cache.set(cache_key, result)
        return result

    def get_history(self, ticker: str, period: str = "1mo") -> List[Dict]:
        cache_key = f"history:{ticker}:{period}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            raise ValueError(f"No historical data found for ticker: {ticker}")

        records = []
        for idx, row in hist.iterrows():
            records.append(
                {
                    "date": str(idx.date()),
                    "open": round(float(row["Open"]), 2),
                    "high": round(float(row["High"]), 2),
                    "low": round(float(row["Low"]), 2),
                    "close": round(float(row["Close"]), 2),
                    "volume": int(row["Volume"]),
                }
            )

        self.cache.set(cache_key, records)
        return records

    def get_market_summary(self, query: str) -> Dict:
        try:
            ticker = self._extract_ticker(query)
            return self.get_quote(ticker)
        except Exception:
            return {
                "ticker": "UNKNOWN",
                "current_price": 0.0,
                "previous_close": 0.0,
                "change_percent": 0.0,
                "fetched_at": "N/A",
                "from_cache": False,
                "summary": (
                    "Live market data is currently unavailable. "
                    "Please try again later. This assistant provides educational information only."
                ),
            }