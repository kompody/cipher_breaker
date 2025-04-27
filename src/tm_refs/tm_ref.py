import numpy as np
import pandas as pd

def krakatit() -> pd.DataFrame:
    return pd.read_csv("./tm_krakatit.csv", header=None)

def save_bigrams(bigrams: pd.DataFrame, path: str):
    pd.DataFrame(bigrams).to_csv(path, header=False, index=False)

def save_bigrams(bigrams: np.ndarray, path: str):
    pd.DataFrame(bigrams).to_csv(path, header=False, index=False)

def load_bigrams(path: str) -> pd.DataFrame:
    return pd.read_csv(path, header=None)