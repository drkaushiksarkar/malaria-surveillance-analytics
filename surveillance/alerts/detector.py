"""Outbreak detection algorithms for malaria surveillance."""
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from loguru import logger


class OutbreakDetector:
    """Detect malaria outbreaks using statistical thresholds."""

    def __init__(
        self,
        baseline_window: int = 36,
        alert_threshold_sd: float = 2.0,
        epidemic_threshold_sd: float = 3.0,
    ):
        self.baseline_window = baseline_window
        self.alert_threshold_sd = alert_threshold_sd
        self.epidemic_threshold_sd = epidemic_threshold_sd

    def compute_thresholds(
        self,
        df: pd.DataFrame,
        value_col: str = "malaria_total",
        group_col: str = "DISTRICT",
    ) -> pd.DataFrame:
        """Compute rolling mean and standard deviation thresholds."""
        df = df.sort_values(["YEAR", "MONTH"]).copy()
        results = []

        for name, group in df.groupby(group_col):
            series = group[value_col].values
            for i in range(len(series)):
                start = max(0, i - self.baseline_window)
                baseline = series[start:i] if i > 0 else series[:1]
                mean = np.mean(baseline)
                std = np.std(baseline) if len(baseline) > 1 else 0

                row = group.iloc[i].to_dict()
                row["baseline_mean"] = mean
                row["baseline_std"] = std
                row["alert_threshold"] = mean + self.alert_threshold_sd * std
                row["epidemic_threshold"] = mean + self.epidemic_threshold_sd * std
                row["is_alert"] = series[i] > row["alert_threshold"]
                row["is_epidemic"] = series[i] > row["epidemic_threshold"]
                results.append(row)

        return pd.DataFrame(results)

    def detect_outbreaks(
        self,
        df: pd.DataFrame,
        value_col: str = "malaria_total",
        group_col: str = "DISTRICT",
    ) -> List[Dict]:
        """Identify outbreak events."""
        thresholds = self.compute_thresholds(df, value_col, group_col)
        alerts = thresholds[thresholds["is_alert"]].copy()

        outbreaks = []
        for _, row in alerts.iterrows():
            outbreaks.append({
                "district": row[group_col],
                "year": int(row["YEAR"]),
                "month": int(row["MONTH"]),
                "observed": float(row[value_col]),
                "threshold": float(row["alert_threshold"]),
                "severity": "epidemic" if row["is_epidemic"] else "alert",
                "excess": float(row[value_col] - row["baseline_mean"]),
            })

        logger.info(
            f"Detected {len(outbreaks)} outbreak events "
            f"({sum(1 for o in outbreaks if o['severity'] == 'epidemic')} epidemic-level)"
        )
        return outbreaks
