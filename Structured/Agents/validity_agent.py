from .base_agent import BaseAgent
import pandas as pd
"""Type checker"""
class ValidityAgent(BaseAgent):
    def __init__(self):
        super().__init__('Validity')

    def evaluate(self, df):
        valid_cells = 0
        total_cells = df.size

        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                valid_cells += df[col].dropna().apply(lambda x: isinstance(x, (int, float))).sum()
            elif pd.api.types.is_string_dtype(df[col]):
                valid_cells += df[col].dropna().apply(lambda x: isinstance(x, str)).sum()
            else:
                valid_cells += df[col].notnull().sum()

        return round(valid_cells / total_cells, 4)
