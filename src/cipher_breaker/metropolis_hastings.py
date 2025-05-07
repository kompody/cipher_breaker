import numpy as np
from .cipher_breakers import CipherBreaker


class MetropolisHastings(CipherBreaker):
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
        self.alphabet = np.array(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_"))
        self.start_key = start_key if start_key else self.generate_random_key()
        self.plausibility_scores = []

    def prolom_substitute(
        self, text: str, TM_ref: np.ndarray, iter: int, start_key: str
    ) -> tuple[str, str, float]:
        """Main function for breaking the cipher using the Metropolis-Hastings algorithm.

        Args:
            text (str): The text to be decrypted.
            TM_ref (np.ndarray): The transition matrix reference for plausibility calculation.
            iter (int): The number of iterations to perform.
            start_key (str): The initial key for decryption.

        Returns:
            tuple[str, str, float]: A tuple containing the best key found, the decrypted text, and the plausibility score.
        """
        current_key = start_key
        decrypted_current = self.substitute_decrypt(text, current_key)
        p_current = self.plausibility(decrypted_current, TM_ref)
        self.plausibility_scores.append(p_current)

        for i in range(iter):
            candidate_key = list(current_key)
            indices = np.random.choice(len(self.alphabet), 2, replace=False)
            candidate_key[indices[0]], candidate_key[indices[1]] = candidate_key[indices[1]], candidate_key[indices[0]]
            candidate_key = "".join(candidate_key)

            decrypted_candidate = self.substitute_decrypt(text, candidate_key)
            p_candidate = self.plausibility(decrypted_candidate, TM_ref)

            q = p_candidate / p_current

            if q > 1 or np.random.uniform(0, 1) < 0.01:
                current_key, p_current = candidate_key, p_candidate

            self.plausibility_scores.append(p_current)

            if i % 50 == 0:
                print(f"Iteration: {i}, log plausibility: {p_current}")

        best_decrypted_text = self.substitute_decrypt(text, current_key)
        return current_key, best_decrypted_text, p_current

    def generate_random_key(self) -> str:
        """Generate a random key for the cipher.

        Returns:
            str: A randomly generated key for the cipher.
        """
        return "".join(
            np.random.choice(self.alphabet, size=len(self.alphabet), replace=False)
        )

    def get_bigrams(self, text: str) -> np.ndarray:
        """Function to get bigrams from the text.

        Args:
            text (str): The input text from which to extract bigrams.

        Returns:
            np.ndarray: An array of bigrams extracted from the input text.
        """
        return np.array([text[i : i + 2] for i in range(len(text) - 1)])

    def transition_matrix(self, bigrams: np.ndarray) -> np.ndarray:
        """Build the transition matrix for bigrams.

        Args:
            bigrams (np.ndarray): An array of bigrams for which to build the transition matrix.

        Returns:
            np.ndarray: The transition matrix representing the frequency of bigram occurrences.
        """
        n = len(self.alphabet)
        TM = np.zeros((n, n), dtype=int)

        for bigram in bigrams:
            c1, c2 = bigram[0], bigram[1]
            i = np.where(self.alphabet == c1)[0][0]
            j = np.where(self.alphabet == c2)[0][0]
            TM[i, j] += 1

        # Replace zeros with 1 to prevent log(0)
        TM[TM == 0] = 1
        return TM

    def plausibility(self, text: str, TM_ref: np.ndarray) -> float:
        """Calculate the plausibility of the text relative to the reference transition matrix.

        Args:
            text (str): The input text for which to calculate plausibility.
            TM_ref (np.ndarray): The reference transition matrix for comparison.

        Returns:
            float: The calculated plausibility of the text.
        """
        bigrams_obs = self.get_bigrams(text)
        TM_obs = self.transition_matrix(bigrams_obs)
        likelihood = np.sum(np.log(TM_ref) * TM_obs)

        return likelihood

    def substitute_encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt the text using the key.

        Args:
            plaintext (str): The text to be encrypted.
            key (str): The key used for encryption.

        Returns:
            str: The encrypted text.
        """
        key_array = np.array(list(key))
        encrypted_text = "".join(
            map(
                lambda char: (
                    key_array[np.where(self.alphabet == char)[0][0]]
                    if char in self.alphabet
                    else char
                ),
                plaintext,
            )
        )
        return encrypted_text

    def substitute_decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt the text using the key.

        Args:
            ciphertext (str): The text to be decrypted.
            key (str): The key used for decryption.

        Returns:
            str: The decrypted text.
        """
        key_array = np.array(list(key))
        decrypted_text = "".join(
            map(
                lambda char: (
                    self.alphabet[np.where(key_array == char)[0][0]]
                    if char in key_array
                    else char
                ),
                ciphertext,
            )
        )
        return decrypted_text
