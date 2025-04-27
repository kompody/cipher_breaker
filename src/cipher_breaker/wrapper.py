import numpy as np
import concurrent.futures
from .cipher_breakers import CipherBreaker

class CipherBreakerWrapper:
    """A wrapper class for the MetropolisHastings class that uses the builder pattern
    to set parameters and output results in a structured way.
    """

    def __init__(self, cipher_breaker: CipherBreaker):
        self.cipher_breaker = cipher_breaker
        self.iterations = 1000
        self.text = None
        self.TM_ref = None

    def set_iterations(self, iterations: int):
        self.iterations = iterations
        return self
    
    def set_start_key(self, start_key: str):
        self.cipher_breaker.start_key = start_key
        return self

    def set_text(self, text: str):
        self.text = text
        return self

    def set_transition_matrix(self, TM_ref: np.ndarray):
        self.TM_ref = TM_ref
        return self

    def execute(self, threads: int = 1, is_show_plot: bool = False) -> tuple[str, str, float]:
        """Execute the Metropolis-Hastings algorithm with the provided parameters.

        Args:
            threads (int): The number of threads to use for parallel execution of the Metropolis-Hastings algorithm.
            is_show_plot (bool): A flag indicating whether to display the plausibility plot.

        Returns:
            tuple[str, str, float]: A tuple containing the best key found, the decrypted text, and the plausibility score.
        """
        
        if threads == 1:
            return self.execute_single_thread(is_show_plot)
        
        if self.text is None or self.TM_ref is None:
            raise ValueError("Text and transition matrix must be set before execution.")
        
        if threads < 1:
            raise ValueError("Threads must be greater than 0.")

        divided_iterations = self.iterations // threads
        futures = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                futures.append(executor.submit(
                    self.cipher_breaker.prolom_substitute,
                    self.text,
                    self.TM_ref,
                    divided_iterations,
                    self.cipher_breaker.start_key
                ))

            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        # Combine results to find the best key and score
        best_key, best_text, best_score = max(results, key=lambda x: x[2])

        if is_show_plot:
            self.cipher_breaker.plot_plausibility(self.cipher_breaker.plausibility_scores)
        return best_key, best_text, best_score

    def execute_single_thread(self, is_show_plot: bool = False) -> tuple[str, str, float]:
        """Execute the Metropolis-Hastings algorithm with the provided parameters.

        Args:
            is_show_plot (bool): A flag indicating whether to display the plausibility plot.

        Returns:
            tuple[str, str, float]: A tuple containing the best key found, the decrypted text, and the plausibility score.
        """
        if self.text is None or self.TM_ref is None:
            raise ValueError("Text and transition matrix must be set before execution.")

        key, text, score = self.cipher_breaker.prolom_substitute(self.text, self.TM_ref, self.iterations, self.cipher_breaker.start_key)
        if is_show_plot:
            self.cipher_breaker.plot_plausibility(self.cipher_breaker.plausibility_scores)
        return key, text, score
