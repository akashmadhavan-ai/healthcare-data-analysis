"""
Healthcare Analytics Core Package
---------------------------------

This package contains the main backend
modules for the Healthcare Analytics
Platform.

Modules:
    - loader
    - cleaner
    - analyzer
    - insights
    - visualizer
    - report_generator
    - export_manager
    - domain_detector
"""

# Data Loading
from .loader import (
    DataLoader,
    SampleDataLoader
)

# Data Cleaning
from .cleaner import (
    DataCleaner
)

# Analytics
from .analyzer import (
    DataAnalyzer
)

# Insights
from .insights import (
    InsightGenerator
)

# Visualization
from .visualizer import (
    DataVisualizer
)

# Reporting
from .report_generator import (
    ReportGenerator
)

# Export System
from .export_manager import (
    ExportManager
)

# Domain Detection
from .domain_detector import (
    detect_healthcare_domain
)

__all__ = [
    "DataLoader",
    "SampleDataLoader",
    "DataCleaner",
    "DataAnalyzer",
    "InsightGenerator",
    "DataVisualizer",
    "ReportGenerator",
    "ExportManager",
    "detect_healthcare_domain"
]