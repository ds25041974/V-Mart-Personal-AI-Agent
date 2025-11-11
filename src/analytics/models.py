"""
Analytics Data Models for V-Mart Store Intelligence

This module provides data models for sales analytics, inventory optimization,
competition analysis, and business insights.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from enum import Enum


class AnalysisType(Enum):
    """Types of analytics analyses"""
    SALES_TREND = "sales_trend"
    INVENTORY_OPTIMIZATION = "inventory_optimization"
    COMPETITION_IMPACT = "competition_impact"
    WEATHER_CORRELATION = "weather_correlation"
    DEMAND_FORECAST = "demand_forecast"
    OVERALL_INSIGHTS = "overall_insights"


class InsightPriority(Enum):
    """Priority levels for insights"""
    CRITICAL = "critical"  # Immediate action required
    HIGH = "high"  # Action needed within 24-48 hours
    MEDIUM = "medium"  # Action needed within a week
    LOW = "low"  # Monitor and plan


class InsightCategory(Enum):
    """Categories of business insights"""
    SALES = "sales"
    INVENTORY = "inventory"
    COMPETITION = "competition"
    WEATHER = "weather"
    OPERATIONS = "operations"
    CUSTOMER = "customer"


@dataclass
class SalesData:
    """Sales data for a store on a specific date"""
    store_id: str
    date: date
    period: str  # Morning, Afternoon, Evening, Night
    total_sales: float
    transaction_count: int
    average_transaction_value: float
    category_sales: Dict[str, float]  # Category -> Sales amount
    footfall: int
    conversion_rate: float  # Percentage
    
    def to_dict(self) -> dict:
        return {
            "store_id": self.store_id,
            "date": self.date.isoformat(),
            "period": self.period,
            "total_sales": self.total_sales,
            "transaction_count": self.transaction_count,
            "average_transaction_value": self.average_transaction_value,
            "category_sales": self.category_sales,
            "footfall": self.footfall,
            "conversion_rate": self.conversion_rate,
        }


@dataclass
class InventoryData:
    """Inventory data for a store"""
    store_id: str
    date: date
    category: str
    stock_level: int
    reorder_point: int
    days_of_supply: float
    stockout_incidents: int
    overstock_value: float
    turnover_rate: float  # Times per month
    
    def to_dict(self) -> dict:
        return {
            "store_id": self.store_id,
            "date": self.date.isoformat(),
            "category": self.category,
            "stock_level": self.stock_level,
            "reorder_point": self.reorder_point,
            "days_of_supply": self.days_of_supply,
            "stockout_incidents": self.stockout_incidents,
            "overstock_value": self.overstock_value,
            "turnover_rate": self.turnover_rate,
        }


@dataclass
class SalesTrend:
    """Sales trend analysis"""
    store_id: str
    period_start: date
    period_end: date
    total_sales: float
    sales_growth: float  # Percentage change
    average_daily_sales: float
    peak_sales_day: str  # Day of week
    peak_sales_period: str  # Morning/Afternoon/Evening/Night
    trending_categories: List[Tuple[str, float]]  # Category, growth %
    underperforming_categories: List[Tuple[str, float]]
    
    def to_dict(self) -> dict:
        return {
            "store_id": self.store_id,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "total_sales": self.total_sales,
            "sales_growth": self.sales_growth,
            "average_daily_sales": self.average_daily_sales,
            "peak_sales_day": self.peak_sales_day,
            "peak_sales_period": self.peak_sales_period,
            "trending_categories": [{"category": cat, "growth": growth} 
                                   for cat, growth in self.trending_categories],
            "underperforming_categories": [{"category": cat, "decline": decline} 
                                          for cat, decline in self.underperforming_categories],
        }


@dataclass
class WeatherImpactAnalysis:
    """Analysis of weather impact on sales"""
    store_id: str
    weather_condition: str
    temperature_range: Tuple[float, float]  # Min, Max
    average_sales: float
    sales_variance: float  # Percentage from normal
    recommended_actions: List[str]
    affected_categories: List[Tuple[str, float]]  # Category, impact %
    
    def to_dict(self) -> dict:
        return {
            "store_id": self.store_id,
            "weather_condition": self.weather_condition,
            "temperature_range": {
                "min": self.temperature_range[0],
                "max": self.temperature_range[1]
            },
            "average_sales": self.average_sales,
            "sales_variance": self.sales_variance,
            "recommended_actions": self.recommended_actions,
            "affected_categories": [{"category": cat, "impact": impact} 
                                   for cat, impact in self.affected_categories],
        }


@dataclass
class CompetitionImpact:
    """Competition impact analysis"""
    store_id: str
    competitor_count: int
    nearest_competitor_distance: float  # km
    estimated_market_share: float  # Percentage
    sales_impact: float  # Percentage (negative = loss due to competition)
    competitive_advantages: List[str]
    competitive_threats: List[str]
    recommended_strategies: List[str]
    
    def to_dict(self) -> dict:
        return {
            "store_id": self.store_id,
            "competitor_count": self.competitor_count,
            "nearest_competitor_distance": self.nearest_competitor_distance,
            "estimated_market_share": self.estimated_market_share,
            "sales_impact": self.sales_impact,
            "competitive_advantages": self.competitive_advantages,
            "competitive_threats": self.competitive_threats,
            "recommended_strategies": self.recommended_strategies,
        }


@dataclass
class InventoryRecommendation:
    """Inventory optimization recommendation"""
    store_id: str
    category: str
    current_stock: int
    recommended_stock: int
    reorder_quantity: int
    reorder_urgency: InsightPriority
    estimated_stockout_risk: float  # Percentage
    estimated_overstock_cost: float
    reasoning: str
    seasonal_factors: List[str]
    
    def to_dict(self) -> dict:
        return {
            "store_id": self.store_id,
            "category": self.category,
            "current_stock": self.current_stock,
            "recommended_stock": self.recommended_stock,
            "reorder_quantity": self.reorder_quantity,
            "reorder_urgency": self.reorder_urgency.value,
            "estimated_stockout_risk": self.estimated_stockout_risk,
            "estimated_overstock_cost": self.estimated_overstock_cost,
            "reasoning": self.reasoning,
            "seasonal_factors": self.seasonal_factors,
        }


@dataclass
class DemandForecast:
    """Demand forecast based on multiple factors"""
    store_id: str
    forecast_date: date
    category: str
    predicted_demand: float
    confidence_level: float  # 0-100%
    influencing_factors: Dict[str, float]  # Factor -> Impact weight
    weather_factor: str
    competition_factor: float
    seasonal_factor: float
    trend_factor: float
    
    def to_dict(self) -> dict:
        return {
            "store_id": self.store_id,
            "forecast_date": self.forecast_date.isoformat(),
            "category": self.category,
            "predicted_demand": self.predicted_demand,
            "confidence_level": self.confidence_level,
            "influencing_factors": self.influencing_factors,
            "weather_factor": self.weather_factor,
            "competition_factor": self.competition_factor,
            "seasonal_factor": self.seasonal_factor,
            "trend_factor": self.trend_factor,
        }


@dataclass
class BusinessInsight:
    """Actionable business insight"""
    insight_id: str
    store_id: str
    category: InsightCategory
    priority: InsightPriority
    title: str
    description: str
    impact: str  # Expected business impact
    recommended_actions: List[str]
    data_sources: List[str]  # Which data contributed
    confidence_score: float  # 0-100%
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            "insight_id": self.insight_id,
            "store_id": self.store_id,
            "category": self.category.value,
            "priority": self.priority.value,
            "title": self.title,
            "description": self.description,
            "impact": self.impact,
            "recommended_actions": self.recommended_actions,
            "data_sources": self.data_sources,
            "confidence_score": self.confidence_score,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }


@dataclass
class PerformanceMetrics:
    """Overall store performance metrics"""
    store_id: str
    period_start: date
    period_end: date
    
    # Sales metrics
    total_revenue: float
    revenue_growth: float  # Percentage
    average_transaction_value: float
    transaction_count: int
    
    # Operational metrics
    inventory_turnover: float
    stockout_rate: float  # Percentage
    overstock_cost: float
    
    # Competition metrics
    market_share_estimate: float  # Percentage
    competitive_position: str  # "Leading", "Strong", "Moderate", "Weak"
    
    # Customer metrics
    footfall: int
    conversion_rate: float  # Percentage
    
    # Weather impact
    weather_impact_score: float  # -100 to +100
    
    def to_dict(self) -> dict:
        return {
            "store_id": self.store_id,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "sales_metrics": {
                "total_revenue": self.total_revenue,
                "revenue_growth": self.revenue_growth,
                "average_transaction_value": self.average_transaction_value,
                "transaction_count": self.transaction_count,
            },
            "operational_metrics": {
                "inventory_turnover": self.inventory_turnover,
                "stockout_rate": self.stockout_rate,
                "overstock_cost": self.overstock_cost,
            },
            "competition_metrics": {
                "market_share_estimate": self.market_share_estimate,
                "competitive_position": self.competitive_position,
            },
            "customer_metrics": {
                "footfall": self.footfall,
                "conversion_rate": self.conversion_rate,
            },
            "weather_impact_score": self.weather_impact_score,
        }


# Database schema for analytics tables
ANALYTICS_DATABASE_SCHEMA = """
-- Sales data table
CREATE TABLE IF NOT EXISTS sales_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id TEXT NOT NULL,
    date DATE NOT NULL,
    period TEXT NOT NULL,
    total_sales REAL NOT NULL,
    transaction_count INTEGER NOT NULL,
    average_transaction_value REAL NOT NULL,
    category_sales TEXT NOT NULL,  -- JSON
    footfall INTEGER NOT NULL,
    conversion_rate REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES vmart_stores(store_id)
);

