"""Data schemas and validation for surveillance data."""
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class SurveillanceRecord(BaseModel):
    """Single surveillance observation at sub-center level."""
    year: int = Field(ge=2000, le=2030)
    month: int = Field(ge=1, le=12)
    district: str
    block: str
    chc: Optional[str] = None
    sc: Optional[str] = None
    population: int = Field(ge=0)
    fever: int = Field(ge=0)
    pv_total: int = Field(ge=0, description="Plasmodium vivax cases")
    pf_total: int = Field(ge=0, description="Plasmodium falciparum cases")
    malaria_total: int = Field(ge=0)

    @field_validator("malaria_total")
    @classmethod
    def malaria_total_consistent(cls, v, info):
        pv = info.data.get("pv_total", 0)
        pf = info.data.get("pf_total", 0)
        if v < pv + pf:
            raise ValueError(f"malaria_total ({v}) < pv_total ({pv}) + pf_total ({pf})")
        return v

    @property
    def tpr(self) -> float:
        return self.malaria_total / self.population if self.population > 0 else 0.0

    @property
    def api(self) -> float:
        """Annual Parasite Incidence per 1000 population."""
        return (self.malaria_total / self.population) * 1000 if self.population > 0 else 0.0


class AggregatedRecord(BaseModel):
    """Aggregated surveillance at block or district level."""
    year: int
    month: int
    district: str
    block: Optional[str] = None
    population: int
    fever: int
    pv_total: int
    pf_total: int
    malaria_total: int
    fever_proportion: float
    tpr: float
    api: float
    pf_fraction: float
