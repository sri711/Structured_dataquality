from .base_agent import BaseAgent
"""Unique entries per column in the dataset"""
class UniquenessAgent(BaseAgent):
    def __init__(self):
        super().__init__('Uniqueness')

    def evaluate(self, df):
        total_values = df.size  # total number of cells (rows * columns)
        unique_values = sum(df[col].nunique(dropna=True) for col in df.columns)  # sum of unique counts in each column
        return round(unique_values / total_values, 4) if total_values > 0 else 1.0
