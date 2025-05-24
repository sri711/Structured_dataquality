from .base_agent import BaseAgent
import pandas as pd
"""Numerical consistency of three standard deviations from the mean for numerical columns"""
"""deviation from mode for textual data"""
class ConsistencyAgent(BaseAgent):
    def __init__(self):
        super().__init__('Consistency')

    def evaluate(self, df):
        consistent_cells = 0
        total_cells = df.size

        for col in df.columns:
            col_series = df[col].dropna()
            if pd.api.types.is_numeric_dtype(col_series):
                if len(col_series) > 1:
                    std = col_series.std()
                    consistent_cells += col_series.between(col_series.mean() - 3 * std, col_series.mean() + 3 * std).sum()
            else:
                top_value = col_series.mode().values[0] if not col_series.mode().empty else None
                consistent_cells += col_series.eq(top_value).sum()

        return round(consistent_cells / total_cells, 4)

