class BaseAgent:
    def __init__(self, name):
        self.name = name

    def evaluate(self, df):
        raise NotImplementedError