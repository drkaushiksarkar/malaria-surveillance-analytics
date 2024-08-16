"""Tests for surveillance data aggregation."""
import pandas as pd
import pytest

from surveillance.aggregator import SurveillanceAggregator


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "YEAR": [2023, 2023, 2023, 2023],
        "MONTH": [1, 1, 1, 1],
        "DISTRICT": ["D1", "D1", "D2", "D2"],
        "BLOCK": ["B1", "B2", "B3", "B4"],
        "Population": [10000, 15000, 12000, 8000],
        "Fever": [100, 200, 150, 80],
        "pv_total": [20, 40, 30, 10],
        "pf_total": [10, 30, 20, 5],
        "malaria_total": [30, 70, 50, 15],
    })


class TestSurveillanceAggregator:
    def test_aggregate_to_district(self, sample_data):
        agg = SurveillanceAggregator()
        result = agg.aggregate_to_level(sample_data, "DISTRICT")
        assert len(result) == 2
        d1 = result[result["DISTRICT"] == "D1"].iloc[0]
        assert d1["Population"] == 25000
        assert d1["malaria_total"] == 100

    def test_aggregate_to_block(self, sample_data):
        agg = SurveillanceAggregator()
        result = agg.aggregate_to_level(sample_data, "BLOCK")
        assert len(result) == 4

    def test_derived_rates(self, sample_data):
        agg = SurveillanceAggregator()
        result = agg.aggregate_to_level(sample_data, "DISTRICT")
        assert "tpr" in result.columns
        assert "api" in result.columns
        assert "pf_fraction" in result.columns
        assert all(result["api"] > 0)

    def test_invalid_level_raises(self, sample_data):
        agg = SurveillanceAggregator()
        with pytest.raises(ValueError, match="Invalid level"):
            agg.aggregate_to_level(sample_data, "INVALID")
