import numpy as np
from cipher_breaker.metropolis_hastings_2d import MetropolisHastings2D


class MetropolisHastings4D(MetropolisHastings2D):
    """A class to implement the Metropolis-Hastings algorithm for breaking ciphers in a four-dimensional context.

    This class extends the capabilities of the Metropolis-Hastings algorithm to handle four-dimensional transition matrices,
    allowing for more complex analysis of decrypted text. It provides methods to encrypt and decrypt text using a substitution cipher,
    and evaluates the plausibility of the decrypted text against a reference transition matrix specific to four-dimensional data.
    The algorithm iteratively refines the decryption key based on the likelihood of the decrypted text, enhancing the accuracy of the decryption process.

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
            # "smart" mutation based on bad 4-grams
            fourgrams = self.get_bigrams(decrypted_text)
            worst_score = float("inf")
            worst_fourgram = None

            for fg in fourgrams:
                # Ensure all four characters are in the alphabet
                idx0 = np.where(self.alphabet == fg[0])[0]
                idx1 = np.where(self.alphabet == fg[1])[0]
                idx2 = np.where(self.alphabet == fg[2])[0]
                idx3 = np.where(self.alphabet == fg[3])[0]
                if idx0.size == 0 or idx1.size == 0 or idx2.size == 0 or idx3.size == 0:
                    continue
                i = idx0[0]
                j = idx1[0]
                k = idx2[0]
                l = idx3[0]
                score = TM_ref[i, j, k, l]
                if score < worst_score:
                    worst_score = score
                    worst_fourgram = (fg[0], fg[1], fg[2], fg[3])

            if worst_fourgram:
                # Swap two characters from the worst fourgram in the key
                key_array = np.array(key)
                idxs = [np.where(key_array == c)[0] for c in worst_fourgram]
                # Only swap if at least two unique indices found
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
        return np.array([text[i : i + 4] for i in range(len(text) - 3)])

    def transition_matrix(self, bigrams: np.ndarray) -> np.ndarray:
        """Build the transition matrix for bigrams.

        Args:
            bigrams (np.ndarray): An array of bigrams for which to build the transition matrix.

        Returns:
            np.ndarray: The transition matrix representing the frequency of bigram occurrences.
        """
        n = len(self.alphabet)
        TM = np.zeros((n, n, n, n), dtype=int)

        for bigram in bigrams:
            c1, c2, c3, c4 = bigram[0], bigram[1], bigram[2], bigram[3]
            i = np.where(self.alphabet == c1)[0][0]
            j = np.where(self.alphabet == c2)[0][0]
            k = np.where(self.alphabet == c3)[0][0]
            l = np.where(self.alphabet == c4)[0][0]
            TM[i, j, k, l] += 1

        # Replace zeros with 1 to prevent log(0)
        TM[TM == 0] = 1
        return TM