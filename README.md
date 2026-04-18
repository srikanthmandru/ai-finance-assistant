# Finnie AI

## Architecture Overview

The AI Finance Assistant is a multi-agent conversational system designed to provide financial education, portfolio analysis, market insights, and goal planning. The application uses LangGraph for workflow orchestration, a RAG pipeline for grounded financial knowledge retrieval, and external market APIs for real-time data.

### Core Components
- **UI Layer:** Streamlit-based chat and dashboard interface
- **Workflow Layer:** LangGraph router for query classification and agent orchestration
- **Agent Layer:** Specialized agents for Q&A, portfolio, market, goals, news, and tax
- **RAG Layer:** FAISS-based retrieval over curated financial education content
- **Tool Layer:** Portfolio calculators, goal projection engine, market API clients
- **State Layer:** Conversation memory and session context preservation

## Current architecture

User -> Gradio UI -> LangGraph router -> Specialist finance agent -> Response

## System Architecture

```text
User
  |
  v
Streamlit UI
  |
  v
LangGraph Workflow Router
  |
  +-------------------+-------------------+-------------------+-------------------+
  |                   |                   |                   |                   |
  v                   v                   v                   v                   v
Finance Q&A      Portfolio Agent     Market Agent       Goal Agent        News/Tax Agents
  |                   |                   |                   |                   |
  v                   v                   v                   v                   v
RAG Retriever    Calc Engine        Market API         Projection Logic   RAG / External Data
  |                   |                   |                   |                   
  v                   v                   v                   v
FAISS KB         Portfolio Metrics   Cache + Rate Limit  Goal Plans
  \____________________    ________________________________/
                       \  /
                        v
               LLM Response Builder
                        |
                        v
            Response with Source Attribution
                        |
                        v
                  Back to Streamlit UI

```
## Project Structure

```text
ai_finance_assistant/
├── src/
│   ├── agents/        # Specialized finance agents
│   ├── core/          # Shared config, constants, models, logging
│   ├── data/          # Financial articles, glossary, sample portfolios
│   ├── rag/           # Chunking, embeddings, vector store, retrieval
│   ├── tools/         # Market APIs, portfolio calculations, goal planning
│   ├── workflow/      # LangGraph router, state, nodes, graph
│   ├── web_app/       # Streamlit UI and visual components
│   └── utils/         # Helper and validation utilities
├── tests/             # Unit and integration tests
├── config.yaml        # App configuration
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
python src/main.py
```

```bash
# Build Index:
python -m src.rag.build_index
```

```bash
# Test retriever:
python -m src.rag.test_retriever
```

```bash
# Test Portfolio Calculator
python -m src.tools.test_portfolio_calculator
```

```bash
# Test Market data tool
python -m src.tools.test_market_data_tool
```

```bash
# Run streamlit app
export PYTHONPATH=$(pwd)
streamlit run src/web_app/app.py
```

```bash
# Run tests
pytest
```

## Example User queries
#### QA Agent
- What is an ETF?
- Is an ETF safer than an individual stock?
- Compare ETFs with mutual funds.
- What does diversification mean?
- Explain compound interest in simple terms.
#### Market Agent
- What is the current price of AAPL?
- Show me the trend for NVDA over the last month.
- How has TSLA performed recently?
- Give me a market snapshot for my portfolio.
- What is happening with MSFT stock?
#### Portfolio Agent
- Analyze this portfolio: 10 VTI at 250, 5 AAPL at 190, 8 BND at 72
- Is this portfolio diversified enough: 20 AAPL at 190, 15 MSFT at 420
- Suggest improvements for this portfolio: 10 VTI at 250, 5 AAPL at 190, 8 BND at 72
- How risky is this portfolio: 15 TSLA at 180, 10 NVDA at 900
- Help me rebalance this portfolio: 20 AAPL at 190, 10 TSLA at 180, 5 BND at 72
#### Goal Agent
- Help me save 50000 in 5 years at 7% annual return.
- How much will I have if I invest 500 per month for 10 years at 7%?
- I want to reach 100000 in 8 years. How much should I invest monthly?
- If I invest 1000 per month for 15 years, what could it grow to?
- Plan a retirement goal of 750000 in 25 years.
#### Multi-agent queries
- Analyze this portfolio and compare it with current market trends: 10 VTI at 250, 5 AAPL at 190, 8 BND at 72
- Help me plan retirement and explain the tax basics.
- Build a beginner ETF portfolio and analyze its risk.
- Compare my portfolio with market conditions and suggest improvements: 10 VTI at 250, 5 AAPL at 190, 8 BND at 72
- If I have moderate risk tolerance, how should I plan a 10-year investment goal?
- Follow-up / multi-turn queries

Use these in sequence.

##### Flow 1
- What is an ETF?
- Is that safer than individual stocks?
- Compare it with bonds.
- Build a beginner portfolio using it.
- Now analyze that portfolio.
- Add few more stocks, ETFs and bonds to the beginner portfolio.

##### Flow 2
- Help me save 50000 in 5 years at 7% annual return.
- What if I extend it to 7 years?
- What if my return is only 5%?
- Is that a high monthly contribution?
##### Flow 3
- Analyze this portfolio: 10 VTI at 250, 5 AAPL at 190, 8 BND at 72
- How is it doing compared with market trends?
- Should I reduce concentration risk?
- What would be a more balanced version?
##### Best 5 queries for demo
- What is an ETF?
- Analyze this portfolio: 10 VTI at 250, 5 AAPL at 190, 8 BND at 72
- Show me the trend for AAPL over the last month.
- Help me save 50000 in 5 years at 7% annual return.
- Analyze this portfolio and compare it with current market trends: 10 VTI at 250, 5 AAPL at 190, 8 BND at 72


## Notes

- The current assistant is educational and not a substitute for professional financial, tax, or legal advice.
- Live data integration is not implemented yet in this MVP.
