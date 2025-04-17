"""
Data ingestion pipeline for MarketPulse: fetch data from Census Bureau and Socrata portals.
"""
import os
import requests

def fetch_census_business_patterns(geography: str):
    """
    Fetch County Business Patterns (EMP, ESTAB) from the U.S. Census Bureau API for the given state FIPS code.
    Returns a list of dicts with keys: EMP, ESTAB, NAME, state, county.
    """
    api_key = os.getenv("CENSUS_API_KEY")
    if not api_key:
        raise RuntimeError("CENSUS_API_KEY environment variable is not set")
    url = "https://api.census.gov/data/2020/cbp"
    params = {
        "get": "EMP,ESTAB,NAME",
        "for": "county:*",
        "in": f"state:{geography}",
        "key": api_key,
    }
    resp = requests.get(url, params=params)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Census API error: {e}")
    data = resp.json()
    header, *rows = data
    return [dict(zip(header, row)) for row in rows]

def fetch_census_population_by_zip(zip_code: str):
    """
    Fetch population (P1_001N) from the 2020 Decennial Census for a given ZIP Code Tabulation Area.
    Returns a dict with keys: P1_001N, NAME, zip code tabulation area.
    """
    api_key = os.getenv("CENSUS_API_KEY")
    if not api_key:
        raise RuntimeError("CENSUS_API_KEY environment variable is not set")
    url = "https://api.census.gov/data/2020/dec/pl"
    params = {
        "get": "P1_001N,NAME",
        "for": f"zip code tabulation area:{zip_code}",
        "key": api_key,
    }
    resp = requests.get(url, params=params)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Census API error: {e}")
    data = resp.json()
    header, row = data
    return dict(zip(header, row))

def fetch_socrata_business_registry(state: str, limit: int = 1000):
    """
    Query a Socrata open-data portal for business registry data for the specified state.
    Uses SODA_ENDPOINT and optional SODA_APP_TOKEN environment variables.
    Returns a list of records as dicts.
    """
    endpoint = os.getenv("SODA_ENDPOINT")
    if not endpoint:
        raise RuntimeError("SODA_ENDPOINT environment variable is not set")
    app_token = os.getenv("SODA_APP_TOKEN")
    headers = {"X-App-Token": app_token} if app_token else {}
    params = {"$limit": limit}
    # Optionally filter by state if supported by dataset
    if state:
        params.setdefault("state", state)
    resp = requests.get(endpoint, params=params, headers=headers)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Socrata API error: {e}")
    return resp.json()