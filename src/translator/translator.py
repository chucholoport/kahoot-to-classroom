import re
import pandas as pd
import unicodedata
import difflib

from translator.config import kahoot_to_classroom

k2c = kahoot_to_classroom()

def split_camel(text: str) -> str:
    return re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text))
    
def keep_only_alphabetics(text: str):
    return re.sub(r'[^a-z\s]', '', ''.join(c for c in unicodedata.normalize('NFD', text.lower().replace('_', ' ')) if unicodedata.category(c) != 'Mn'))

def preprocess_text(text: str) -> str:
    return keep_only_alphabetics(split_camel(text).lower())

def tokenize_text(text: str, sep: str=' '):
    return [tok for tok in text.split(sep=sep) if tok and re.search(r'[a-zA-Z]', tok)]

def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()

def translate_report(report: pd.DataFrame, total:int, reference: list) -> pd.DataFrame:

    # Expected: real names in reference list
    expected = [tokenize_text(preprocess_text(line)) for line in reference]
    used = set()
    # Current: names in DataFrame
    current = report.copy()
    current['classroom'] = None
    
    # First evaluation: pass if two tokens match
    for idx, row in current.iterrows():
        tokens = tokenize_text(preprocess_text(row.Player))

        for exp_tokens, real_name in zip(expected, reference):
            matches = len(set(tokens) & set(exp_tokens))
            
            if matches >= 2:
                current.at[idx, 'classroom'] = real_name
                used.add(real_name)
                break

    # Second evaluation: pass if one token match and another has 60% similarity
    for idx, row in current[current['classroom'].isna()].iterrows():
        tokens = tokenize_text(preprocess_text(row.Player))

        for exp_tokens, real_name in zip(expected, reference):

            if real_name in used:
                continue 

            exact = any(tok in exp_tokens for tok in tokens)
            similar = any(similarity(tok, exp_tok) >= 0.6 for tok in tokens for exp_tok in exp_tokens)

            if exact and similar:
                current.at[idx, 'classroom'] = real_name
                used.add(real_name)
                break
    
    # Calculate grades with total
    current['Correct Answers'] = pd.to_numeric(current['Correct Answers'], errors='coerce')
    current['grade'] = (current['Correct Answers'].astype(float) / int(total)) * 100

    # Grade with 100 the podium winners
    current.loc[current['Rank'] <= 3, 'grade'] = 100.0
    
    # Keep only relevant columns
    current = current[['Player', 'classroom', 'grade']].rename(columns={'Player': 'name'})
    
    # Order according to reference
    current['classroom'] = pd.Categorical(
        current['classroom'],
        categories=reference,   # la lista de referencia original
        ordered=True
    )

    current = current.sort_values('classroom').reset_index(drop=True)

    return current
