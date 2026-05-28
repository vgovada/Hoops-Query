# Hoops Query

**Ask questions about NBA stats in plain English. Get real answers, computed from real data.**

Hoops Query is a natural-language analytics agent for NBA statistics. Ask a question like *"Which players had the biggest scoring jump over the season?"* and an AI agent figures out which parts of the database matter, writes the SQL to answer it, runs that query against a PostgreSQL database of historical NBA data, and checks the result — retrying automatically when a query fails or returns something that doesn't add up. For questions that take more than one step, it chains queries and computes the stats it needs along the way, then returns the answer with a chart and a record of how it got there.

The model never makes up answers. Every response is computed from real data using SQL the agent writes and runs itself.

---

## Demo

<!-- Add a screenshot or GIF of the app in action here -->
![Hoops Query demo](docs/demo.gif)

---

## Features

- **Natural-language to SQL** — ask questions in plain English, get accurate results.
- **Self-correcting agent** — when a query fails or returns nonsense, the agent reads the error and retries until it gets it right.
- **Schema-aware** — retrieves only the relevant tables and columns for each question, so it scales to large schemas.
- **Multi-step reasoning** — runs follow-up queries and computes statistics when a single query isn't enough.
- **Transparent** — shows the reasoning steps and the SQL it ran, so you can trust (and verify) every answer.
- **Visualizations** — renders charts automatically based on the result.

---

## How it works

```
User question
      │
      ▼
 Schema linker  ──▶  LLM agent  ──▶  run SQL on PostgreSQL
                          ▲                  │
                          │   error / rows   │
                          └── validate & retry ◀┘
                          │
                          ▼
              synthesize answer + chart
```

The agent has access to three tools — `run_sql`, `compute_stats`, and `make_chart` — and decides which to call at each step.

---

## Tech stack

- **Frontend:** React
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **AI:** LLM-based text-to-SQL with an agentic self-correction loop
- **Data:** [`nba_api`](https://github.com/swar/nba_api) (free, no API key required)

---

## Getting started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

### Setup

```bash
# Clone the repo
git clone https://github.com/<your-username>/hoops-query.git
cd hoops-query

# Install backend dependencies
pip install -r requirements.txt

# Create the database and load NBA data
createdb hoops_query
python scripts/load_data.py

# Start the backend
uvicorn app.main:app --reload
```

```bash
# In a second terminal, start the frontend
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173` and start asking questions.

---

## Example questions

- *"Who were the top 10 scorers by points per game this season?"*
- *"Which players improved their three-point percentage the most?"*
- *"What's the Celtics' record on the second night of back-to-backs?"*
- *"Show me the most efficient scorers by true shooting percentage."*

---
## License

Released under the MIT License. See [LICENSE](LICENSE) for details.
