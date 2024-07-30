"""Heatmap visualizations for geographic and temporal patterns."""
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from loguru import logger


def district_month_heatmap(
    df: pd.DataFrame,
    value_col: str = "malaria_total",
    figsize: Tuple[int, int] = (16, 8),
    output_path: Optional[str] = None,
) -> plt.Figure:
    """Create district x month heatmap of malaria burden."""
    pivot = df.pivot_table(
        values=value_col, index="DISTRICT", columns="MONTH", aggfunc="sum"
    )
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(pivot, cmap="YlOrRd", annot=True, fmt=".0f", ax=ax)
    ax.set_title(f"{value_col} by District and Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("District")
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return fig


def annual_trend_heatmap(
    df: pd.DataFrame,
    value_col: str = "api",
    figsize: Tuple[int, int] = (14, 8),
    output_path: Optional[str] = None,
) -> plt.Figure:
    """Create district x year heatmap showing API trends."""
    pivot = df.pivot_table(
        values=value_col, index="DISTRICT", columns="YEAR", aggfunc="mean"
    )
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(pivot, cmap="RdYlGn_r", annot=True, fmt=".1f", ax=ax)
    ax.set_title(f"Annual {value_col} Trends by District")
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return fig


def correlation_matrix(
    df: pd.DataFrame,
    columns: Optional[list] = None,
    figsize: Tuple[int, int] = (12, 10),
    output_path: Optional[str] = None,
) -> plt.Figure:
    """Plot correlation matrix heatmap."""
    if columns:
        df = df[columns]
    numeric = df.select_dtypes(include=[np.number])
    corr = numeric.corr()

    fig, ax = plt.subplots(figsize=figsize)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap="coolwarm", center=0,
               annot=True, fmt=".2f", ax=ax)
    ax.set_title("Feature Correlation Matrix")
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return fig
