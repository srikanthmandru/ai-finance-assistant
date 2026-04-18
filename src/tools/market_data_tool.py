import os
import re
from datetime import datetime, timezone
from typing import Dict, List
import streamlit as st
import requests
import yfinance as yf
from dotenv import load_dotenv

from src.tools.cache_manager import CacheManager

load_dotenv()


class MarketDataTool:
    def __init__(self, ttl_seconds: int = 1800):
        self.cache = CacheManager(ttl_seconds=ttl_seconds)
        self.alpha_vantage_api_key = (
            os.getenv("ALPHA_VANTAGE_API_KEY")
            or st.secrets.get("ALPHA_VANTAGE_API_KEY")
        )
        self.alpha_vantage_url = "https://www.alphavantage.co/query"

    def _extract_ticker(self, query: str) -> str:
        tokens = re.findall(r"\b[A-Z]{1,5}\b", query.upper())
        common_words = {"WHAT", "IS", "THE", "PRICE", "OF", "STOCK", "MARKET", "SHOW"}
        tokens = [t for t in tokens if t not in common_words]

        if tokens:
            return tokens[0]

        raise ValueError("Could not identify ticker symbol from query.")

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    def _build_quote_summary(self, data: Dict) -> str:
        source = data.get("provider", "unknown")
        freshness = "cached" if data.get("from_cache") else "live"

        return (
            f"{data['ticker']} price is ${data['current_price']:.2f}. "
            f"Day change is {data['change_percent']:.2f}%. "
            f"Source: {source}. Data is {freshness}. "
            f"Last updated: {data['fetched_at']} UTC."
        )

    def _get_quote_yfinance(self, ticker: str) -> Dict:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d", interval="1d")

        if hist.empty:
            raise ValueError(f"No yfinance data found for {ticker}")

        current_price = float(hist["Close"].iloc[-1])
        prev_close = float(hist["Close"].iloc[-2]) if len(hist) > 1 else current_price
        change_percent = ((current_price - prev_close) / prev_close * 100) if prev_close else 0.0

        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "previous_close": round(prev_close, 2),
            "change_percent": round(change_percent, 2),
            "provider": "yfinance",
            "fetched_at": self._timestamp(),
            "from_cache": False,
        }

    def _get_quote_alpha_vantage(self, ticker: str) -> Dict:
        if not self.alpha_vantage_api_key:
            raise ValueError("Alpha Vantage API key not configured.")

        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self.alpha_vantage_api_key,
        }
        response = requests.get(self.alpha_vantage_url, params=params, timeout=20)
        response.raise_for_status()
        payload = response.json()

        quote = payload.get("Global Quote", {})
        if not quote or "05. price" not in quote:
            if "Note" in payload:
                raise ValueError(f"Alpha Vantage rate limit hit: {payload['Note']}")
            raise ValueError(f"No Alpha Vantage quote found for {ticker}")

        current_price = float(quote["05. price"])
        prev_close = float(quote.get("08. previous close", current_price))
        change_percent = float(quote.get("10. change percent", "0%").replace("%", ""))

        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "previous_close": round(prev_close, 2),
            "change_percent": round(change_percent, 2),
            "provider": "alpha_vantage",
            "fetched_at": self._timestamp(),
            "from_cache": False,
        }

    def get_quote(self, ticker: str) -> Dict:
        cache_key = f"quote:{ticker}"
        cached = self.cache.get(cache_key)
        if cached:
            return {**cached, "from_cache": True}

        errors = []

        for provider in (self._get_quote_alpha_vantage, self._get_quote_yfinance):
            try:
                result = provider(ticker)
                result["summary"] = self._build_quote_summary(result)
                self.cache.set(cache_key, result)
                return result
            except Exception as exc:
                errors.append(str(exc))

        raise ValueError(" ; ".join(errors))

    def get_history(self, ticker: str, period: str = "1mo") -> List[Dict]:
        cache_key = f"history:{ticker}:{period}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            raise ValueError(f"No historical data found for {ticker}")

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
        ticker = self._extract_ticker(query)
        return self.get_quote(ticker)

    def get_portfolio_market_summary(self, tickers: List[str]) -> Dict:
        seen = []
        for t in tickers:
            if t and t not in seen:
                seen.append(t)

        quotes = []
        for ticker in seen[:5]:
            try:
                quotes.append(self.get_quote(ticker))
            except Exception:
                continue

        if not quotes:
            return {
                "summary": (
                    "Live market data is currently unavailable for the portfolio. "
                    "Please try again later."
                ),
                "quotes": [],
            }

        lines = [
            f"{q['ticker']}: ${q['current_price']:.2f} ({q['change_percent']:.2f}%)"
            for q in quotes
        ]

        return {
            "quotes": quotes,
            "summary": "Portfolio market snapshot:\n" + "\n".join(lines),
        }