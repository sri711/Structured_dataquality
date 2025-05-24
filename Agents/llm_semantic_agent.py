from .base_agent import BaseAgent
import google.generativeai as genai
import pandas as pd
import os
import time
from google.api_core import exceptions
"""Constraint learning and validation using LLMs"""
class LLMSemanticAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__("LLMSemantic")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")  # Using stable model
        self.delay = 1  # 1 second delay between API calls

    def _make_api_call(self, prompt):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                time.sleep(self.delay)  # Add delay after successful call
                return response
            except exceptions.ResourceExhausted as e:
                retry_delay = 30  # Default delay of 30 seconds
                print(f"\nRate limit reached. Waiting {retry_delay} seconds...")
                time.sleep(retry_delay)
                if attempt == max_retries - 1:
                    raise e
            except Exception as e:
                print(f"\nError during API call: {str(e)}")
                raise e

    def evaluate(self, df: pd.DataFrame) -> float:
        column_scores = []
        total_columns = len(df.columns)

        for col_idx, col in enumerate(df.columns, 1):
            print(f"\n[{col_idx}/{total_columns}] Processing column: '{col}'")
            
            sample_values = df[col].dropna().head(10).tolist()
            if not sample_values:
                print(f"⚠️ Column '{col}' is empty, skipping...")
                column_scores.append(1.0)
                continue

            # Step 1: Learn constraint with retry logic
            constraint_prompt = self._build_constraint_prompt(col, sample_values)
            constraint_response = self._make_api_call(constraint_prompt)
            constraint_description = constraint_response.text.strip()

            print(f"🔍 Inferred constraint: {constraint_description}")

            # Step 2: Check entries with retry logic
            valid_count = 0
            total_count = df[col].notna().sum()
            processed_count = 0

            print(f"⏳ Validating {total_count} values...")
            for val in df[col].dropna():
                processed_count += 1
                validation_prompt = self._build_validation_prompt(col, val, constraint_description)
                validation_response = self._make_api_call(validation_prompt)
                
                is_valid = self._is_valid(validation_response.text)
                valid_count += int(is_valid)
                
                status = "✅" if is_valid else "❌"
                print(f"  [{processed_count}/{total_count}] Value: '{val}' {status}")

            score = valid_count / total_count if total_count > 0 else 1.0
            print(f"📊 Column '{col}' score: {score:.4f} ({valid_count}/{total_count} valid)")
            column_scores.append(score)

        final_score = round(sum(column_scores) / len(column_scores), 4)
        print(f"\n🎯 Final score across all columns: {final_score}")
        return final_score

    def _build_constraint_prompt(self, column_name, values):
        return f"""
You are a data quality analyzer. Below is a column named '{column_name}' with sample values:
{values}

From these examples, infer the expected pattern or rule for valid data in this column.
Describe the rule clearly in 1-2 sentences.
        """

    def _build_validation_prompt(self, column_name, value, constraint_description):
        return f"""
You are validating a value for a column named '{column_name}'.
The expected rule is: {constraint_description}

Here is the value to check: '{value}'

Does this value follow the rule? Reply with "Yes" or "No".
        """

    def _is_valid(self, response_text):
        return "yes" in response_text.strip().lower()
