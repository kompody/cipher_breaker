import numpy as np
from cipher_breaker.metropolis_hastings_2d import MetropolisHastings2D


class MetropolisHastings3D(MetropolisHastings2D):
    """A class to implement the Metropolis-Hastings algorithm for breaking ciphers.

    This class provides methods to encrypt and decrypt text using a substitution cipher,
    as well as to analyze the plausibility of decrypted text against a reference transition matrix.
    It utilizes the Metropolis-Hastings algorithm to iteratively improve the decryption key
    based on the likelihood of the decrypted text.

    Attributes:
        alphabet (np.ndarray): An array representing the characters used in the cipher.
        start_key (str): The initial key for decryption, which can be randomly generated.
    """

    def __init__(self, start_key: str = None):
        super().__init__(start_key)

    def mutate_key_smart(self, key: str, decrypted_text: str, TM_ref: np.ndarray) -> str:
        key = list(key)

        if np.random.rand() < 0.5:
            # simple permutation
            a, b = np.random.choice(len(self.alphabet), 2, replace=False)
            key[a], key[b] = key[b], key[a]
        else:
            # "smart" mutation based on bad bigrams
            bigrams = self.get_bigrams(decrypted_text)
            worst_score = float("inf")
            worst_bigram = None

            for bg in bigrams:
                # Ensure all three characters are in the alphabet
                idx0 = np.where(self.alphabet == bg[0])[0]
                idx1 = np.where(self.alphabet == bg[1])[0]
                idx2 = np.where(self.alphabet == bg[2])[0]
                if idx0.size == 0 or idx1.size == 0 or idx2.size == 0:
                    continue
                i = idx0[0]
                j = idx1[0]
                k = idx2[0]
                score = TM_ref[i, j, k]
                if score < worst_score:
                    worst_score = score
                    worst_bigram = (bg[0], bg[1], bg[2])

            if worst_bigram is not None:
                key_array = np.array(key)
                idxs = [np.where(key_array == c)[0] for c in worst_bigram]
                found_idxs = [idx[0] for idx in idxs if idx.size > 0]
                if len(found_idxs) >= 2:
                    i1, i2 = found_idxs[0], found_idxs[1]
                    key[i1], key[i2] = key[i2], key[i1]

        return "".join(key)

    def get_bigrams(self, text: str) -> np.ndarray:
        """Function to get bigrams from the text.

        Args:
            text (str): The input text from which to extract bigrams.

        Returns:
            np.ndarray: An array of bigrams extracted from the input text.
        """
        return np.array([text[i : i + 3] for i in range(len(text) - 2)])

    def transition_matrix(self, bigrams: np.ndarray) -> np.ndarray:
        """Build the transition matrix for bigrams.

        Args:
            bigrams (np.ndarray): An array of bigrams for which to build the transition matrix.

        Returns:
            np.ndarray: The transition matrix representing the frequency of bigram occurrences.
        """
        n = len(self.alphabet)
        TM = np.zeros((n, n, n), dtype=int)

        for bigram in bigrams:
            c1, c2, c3 = bigram[0], bigram[1], bigram[2]
            i = np.where(self.alphabet == c1)[0][0]
            j = np.where(self.alphabet == c2)[0][0]
            k = np.where(self.alphabet == c3)[0][0]
            TM[i, j, k] += 1

        # Replace zeros with 1 to prevent log(0)
        TM[TM == 0] = 1
        return TM