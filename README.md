# Structured Data Quality Framework

A modular Python framework for automated data quality assessment using multiple specialized agents and LLM-based semantic analysis specifically for strucured data

## 🌟 Features

- Multiple specialized data quality agents
- LLM-powered semantic validation using Google's Gemini LLM
- Comprehensive scoring system
- Support for CSV and Excel files
- Detailed quality reports

## 📁 Project Structure

```
Structured
│
├── data/
│   └── monthly_index_202504.xls  # Sample data
│   └── dummy.csv                 # Test dataset
│
├── agents/
│   ├── base_agent.py            # Abstract base class for all agents
│   ├── accuracy_agent.py        # Validates data accuracy through type checks
│   ├── completeness_agent.py    # Checks for missing values
│   ├── validity_agent.py        # Data type validation
│   ├── consistency_agent.py     # Statistical consistency checks
│   ├── uniqueness_agent.py      # Duplicate detection
│   └── llm_semantic_agent.py    # LLM-based constraint validation
│
├── engine/
│   ├── loader.py               # Data ingestion and preprocessing
│   ├── evaluator.py            # Agent orchestration
│   └── .env                    # Configuration (API keys)
```

## 🚀 Quick Start

1. **Setup Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Configure API Keys**
Create `.env` file in the Engine directory:
```env
GOOGLE_API_KEY=your_api_key_here
```

3. **Run Analysis**
```bash
python -m Structured.Engine.evaluator "Data/dummy.csv"
```

## 📊 Quality Dimensions

1. **Accuracy**
   - Type matching

2. **Completeness**
   - Null detection
   - Empty string checking

3. **Consistency**
   - Statistical anomaly detection
   - Mode deviation for textual data
   - Standard deviation for numerical data

4. **Validity**
   - Data type verification
   - Format validation

5. **Uniqueness**
   - Duplicate detection
   - Column-wise uniqueness

6. **Semantic**
   - LLM-based constraint learning
   - Natural language validation


## 🛠 Dependencies

- pandas: Data manipulation
- numpy: Numerical operations
- google-generativeai: LLM integration
- python-dotenv: Environment configuration


## 📈 Scoring System

Each agent produces a score between 0 and 1:
- 1.0: Perfect quality
- 0.0: Complete failure

Overall score is calculated as:
```python
final_score = sum(agent_scores) / len(agents)
```
