from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class Financials(BaseModel):
    timestamp: datetime
    checking_account: Optional[Optional[float]] = Field(None, serialization_alias="checkingAccount")
    long_term_investments: Optional[float] = Field(None, serialization_alias="longTermInvestments")
    total_investments: Optional[float] = Field(None, serialization_alias="totalInvestments")
    physical_assets: Optional[float] = Field(None, serialization_alias="physicalAssets")
    total_actives: Optional[float] = Field(None, serialization_alias="totalActives")
    loans: Optional[float] = Field(None,)
    total_passives: Optional[float] = Field(None, serialization_alias="totalPassives")
    total_donations: Optional[float] = Field(None, serialization_alias="totalDonations")
    federal_revenue: Optional[float] = Field(None, serialization_alias="federalRevenue")
    provincial_revenue: Optional[float] = Field(None, serialization_alias="provincialRevenue")
    municipal_revenue: Optional[float] = Field(None, serialization_alias="municipalRevenue")
    total_revenue: Optional[float] = Field(None, serialization_alias="totalRevenue")
    interest_and_banking_fees: Optional[float] = Field(None, serialization_alias="interestAndBankingFees")
    occupation_cost: Optional[float] = Field(None, serialization_alias="occupationCost")
    professional_fees: Optional[float] = Field(None, serialization_alias="professionalFees")
    salaries: Optional[float] = Field(None)
    fixed_asset_depreciation: Optional[float] = Field(None, serialization_alias="fixedAssetDepreciation")
    others: Optional[float] = Field(None)
    total_expenses: Optional[float] = Field(None, serialization_alias="totalExpenses")