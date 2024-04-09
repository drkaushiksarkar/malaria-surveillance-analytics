# Malaria Surveillance Analytics

District-level malaria surveillance analytics platform with automated
reporting, outbreak detection, and visualization.

## Features

- **Multi-level Aggregation**: Aggregate surveillance data across district,
  block, CHC, and sub-center geographic hierarchies
- **Outbreak Detection**: Statistical threshold-based outbreak detection
  with configurable alert and epidemic thresholds
- **Time Series Visualization**: Interactive time series plots for malaria
  trends, species comparison (P. vivax vs P. falciparum), and seasonal patterns
- **Heatmaps**: District-month burden heatmaps, annual trend heatmaps,
  feature correlation matrices
- **Pipeline Flowcharts**: Visual documentation of data preparation,
  benchmarking, and feature engineering workflows
- **Automated Reports**: Markdown and JSON report generation with
  epidemiological summary statistics

## Quick Start

```bash
pip install -e ".[dev]"
make test
make report
```

## Project Structure

```
surveillance/
    schemas.py              # Pydantic data validation
    aggregator.py           # Geographic hierarchy aggregation
    viz/
        time_series.py      # Temporal trend visualization
        heatmaps.py         # Geographic and seasonal heatmaps
        flowcharts.py       # Pipeline and architecture diagrams
    reports/
        generator.py        # Automated report generation
    alerts/
        detector.py         # Outbreak detection algorithms
tests/
    test_schemas.py
    test_aggregator.py
    test_detector.py
    test_time_series_viz.py
    test_flowcharts.py
```

## Data Format

Surveillance data requires columns:
- YEAR, MONTH, DISTRICT, BLOCK (identifiers)
- Population, Fever, pv_total, pf_total, malaria_total (measures)

## License

MIT
