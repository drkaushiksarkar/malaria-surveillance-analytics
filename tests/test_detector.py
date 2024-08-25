"""Tests for outbreak detection."""
import numpy as np
import pandas as pd
import pytest

from surveillance.alerts.detector import OutbreakDetector


@pytest.fixture
def surveillance_data():
    np.random.seed(42)
    n_months = 48
    return pd.DataFrame({
        "YEAR": np.repeat(range(2020, 2024), 12),
        "MONTH": np.tile(range(1, 13), 4),
        "DISTRICT": ["D1"] * n_months,
        "malaria_total": np.concatenate([
            np.random.poisson(50, 36),  # Normal
            np.array([50, 55, 200, 250, 60, 45, 180, 55, 50, 48, 52, 47]),  # Spikes
        ]),
    })


class TestOutbreakDetector:
    def test_detects_spikes(self, surveillance_data):
        detector = OutbreakDetector(baseline_window=24, alert_threshold_sd=2.0)
        outbreaks = detector.detect_outbreaks(surveillance_data)
        assert len(outbreaks) > 0
        assert any(o["severity"] == "epidemic" for o in outbreaks)

    def test_threshold_computation(self, surveillance_data):
        detector = OutbreakDetector()
        result = detector.compute_thresholds(surveillance_data)
        assert "baseline_mean" in result.columns
        assert "is_alert" in result.columns
        assert "is_epidemic" in result.columns

    def test_no_false_positives_on_flat(self):
        flat = pd.DataFrame({
            "YEAR": np.repeat(range(2020, 2024), 12),
            "MONTH": np.tile(range(1, 13), 4),
            "DISTRICT": ["D1"] * 48,
            "malaria_total": [50] * 48,
        })
        detector = OutbreakDetector()
        outbreaks = detector.detect_outbreaks(flat)
        assert len(outbreaks) == 0
