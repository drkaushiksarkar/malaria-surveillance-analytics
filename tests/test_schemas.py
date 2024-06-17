"""Tests for surveillance data schemas."""
import pytest
from surveillance.schemas import SurveillanceRecord


class TestSurveillanceRecord:
    def test_valid_record(self):
        r = SurveillanceRecord(
            year=2023, month=6, district="D1", block="B1",
            population=10000, fever=200, pv_total=50, pf_total=30,
            malaria_total=80,
        )
        assert r.tpr == 0.008
        assert r.api == 8.0

    def test_zero_population_tpr(self):
        r = SurveillanceRecord(
            year=2023, month=1, district="D1", block="B1",
            population=0, fever=0, pv_total=0, pf_total=0,
            malaria_total=0,
        )
        assert r.tpr == 0.0

    def test_invalid_malaria_total_raises(self):
        with pytest.raises(ValueError, match="malaria_total"):
            SurveillanceRecord(
                year=2023, month=1, district="D1", block="B1",
                population=1000, fever=10, pv_total=50, pf_total=30,
                malaria_total=10,
            )

    def test_invalid_month_raises(self):
        with pytest.raises(ValueError):
            SurveillanceRecord(
                year=2023, month=13, district="D1", block="B1",
                population=1000, fever=10, pv_total=5, pf_total=3,
                malaria_total=8,
            )
