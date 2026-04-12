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

## Example User queries

- “What is an ETF?” → Finance Q&A Agent
- "what was previous question related to?" - chat history
- “Analyze my portfolio.” → Portfolio Agent
- “What is Apple stock price('AAPL')?” → Market Agent
- “Explain capital gains tax” → Tax Agent
- “Help me save $50k in 5 years” → Goal Agent
- “Summarize market news” → News Agent


## Notes

- The current assistant is educational and not a substitute for professional financial, tax, or legal advice.
- Live data integration is not implemented yet in this MVP.
