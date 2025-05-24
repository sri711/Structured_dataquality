import pandas as pd

def load_data(file_path):
    if file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.tsv'):
        return pd.read_csv(file_path, sep='\t')
    else:
        raise ValueError("Unsupported file format")

