"""Data aggregation across geographic hierarchies."""
from typing import Dict, List, Optional

import pandas as pd
from loguru import logger


class SurveillanceAggregator:
    """Aggregate surveillance data across geographic levels."""

    HIERARCHY = ["DISTRICT", "BLOCK", "CHC", "SC"]
    SUM_COLS = ["Population", "Fever", "pv_total", "pf_total", "malaria_total"]

    def aggregate_to_level(
        self,
        df: pd.DataFrame,
        level: str,
        time_cols: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Aggregate surveillance data to specified geographic level."""
        if level not in self.HIERARCHY:
            raise ValueError(f"Invalid level: {level}. Must be one of {self.HIERARCHY}")

        time_cols = time_cols or ["YEAR", "MONTH"]
        level_idx = self.HIERARCHY.index(level)
        group_cols = time_cols + self.HIERARCHY[: level_idx + 1]

        # Filter to available columns
        sum_cols = [c for c in self.SUM_COLS if c in df.columns]
        group_cols = [c for c in group_cols if c in df.columns]

        aggregated = df.groupby(group_cols)[sum_cols].sum().reset_index()

        # Compute derived rates
        aggregated["fever_proportion"] = aggregated["Fever"] / aggregated["Population"].clip(lower=1)
        aggregated["tpr"] = aggregated["malaria_total"] / aggregated["Population"].clip(lower=1)
        aggregated["api"] = aggregated["tpr"] * 1000
        aggregated["pf_fraction"] = (
            aggregated["pf_total"] / aggregated["malaria_total"].clip(lower=1)
        )

        logger.info(f"Aggregated to {level}: {len(aggregated)} records")
        return aggregated

    def aggregate_all_levels(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Aggregate to all available geographic levels."""
        results = {}
        for level in self.HIERARCHY:
            if level in df.columns:
                results[level] = self.aggregate_to_level(df, level)
        return results

    def compute_trends(
        self,
        df: pd.DataFrame,
        group_cols: List[str],
        value_col: str = "malaria_total",
    ) -> pd.DataFrame:
        """Compute year-over-year trends."""
        annual = (
            df.groupby(group_cols + ["YEAR"])[value_col]
            .sum()
            .reset_index()
        )
        annual["yoy_change"] = annual.groupby(group_cols)[value_col].pct_change()
        return annual
