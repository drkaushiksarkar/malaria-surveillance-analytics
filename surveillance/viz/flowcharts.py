"""Pipeline and architecture visualization using networkx/graphviz."""
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx
from loguru import logger


def draw_pipeline_flowchart(
    steps: List[str],
    title: str = "Data Pipeline",
    figsize: Tuple[int, int] = (12, 8),
    output_path: Optional[str] = None,
) -> plt.Figure:
    """Draw a linear pipeline flowchart."""
    G = nx.DiGraph()
    for i, step in enumerate(steps):
        G.add_node(step)
        if i > 0:
            G.add_edge(steps[i - 1], step)

    fig, ax = plt.subplots(figsize=figsize)
    pos = {step: (0, -i) for i, step in enumerate(steps)}
    nx.draw(
        G, pos, ax=ax, with_labels=True, node_color="#4CAF50",
        node_size=3000, font_size=9, font_weight="bold",
        edge_color="#666", arrows=True, arrowsize=20,
    )
    ax.set_title(title)
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return fig


def draw_feature_hierarchy(
    categories: Dict[str, List[str]],
    title: str = "Feature Hierarchy",
    figsize: Tuple[int, int] = (16, 10),
    output_path: Optional[str] = None,
) -> plt.Figure:
    """Draw a hierarchical feature category diagram."""
    G = nx.DiGraph()
    G.add_node("Features")

    for category, features in categories.items():
        G.add_edge("Features", category)
        for feat in features:
            G.add_edge(category, feat)

    fig, ax = plt.subplots(figsize=figsize)
    pos = nx.spring_layout(G, k=2, seed=42)
    colors = []
    for node in G.nodes():
        if node == "Features":
            colors.append("#1976D2")
        elif node in categories:
            colors.append("#4CAF50")
        else:
            colors.append("#FFC107")

    nx.draw(
        G, pos, ax=ax, with_labels=True, node_color=colors,
        node_size=1500, font_size=7, edge_color="#999",
        arrows=True, arrowsize=15,
    )
    ax.set_title(title)
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return fig


# Standard pipeline definitions from MPPT data preparation workflow
DATA_PREP_STEPS = [
    "Replace zero population values",
    "Name correction (fuzzy matching)",
    "Create secondary columns (TPR, PfPR, proportions)",
    "Create Area_Index",
    "Drop sub-center geographic columns",
    "Sort by date and geography",
    "Create lag features (1, 2, 3, 6, 12 months)",
    "Drop lag source columns",
    "Remove NaN rows from lagging",
    "One-hot encode categorical variables",
    "Select feature columns",
    "Validate no inf/NaN values",
    "Scale features (RobustScaler)",
]

BENCHMARKING_STEPS = [
    "Import libraries and data",
    "Define evaluation metrics",
    "Define baseline models",
    "Configure time series cross-validation",
    "Loop through Area_Index values",
    "Load LSTM model per area",
    "Generate predictions",
    "Inverse scale predictions",
    "Evaluate LSTM model",
    "Evaluate baseline models",
    "Compare all models",
    "Generate benchmark report",
]

FEATURE_CATEGORIES = {
    "Time Information": ["MONTH", "YEAR"],
    "Geographical Information": ["DISTRICT", "BLOCK"],
    "Weather Metrics": ["temperature", "rainfall", "humidity", "wind_speed"],
    "Soil and Vegetation": ["NDVI", "soil_moisture", "elevation"],
    "Population and Health": ["Population", "Fever", "surveillance_coverage"],
    "Previous Malaria": ["pv_lag1", "pf_lag1", "malaria_lag1", "malaria_lag3"],
    "Target": ["TPR"],
}
