import os
import pandas as pd
import numpy as np

def get_krakatit_text() -> str:
    """Load the text of Krakatit from a text file.

    Returns:
        str: A string containing the preprocessed text of Krakatit (e.g., uppercased, non-alphabetic characters removed, and underscores for spaces).
    """
    file_path = os.path.join(os.path.dirname(__file__), "krakatit.txt")
    with open(file_path, "r") as file:
        return file.read()
    
def get_krakatit_2d_tm() -> np.ndarray:
    """Load the 2D transition matrix of Krakatit from a NumPy .npy file.

    Returns:
        np.ndarray: A NumPy array containing the 2D transition matrix.
    """
    return np.load("krakatit_2d.npy")

def get_krakatit_3d_tm() -> np.ndarray:
    """Load the 3D transition matrix of Krakatit from a NumPy .npy file.

    Returns:
        np.ndarray: A NumPy array containing the 3D transition matrix.
    """
    return np.load("krakatit_3d.npy")

def get_krakatit_4d_tm() -> np.ndarray:
    """Load the 4D transition matrix of Krakatit from a NumPy .npy file.

    Returns:
        np.ndarray: A NumPy array containing the 4D transition matrix.
    """
    return np.load("krakatit_4d.npy")

