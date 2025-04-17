import os
import pytest
import requests

from app import data_ingest

class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise requests.HTTPError(f"Status code: {self.status_code}")

def test_fetch_census_business_patterns(monkeypatch):
    sample = [
        ["EMP", "ESTAB", "NAME", "state", "county"],
        ["10", "5", "County A", "06", "001"],
        ["20", "8", "County B", "06", "003"],
    ]
    monkeypatch.setenv("CENSUS_API_KEY", "TESTKEY")
    def fake_get(url, params):
        assert "census.gov" in url
        assert params.get("key") == "TESTKEY"
        return DummyResponse(sample)
    monkeypatch.setattr(requests, "get", fake_get)
    result = data_ingest.fetch_census_business_patterns("06")
    assert isinstance(result, list)
    assert result[0]["EMP"] == "10"
    assert result[1]["NAME"] == "County B"

def test_fetch_census_population_by_zip(monkeypatch):
    sample = [["P1_001N", "NAME", "zip code tabulation area"], ["1234", "Test ZCTA", "90210"]]
    monkeypatch.setenv("CENSUS_API_KEY", "TESTKEY")
    def fake_get(url, params):
        assert "dec/pl" in url
        assert params.get("for") == "zip code tabulation area:90210"
        return DummyResponse(sample)
    monkeypatch.setattr(requests, "get", fake_get)
    result = data_ingest.fetch_census_population_by_zip("90210")
    assert result.get("P1_001N") == "1234"

def test_fetch_socrata_business_registry(monkeypatch):
    sample = [{"name": "B1"}, {"name": "B2"}]
    monkeypatch.setenv("SODA_ENDPOINT", "https://example.com/data.json")
    monkeypatch.setenv("SODA_APP_TOKEN", "TOKEN123")
    def fake_get(url, params, headers):
        assert url == "https://example.com/data.json"
        assert headers.get("X-App-Token") == "TOKEN123"
        assert params.get("$limit") == 500
        return DummyResponse(sample)
    monkeypatch.setattr(requests, "get", fake_get)
    result = data_ingest.fetch_socrata_business_registry("CA", limit=500)
    assert result == sample

def test_missing_env_vars(monkeypatch):
    # Ensure missing Census API key raises
    monkeypatch.delenv("CENSUS_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        data_ingest.fetch_census_business_patterns("06")
    with pytest.raises(RuntimeError):
        data_ingest.fetch_census_population_by_zip("90210")
    # Ensure missing Socrata endpoint raises
    monkeypatch.delenv("SODA_ENDPOINT", raising=False)
    with pytest.raises(RuntimeError):
        data_ingest.fetch_socrata_business_registry("CA")