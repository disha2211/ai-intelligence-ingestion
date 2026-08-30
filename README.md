# AI Intelligence Ingestion

An asynchronous data ingestion pipeline for collecting and structuring **AI startups, products, research papers, models, and datasets** from multiple sources.

The project focuses on building a clean and extensible ingestion flow rather than tightly coupling the system to a single data source.

## What I Built

- Multi-source acquisition layer for AI intelligence data
- Async crawling with concurrency limits and retry handling
- Canonical normalization using Pydantic models
- Entity deduplication and resolution
- LLM-based metadata enrichment
- Multi-provider LLM fallback
- Research paper enrichment with topics, summaries, application areas, and GitHub information
- PostgreSQL persistence with SQLAlchemy
- CSV export for downstream analysis
- Pipeline statistics and automated tests

## Architecture

```text
Data Sources
    │
    ├── Y Combinator
    ├── Futurepedia
    ├── arXiv
    └── Hugging Face
            │
            ▼
     Acquisition Layer
            │
            ▼
     Raw Records / Documents
            │
            ▼
       Normalization
            │
            ▼
     Entity Resolution
       & Deduplication
            │
            ├──────────────► CSV Export
            │
            ▼
       LLM Enrichment
            │
       ├── Gemini
       ├── Groq
       └── DeepSeek
            │
            ▼
        Validation
            │
            ▼
      PostgreSQL / Entities
```

## Project Structure

```text
src/
├── acquisition/       # Source-specific data acquisition
├── crawlers/          # Async HTTP and arXiv crawlers
├── normalization/     # Convert raw data into canonical models
├── models/            # Domain and validation schemas
├── parsing/           # HTML and research-paper parsing
├── enrichment/        # LLM and GitHub enrichment
├── llm/               # Providers, orchestration, retries, chunking
├── quality/           # Deduplication and entity resolution
├── validation/        # Data validation
├── pipeline/          # End-to-end ingestion pipelines
├── db/                # SQLAlchemy persistence layer
└── export/             # CSV generation

scripts/
├── collect_bulk.py    # Collect source data
└── build_output.py    # Collect, deduplicate and export data

tests/                 # Unit and integration-style tests
output/                # Generated CSV datasets
```

## Key Design Decisions

### Source abstraction

Each acquisition source follows a common interface, allowing new sources to be added without changing the rest of the pipeline.

### Canonical data models

Source-specific payloads are converted into common Pydantic models such as:

- `Startup`
- `Product`
- `ResearchPaper`

This keeps downstream processing independent of the original source format.

### Async-first processing

The ingestion layer uses `asyncio` and `aiohttp` with bounded concurrency, connection limits, timeouts, and retry/backoff handling.

### LLM provider fallback

LLM calls are abstracted behind providers and an orchestrator. If one provider fails, the orchestrator can continue with the next configured provider.

### Entity resolution

Records are deduplicated using canonical URLs and normalized names, while mappings are retained so duplicate decisions remain traceable.

### Separation of concerns

Acquisition, normalization, enrichment, validation, persistence, and export are implemented as separate layers so individual components can evolve independently.

## Current Data Outputs

The pipeline currently produces:

```text
output/
├── startups.csv
├── products.csv
├── research_papers.csv
└── entity_mapping_log.csv
```

## Setup

```bash
git clone <repository-url>
cd ai-intelligence-ingestion

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Configure the required environment variables in `.env`:

```env
GEMINI_API_KEY=
GROQ_API_KEY=
DEEPSEEK_API_KEY=
GITHUB_TOKEN=
DATABASE_URL=
```

## Run

Collect data from the configured sources:

```bash
python scripts/collect_bulk.py
```

Build the cleaned CSV outputs:

```bash
python scripts/build_output.py
```

Initialize the database:

```bash
python -m src.db.init_db
```

Run the test suite:

```bash
pytest
```

## Tech Stack

**Python · asyncio · aiohttp · Pydantic · BeautifulSoup · SQLAlchemy · PostgreSQL · Gemini · Groq · DeepSeek · pytest**

## Status

The core ingestion architecture is implemented with multi-source acquisition, normalization, deduplication, LLM enrichment, persistence, and export pipelines in place.
