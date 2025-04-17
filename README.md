<!-- badges -->
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)

# MarketPulse

> On-demand local market analysis toolkit powered by Codex CLI & OpenAI models.

## Our Why

At MarketPulse, we believe that every entrepreneur and non-profit organization deserves access to powerful market analysis tools. Small business owners and mission-driven organizations often lack the resources to conduct comprehensive market research. By leveraging public-sector data and AI, we aim to:

- Democratize market intelligence
- Empower entrepreneurs to validate ideas and plan growth
- Support non-profits in understanding community needs and measuring impact
- Lower the barrier to entry for meaningful insights

With MarketPulse, we make it easy and affordable to gather and analyze local market data, so mission-driven individuals and organizations can focus on making a difference.

MarketPulse leverages public-sector data (U.S. Census Bureau, Socrata portals) and AI to deliver:
- Competitor landscape mapping
- Trend summaries across demographics, economy, and news
- Quick SWOT analyses

## Table of Contents
1. [Features](#features)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Configuration](#configuration)
3. [Usage](#usage)
   - [Running the API](#running-the-api)
   - [API Endpoints](#api-endpoints)
4. [Data Ingestion Examples](#data-ingestion-examples)
   - [California Business Patterns](#california-business-patterns)
   - [Texas Market Data](#texas-market-data)
5. [Architecture](#architecture)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)

## Features
- Competitor landscape mapping (using embeddings + public data)
- Trend summaries (social media, news, Census & BLS data)
- SWOT report generation with LLM-powered prompts
- Extensible ETL for Census & Socrata data sources

## Getting Started

### Prerequisites
- Python 3.8+
- [Codex CLI](https://github.com/openai/codex-cli) installed & authenticated
- (Optional) Docker & Docker Compose

### Installation
```bash
git clone https://github.com/tekimax/marketpulse.git
cd marketpulse/marketpulse-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in `marketpulse-backend/` with:
```
CENSUS_API_KEY=YOUR_CENSUS_API_KEY
SODA_ENDPOINT=https://data.yourstate.gov/resource/your-dataset.json
SODA_APP_TOKEN=YOUR_SOCRATA_APP_TOKEN
CORS_ORIGINS=*
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

## Usage

### Running the API
```bash
cd marketpulse-backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

#### Health Check
- **GET /**
- **Response:**
```json
{ "message": "MarketPulse API is running" }
```

#### Analyze Prompt
- **POST /api/ai/analyze**
- **Request Body:**
```json
{ "prompt": "<your prompt text>" }
```
- **Response Body:**
```json
{ "analysis": "<codex response>" }
```

## Data Ingestion Examples

### California Business Patterns
```python
from app.data_ingest import (
    fetch_census_business_patterns,
    fetch_census_population_by_zip,
    fetch_socrata_business_registry,
)

# California FIPS code = 06
patterns_ca = fetch_census_business_patterns("06")
# Example ZIP: 94105
population_94105 = fetch_census_population_by_zip("94105")
# CA Socrata endpoint
registry_ca = fetch_socrata_business_registry("CA", limit=500)

print(patterns_ca[:2])
print(population_94105)
print(registry_ca[:2])
```

### Texas Market Data
```bash
export CENSUS_API_KEY=YOUR_KEY
export SODA_ENDPOINT=https://data.texas.gov/resource/vn28-icjr.json
export SODA_APP_TOKEN=YOUR_APP_TOKEN

cd marketpulse-backend
python3 - <<'EOF'
from app.data_ingest import (
    fetch_census_business_patterns,
    fetch_census_population_by_zip,
    fetch_socrata_business_registry,
)

# Texas FIPS code = 48
patterns_tx = fetch_census_business_patterns("48")
# ZIP code example: 77001
pop_77001 = fetch_census_population_by_zip("77001")
registry_tx = fetch_socrata_business_registry("TX", limit=500)

print(patterns_tx[:2])
print(pop_77001)
print(registry_tx[:2])
EOF
```

## Architecture
- **Backend**: FastAPI service (`app/main.py`)
- **AI**: Codex CLI integration (`app/ai.py`)
- **Ingestion**: Census & Socrata (`app/data_ingest.py`)
- **Container**: Docker support via `Dockerfile`

## Testing
```bash
cd marketpulse-backend
pip install -r requirements-dev.txt
pytest
```

## Contributing
1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes
4. Open a Pull Request

## License
This project is licensed under the MIT License.