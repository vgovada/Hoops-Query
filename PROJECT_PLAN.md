# Hoops Query — Project Planner

A step-by-step build plan for the NBA natural-language analytics agent. Work top to bottom. Don't skip phases — each one depends on the last. Check boxes as you go.

**How to use this:** Each step has a goal, the tasks to do it, and a "done when" line so you know when to move on. The traps are real mistakes people make — read them before starting each phase, not after.

---

## Phase 0 — Setup (foundation)

**Goal:** A working environment you can build on.

- [ ] Install PostgreSQL (Mac: Postgres.app or `brew install postgresql`; Windows: postgresql.org installer; Linux: `apt install postgresql`)
- [ ] Connect to it via `psql` or a GUI (DBeaver / pgAdmin)
- [ ] Create an empty database named `hoops_query`
- [ ] Create a project folder and a Python virtual environment
- [ ] `pip install nba_api pandas sqlalchemy psycopg2-binary`
- [ ] Initialize a git repo and make your first commit

**Done when:** You can connect to an empty `hoops_query` database and your virtual environment has the packages installed.

**Trap:** Skipping the virtual environment. Installing globally causes version conflicts later. Do it now.

---

## Phase 1 — Data into PostgreSQL

**Goal:** Real NBA data in a clean schema you understand.

- [ ] Use `nba_api` to pull data for ONE recent season (start with player game logs — don't grab everything)
- [ ] Load it into a pandas DataFrame and inspect it (column names, types, nulls)
- [ ] Decide your schema: sensible table name(s), clean column names, correct types
- [ ] Write a `load_data.py` script that pulls the data and writes it to Postgres
- [ ] Verify the data landed: row counts, spot-check a few records
- [ ] Write 5 SQL queries BY HAND against your schema (e.g. top scorers, most improved, team records)

**Done when:** You can run your 5 hand-written queries in psql and get correct answers.

**Trap:** Rushing the schema. Messy column names and wrong types poison everything downstream. Clean it now. Also: writing the 5 queries by hand is NOT optional — you can't judge the AI's SQL later if you can't write it yourself.

---

## Phase 2 — Baseline text-to-SQL (dumb version)

**Goal:** One end-to-end path working, even if crude.

- [ ] Set up access to an LLM (free API tier or local Ollama with Llama 3.1 / Mistral)
- [ ] Write a function: takes the schema + a question, returns SQL
- [ ] Write a function that runs that SQL against Postgres and returns rows
- [ ] Wire them together: question in → SQL → rows out → print
- [ ] Test on easy questions ("top 10 scorers")

**Done when:** You can type one question in a script and get correct rows back, even if it only works on easy questions.

**Trap:** Trying to make it good here. The goal is a working skeleton. Good comes in Phase 3. Working-but-bad beats clever-but-broken.

---

## Phase 3 — Make the AI real (the core engineering)

**Goal:** Handle where the dumb version breaks. This is the heart of the project.

- [ ] **Schema linking:** instead of dumping the whole schema, retrieve only relevant tables/columns per question
- [ ] **Self-correction loop:** catch SQL errors, feed the error back to the model, retry; cap retries so it can't loop forever
- [ ] **Result validation:** check the result is plausible (not empty, not obviously wrong) before returning
- [ ] **Multi-step reasoning:** let the agent run a follow-up query or compute a statistic when one query isn't enough
- [ ] **Tool structure:** organize the agent around `run_sql`, `compute_stats`, `make_chart`

**Done when:** The agent answers hard questions correctly, recovers from its own errors, and doesn't infinite-loop.

**Trap:** The retry loop not converging — spinning forever or quitting too early. Getting this stable is the real engineering. Expect to spend the most time here.

---

## Phase 4 — Evaluation harness (your resume's load-bearing piece)

**Goal:** Prove it works with a number.

- [ ] Build a benchmark: ~30–50 question / expected-result pairs
- [ ] Write a harness that runs each question and scores execution accuracy (does the SQL return the right rows?)
- [ ] Track average retries per query
- [ ] Run it, record your baseline accuracy
- [ ] Improve prompts/schema linking, re-run, watch the number go up

**Done when:** You have a real accuracy percentage you can put on your resume and defend in an interview.

**Trap:** Skipping this because it's unglamorous. This is the single thing that separates you from people who just built a demo. Do not skip it.

---

## Phase 5 — FastAPI backend

**Goal:** Wrap the agent in an API.

- [ ] Install FastAPI and uvicorn
- [ ] Create an endpoint that takes a question and returns the answer + SQL + reasoning steps
- [ ] Add error handling (bad questions, DB errors, timeouts)
- [ ] Test the endpoint with curl or the auto-generated docs at `/docs`

**Done when:** You can POST a question to your API and get a structured response back.

**Trap:** New to backend — that's fine. Keep the API tiny: one or two endpoints. Don't gold-plate it.

---

## Phase 6 — React frontend

**Goal:** A clean, demoable interface.

- [ ] Scaffold a React app (Vite)
- [ ] Build: a query input box, a results table, a chart, and a panel showing the agent's reasoning steps + the SQL it ran
- [ ] Connect it to your FastAPI backend
- [ ] Style it so it looks intentional, not default

**Done when:** You can type a question in the browser and watch the full answer + reasoning render.

**Trap:** The reasoning-steps panel is the highest-value UI element — it proves the thing is really agentic. Don't cut it to save time.

---

## Phase 7 — Polish & present

**Goal:** Make it readable and provable.

- [ ] Finalize the README (description, architecture, stack, accuracy number, setup steps)
- [ ] Add a screenshot or short GIF of it working
- [ ] Clean the code: remove dead code, add comments where logic is non-obvious
- [ ] Make sure `git clone` → setup steps actually work from scratch
- [ ] Write your resume bullet: stack + scope + the accuracy number

**Done when:** Someone could clone your repo, follow the README, and run it — and your resume bullet is written.

**Trap:** A README promising features the code doesn't have hurts more than a modest one. Make the README match reality.

---

## The two genuinely hard parts (where your interview stories come from)

1. **Text-to-SQL accuracy on a real schema** (Phase 3) — getting the model to write correct SQL against messy column names and multi-table joins.
2. **Getting the agent loop to terminate sensibly** (Phase 3) — not looping forever, not quitting early.

When these fight you, that's not failure — that's the project working. These are the stories you tell in interviews.
