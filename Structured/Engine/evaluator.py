# python -m Structured.Engine.evaluator "Structured\Data\dummy.csv"
import sys
import argparse
import os
from dotenv import load_dotenv
sys.path.append('..')  # Add parent directory to Python path

from Structured.Agents.accuracy_agent import AccuracyAgent
from Structured.Agents.llm_semantic_agent import LLMSemanticAgent
from Structured.Agents.completeness_agent import CompletenessAgent
from Structured.Agents.consistency_agent import ConsistencyAgent
from Structured.Agents.validity_agent import ValidityAgent
from Structured.Agents.uniqueness_agent import UniquenessAgent
from Structured.Engine.loader import load_data

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def evaluate_all(df):
    # Get API key from environment variable
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    agents = [
        AccuracyAgent(),
        CompletenessAgent(),
        ConsistencyAgent(),
        ValidityAgent(),
        UniquenessAgent(),
        LLMSemanticAgent(api_key=api_key)
    ]

    results = {}
    for agent in agents:
        results[agent.name] = agent.evaluate(df)

    results['Overall Score'] = round(sum(results.values()) / len(results), 4)
    return results
def main():
    parser = argparse.ArgumentParser(description='Run data quality evaluation on a structured data file.')
    parser.add_argument('file_path', type=str, help='Path to the data file (csv, tsv, xls, xlsx)')
    args = parser.parse_args()

    try:
        df = load_data(args.file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

    results = evaluate_all(df)

    print("\nData Quality Scores:")
    for k, v in results.items():
        print(f"{k}: {v:.4f}")


if __name__ == "__main__":
    main()