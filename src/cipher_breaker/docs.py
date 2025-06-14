"""
Cipher Breaker Library Documentation
===================================

This library provides implementations of various cipher breaking algorithms using the Metropolis-Hastings algorithm
for cryptanalysis of substitution ciphers.

Main Components
--------------
1. CipherBreaker (Abstract Base Class)
2. MetropolisHastings (Base Implementation)
3. MetropolisHastings2D (2D Implementation)
4. MetropolisHastings3D (3D Implementation)
5. MetropolisHastings4D (4D Implementation)
6. CipherBreakerWrapper (Utility Wrapper)
7. Transition Matrix References (tm_refs module)

CipherBreaker Class
------------------
Abstract base class that defines the interface for all cipher breaking implementations.

Methods:
    - generate_random_key() -> str
        Generates a random substitution key.
    
    - prolom_substitute(text: str, TM_ref: np.ndarray, iter: int, start_key: str) -> tuple[str, str, float]
        Attempts to break a substitution cipher using the provided reference transition matrix.
        Returns: (decrypted_text, key, final_plausibility)
    
    - get_bigrams(text: str) -> np.ndarray
        Extracts bigrams from the input text.
    
    - transition_matrix(bigrams: np.ndarray) -> np.ndarray
        Computes the transition matrix from bigrams.
    
    - plausibility(text: str, TM_ref: np.ndarray) -> float
        Calculates the plausibility score of the text against the reference transition matrix.
    
    - substitute_encrypt(plaintext: str, key: str) -> str
        Encrypts plaintext using the substitution key.
    
    - substitute_decrypt(ciphertext: str, key: str) -> str
        Decrypts ciphertext using the substitution key.
    
    - plot_plausibility(scores: list)
        Plots the plausibility scores over iterations.

MetropolisHastings Class
-----------------------
Base implementation of the Metropolis-Hastings algorithm for cipher breaking.

MetropolisHastings2D/3D/4D Classes
---------------------------------
Specialized implementations of the Metropolis-Hastings algorithm with different dimensionality.

CipherBreakerWrapper Class
-------------------------
Utility wrapper that provides a simplified interface for using the cipher breaking functionality.

Transition Matrix References (tm_refs)
------------------------------------
Module providing access to pre-computed transition matrices and reference text from the novel "Krakatit".

Functions:
    - get_krakatit_text() -> str
        Returns the full text of the novel "Krakatit" used for training.
    
    - get_krakatit_2d_tm() -> np.ndarray
        Returns the 2D transition matrix computed from "Krakatit".
    
    - get_krakatit_3d_tm() -> np.ndarray
        Returns the 3D transition matrix computed from "Krakatit".
    
    - get_krakatit_4d_tm() -> np.ndarray
        Returns the 4D transition matrix computed from "Krakatit".

Usage Example
------------
```python
from cipher_breaker import MetropolisHastings, CipherBreakerWrapper
from cipher_breaker.tm_refs import get_krakatit_2d_tm

# Using the base implementation with Krakatit reference matrix
breaker = MetropolisHastings()
reference_matrix = get_krakatit_2d_tm()
decrypted_text, key, score = breaker.prolom_substitute(
    ciphertext,
    reference_matrix,
    iterations=1000,
    start_key="optional_start_key"
)

# Using the wrapper
wrapper = CipherBreakerWrapper()
result = wrapper.break_cipher(
    ciphertext,
    reference_matrix,
    iterations=1000
)
```

Dependencies
-----------
- numpy: For numerical computations and array operations
- matplotlib: For plotting plausibility scores
- pytest: For running tests

Installation
-----------
The library can be installed using pip:
```bash
pip install cipher-breaker
```

License
-------
This project is licensed under the terms of the license included in the LICENSE file.

Reference Data
-------------
The library includes pre-computed transition matrices based on the novel "Krakatit" by Karel Čapek:
- 2D transition matrix (krakatit_2d.npy): Character pair frequencies
- 3D transition matrix (krakatit_3d.npy): Character triplet frequencies
- 4D transition matrix (krakatit_4d.npy): Character quadruplet frequencies

These matrices are used as reference data for the cipher breaking algorithms to improve their accuracy
in breaking substitution ciphers based on Czech language patterns.
""" 