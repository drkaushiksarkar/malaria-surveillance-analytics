"""Tests for time series visualization."""
import matplotlib
matplotlib.use("Agg")

import pandas as pd
import pytest

from surveillance.viz.time_series import plot_time_series, plot_species_comparison


@pytest.fixture
def sample_ts_data():
    return pd.DataFrame({
        "DATE": pd.date_range("2023-01-01", periods=24, freq="ME"),
        "DISTRICT": ["D1"] * 12 + ["D2"] * 12,
        "pv_total": range(24),
        "pf_total": range(24, 48),
        "malaria_total": range(24, 48),
    })


class TestTimeSeriesPlots:
    def test_plot_time_series_returns_figure(self, sample_ts_data):
        fig = plot_time_series(sample_ts_data, "DISTRICT", "malaria_total")
        assert fig is not None

    def test_species_comparison(self, sample_ts_data):
        fig = plot_species_comparison(sample_ts_data)
        assert fig is not None
