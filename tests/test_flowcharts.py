"""Tests for flowchart visualization."""
import matplotlib
matplotlib.use("Agg")

from surveillance.viz.flowcharts import (
    draw_pipeline_flowchart,
    draw_feature_hierarchy,
    DATA_PREP_STEPS,
    BENCHMARKING_STEPS,
    FEATURE_CATEGORIES,
)


class TestFlowcharts:
    def test_pipeline_flowchart(self):
        fig = draw_pipeline_flowchart(DATA_PREP_STEPS, "Data Preparation")
        assert fig is not None

    def test_benchmarking_flowchart(self):
        fig = draw_pipeline_flowchart(BENCHMARKING_STEPS, "Benchmarking")
        assert fig is not None

    def test_feature_hierarchy(self):
        fig = draw_feature_hierarchy(FEATURE_CATEGORIES)
        assert fig is not None

    def test_empty_steps(self):
        fig = draw_pipeline_flowchart(["Step 1"])
        assert fig is not None
