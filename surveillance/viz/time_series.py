"""Time series visualization for surveillance data."""
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter, MonthLocator
from loguru import logger


def plot_time_series(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    date_col: str = "DATE",
    figsize: Tuple[int, int] = (14, 6),
    title: Optional[str] = None,
    output_path: Optional[str] = None,
) -> plt.Figure:
    """Plot time series for each group in the dataset."""
    fig, ax = plt.subplots(figsize=figsize)

    for name, group in df.groupby(group_col):
        ax.plot(group[date_col], group[value_col], label=str(name), alpha=0.7)

    ax.set_xlabel("Date")
    ax.set_ylabel(value_col)
    ax.set_title(title or f"{value_col} by {group_col}")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    ax.xaxis.set_major_locator(MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        logger.info(f"Saved time series plot to {output_path}")

    return fig


def plot_grouped_time_series(
    df: pd.DataFrame,
    date_col: str,
    group_col: str,
    value_col: str,
    figsize: Tuple[int, int] = (20, 7),
    title: Optional[str] = None,
) -> plt.Figure:
    """Aggregate and plot time series grouped by a categorical variable."""
    grouped = df.groupby([group_col, date_col])[value_col].mean().reset_index()

    fig, ax = plt.subplots(figsize=figsize)
    for name, group in grouped.groupby(group_col):
        ax.plot(group[date_col], group[value_col], label=str(name))

    ax.set_title(title or f"Mean {value_col} by {group_col}")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"Mean {value_col}")
    ax.legend(fontsize=8)
    plt.tight_layout()
    return fig


def plot_species_comparison(
    df: pd.DataFrame,
    date_col: str = "DATE",
    figsize: Tuple[int, int] = (14, 6),
    output_path: Optional[str] = None,
) -> plt.Figure:
    """Compare Plasmodium vivax vs falciparum trends."""
    fig, ax = plt.subplots(figsize=figsize)

    if "pv_total" in df.columns:
        ts_pv = df.groupby(date_col)["pv_total"].sum()
        ax.plot(ts_pv.index, ts_pv.values, label="P. vivax", color="#2196F3")
    if "pf_total" in df.columns:
        ts_pf = df.groupby(date_col)["pf_total"].sum()
        ax.plot(ts_pf.index, ts_pf.values, label="P. falciparum", color="#F44336")

    ax.set_title("Plasmodium Species Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Cases")
    ax.legend()
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return fig
