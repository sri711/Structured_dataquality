from .base_agent import BaseAgent
"""Non null values in the dataset"""
class CompletenessAgent(BaseAgent):
    def __init__(self):
        super().__init__('Completeness')

    def evaluate(self, df):
        missing = df.isnull().sum().sum()
        total = df.size
        return round(1 - (missing / total), 4)
