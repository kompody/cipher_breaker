import os
import numpy as np
import pandas as pd


def krakatit() -> pd.DataFrame:
    file_path = os.path.join(os.path.dirname(__file__), "tm_krakatit.csv")
    return pd.read_csv(file_path, header=None)


def save_bigrams(bigrams: pd.DataFrame, path: str):
    pd.DataFrame(bigrams).to_csv(path, header=False, index=False)


def save_bigrams(bigrams: np.ndarray, path: str):
    pd.DataFrame(bigrams).to_csv(path, header=False, index=False)


def load_bigrams(path: str) -> pd.DataFrame:
    return pd.read_csv(path, header=None)
