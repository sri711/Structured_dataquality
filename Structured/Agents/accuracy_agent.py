from .base_agent import BaseAgent
import pandas as pd
"""majority Type checker"""
class AccuracyAgent(BaseAgent):
    def __init__(self):
        super().__init__('Accuracy')

    def evaluate(self, df):
        incorrect_cells = 0
        total_cells = df.size

        for col in df.columns:
            expected_dtype = df[col].dropna().map(type).mode()[0] if not df[col].dropna().empty else None
            if expected_dtype:
                incorrect_cells += (~df[col].dropna().map(type).eq(expected_dtype)).sum()

        return round(1 - (incorrect_cells / total_cells), 4)