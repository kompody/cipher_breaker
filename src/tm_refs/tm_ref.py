import os
import pandas as pd


def krakatit() -> pd.DataFrame:
    """Load the transition matrix of Krakatit from a CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the transition matrix loaded from the CSV file.
    """
    file_path = os.path.join(os.path.dirname(__file__), "tm_krakatit.csv")
    return pd.read_csv(file_path, header=None).values