import numpy as np
from .cipher_breakers import CipherBreaker


class MetropolisHastings4D(CipherBreaker):
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
        
        best_key = current_key
        best_score = p_current
        
        initial_temperature = 5.0
        cooling_rate = 0.999

        for i in range(iter):
            candidate_key = self.mutate_key_smart(current_key, decrypted_current, TM_ref)

            decrypted_candidate = self.substitute_decrypt(text, candidate_key)
            p_candidate = self.plausibility(decrypted_candidate, TM_ref)
            
            if p_candidate > best_score:
                best_score = p_candidate
                best_key = candidate_key

            T = initial_temperature * (cooling_rate ** i)
            accept_prob = min(1, np.exp((p_candidate - p_current) / T))
            if np.random.uniform(0, 1) < accept_prob:
                current_key, p_current = candidate_key, p_candidate

            self.plausibility_scores.append(p_current)

            if i % 50 == 0:
                print(f"Iter: {i}, Plausibility: {p_current}")
                
            if i % 500 == 0:
                print(f"Iter {i} | Temp={T:.3f} | Accept Prob={accept_prob:.3f} | Score={p_current:.2f}")

        best_decrypted_text = self.substitute_decrypt(text, best_key)
        return best_key, best_decrypted_text, best_score
    
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
