# src/utils/input_parser.py
import re
from typing import Dict, List


def parse_portfolio_from_query(query: str) -> Dict:
    """
    Example:
    'Analyze this portfolio: 10 VTI at 250, 5 AAPL at 190'
    """
    pattern = r'(\d+(?:\.\d+)?)\s+([A-Za-z]{1,5})\s+(?:at|@)\s+(\d+(?:\.\d+)?)'
    matches = re.findall(pattern, query)

    holdings: List[Dict] = []

    for qty, symbol, price in matches:
        symbol = symbol.upper()

        holdings.append(
            {
                "symbol": symbol,
                "quantity": float(qty),
                "price": float(price),
                "asset_type": "ETF" if symbol in {"VTI", "VOO", "BND", "QQQ"} else "Stock",
                "expense_ratio": 0.03 if symbol in {"VTI", "VOO", "BND", "QQQ"} else 0.0,
            }
        )

    return {"holdings": holdings} if holdings else {}


def parse_goal_from_query(query: str) -> Dict:
    target_match = re.search(r'(\$?\d[\d,]*)', query)
    years_match = re.search(r'(\d+)\s+years?', query.lower())
    return_match = re.search(r'(\d+(?:\.\d+)?)\s*%', query)
    monthly_match = re.search(r'(\$?\d[\d,]*)\s*(?:per month|monthly)', query.lower())

    result = {}

    if target_match:
        result["target_amount"] = float(target_match.group(1).replace("$", "").replace(",", ""))

    if years_match:
        result["years"] = int(years_match.group(1))

    if return_match:
        result["expected_return"] = float(return_match.group(1)) / 100

    if monthly_match:
        result["monthly_contribution"] = float(monthly_match.group(1).replace("$", "").replace(",", ""))

    return result


def parse_ticker_from_query(query: str) -> str | None:
    matches = re.findall(r"\b[A-Z]{1,5}\b", query.upper())
    common_words = {"WHAT", "IS", "THE", "PRICE", "OF", "SHOW", "ME", "FOR"}
    matches = [m for m in matches if m not in common_words]

    return matches[0] if matches else None