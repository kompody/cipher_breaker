import numpy as np
from cipher_breaker.metropolis_hastings import MetropolisHastings


class MetropolisHastings2D(MetropolisHastings):
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
        cooling_rate = np.exp(np.log(0.01) / iter)
        min_temperature = 0.01

        for i in range(iter):
            candidate_key = self.mutate_key_smart(current_key, decrypted_current, TM_ref)
            decrypted_candidate = self.substitute_decrypt(text, candidate_key)
            p_candidate = self.plausibility(decrypted_candidate, TM_ref)
            self.plausibility_scores.append(p_current)
            
            if p_candidate > best_score:
                best_score, best_key = p_candidate, candidate_key

            T = max(min_temperature, initial_temperature * (cooling_rate ** i))
            delta = (p_candidate - p_current) / T
            accept_prob = 1 if delta >= 0 else np.exp(delta)
            
            if np.random.uniform(0, 1) < accept_prob:
                current_key, p_current = candidate_key, p_candidate

            if i % 50 == 0:
                if i % 500 == 0:
                    print(f"Iter {i} | Score={p_current:.2f} | Temp={T:.3f} | Accept Prob={accept_prob:.3f}")
                else:
                    print(f"Iter {i} | Score={p_current:.2f}")

        best_decrypted_text = self.substitute_decrypt(text, best_key)
        return best_key, best_decrypted_text, best_score
    
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
                # Ensure both characters are in the alphabet
                idx0 = np.where(self.alphabet == bg[0])[0]
                idx1 = np.where(self.alphabet == bg[1])[0]
                if idx0.size == 0 or idx1.size == 0:
                    continue
                i = idx0[0]
                j = idx1[0]
                score = TM_ref[i, j]
                if score < worst_score:
                    worst_score = score
                    worst_bigram = (bg[0], bg[1])

            if worst_bigram:
                idx1 = np.where(np.array(key) == worst_bigram[0])[0]
                idx2 = np.where(np.array(key) == worst_bigram[1])[0]
                if idx1.size > 0 and idx2.size > 0:
                    i1 = idx1[0]
                    i2 = idx2[0]
                    key[i1], key[i2] = key[i2], key[i1]

        return "".join(key)