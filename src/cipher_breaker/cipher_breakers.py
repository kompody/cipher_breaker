import numpy as np
import matplotlib.pyplot as plt


class CipherBreaker:
    def __init__(self, start_key: str = None):
        self.start_key = start_key if start_key else self.generate_random_key()

    def generate_random_key(self) -> str:
        pass

    def prolom_substitute(
        self, text: str, TM_ref: np.ndarray, iter: int, start_key: str
    ) -> tuple[str, str, float]:
        pass

    def get_bigrams(self, text: str) -> np.ndarray:
        pass

    def transition_matrix(self, bigrams: np.ndarray) -> np.ndarray:
        pass

    def plausibility(self, text: str, TM_ref: np.ndarray) -> float:
        pass

    def substitute_encrypt(self, plaintext: str, key: str) -> str:
        pass

    def substitute_decrypt(self, ciphertext: str, key: str) -> str:
        pass

    def plot_plausibility(self, scores: list):
        """Plot the plausibility scores over iterations.

        Args:
            scores (list): A list of plausibility scores to plot.

        Sample usage:
        >>> cipher_breaker = MetropolisHastings()
        >>> cipher_breaker.prolom_substitute(text, TM_ref, iter, start_key)
        >>> cipher_breaker.plot_plausibility(cipher_breaker.plausibility_scores)
        """
        plt.plot(scores)
        plt.title("Plausibility Scores Over Iterations")
        plt.xlabel("Iteration")
        plt.ylabel("Plausibility Score")
        plt.grid()
        plt.show()