CREATE INDEX IF NOT EXISTS idx_sales_store_date ON sales_data(store_id, date);
CREATE INDEX IF NOT EXISTS idx_sales_period ON sales_data(period);

-- Inventory data table
CREATE TABLE IF NOT EXISTS inventory_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id TEXT NOT NULL,
    date DATE NOT NULL,
    category TEXT NOT NULL,
    stock_level INTEGER NOT NULL,
    reorder_point INTEGER NOT NULL,
    days_of_supply REAL NOT NULL,
    stockout_incidents INTEGER DEFAULT 0,
    overstock_value REAL DEFAULT 0,
    turnover_rate REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES vmart_stores(store_id)
);

CREATE INDEX IF NOT EXISTS idx_inventory_store_date ON inventory_data(store_id, date);
CREATE INDEX IF NOT EXISTS idx_inventory_category ON inventory_data(category);

-- Business insights table
CREATE TABLE IF NOT EXISTS business_insights (
    insight_id TEXT PRIMARY KEY,
    store_id TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    impact TEXT NOT NULL,
    recommended_actions TEXT NOT NULL,  -- JSON
    data_sources TEXT NOT NULL,  -- JSON
    confidence_score REAL NOT NULL,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP,
    acknowledged BOOLEAN DEFAULT 0,
    FOREIGN KEY (store_id) REFERENCES vmart_stores(store_id)
);

CREATE INDEX IF NOT EXISTS idx_insights_store ON business_insights(store_id);
CREATE INDEX IF NOT EXISTS idx_insights_priority ON business_insights(priority);
CREATE INDEX IF NOT EXISTS idx_insights_category ON business_insights(category);

-- Demand forecasts table
CREATE TABLE IF NOT EXISTS demand_forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id TEXT NOT NULL,
    forecast_date DATE NOT NULL,
    category TEXT NOT NULL,
    predicted_demand REAL NOT NULL,
    confidence_level REAL NOT NULL,
    influencing_factors TEXT NOT NULL,  -- JSON
    weather_factor TEXT,
    competition_factor REAL,
    seasonal_factor REAL,
    trend_factor REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES vmart_stores(store_id)
);

CREATE INDEX IF NOT EXISTS idx_forecast_store_date ON demand_forecasts(store_id, forecast_date);
"""
