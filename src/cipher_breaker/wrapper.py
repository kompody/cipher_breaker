import numpy as np
from .cipher_breakers import CipherBreaker


class CipherBreakerWrapper:
    """A wrapper class for the MetropolisHastings class that uses the builder pattern
    to set parameters and output results in a structured way.
    
    Example:
    cipher_breaker = CipherBreakerWrapper(MetropolisHastings())
    cipher_breaker.set_text("Hello, world!")
    cipher_breaker.set_transition_matrix(TM_ref)
    cipher_breaker.set_iterations(1000)
    cipher_breaker.set_start_key("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")
    cipher_breaker.save_to_file("decrypted_text.txt")
    cipher_breaker.show_result()
    cipher_breaker.show_plot()
    cipher_breaker.execute()
    """

    def __init__(self, cipher_breaker: CipherBreaker):
        self.cipher_breaker = cipher_breaker
        self.iterations = 1000
        self.text = None
        self.TM_ref = None
        self.save_file_path = None
        self.save_key_path = None
        self.is_show_result = False
        self.is_show_plot = False

    def set_iterations(self, iterations: int):
        self.iterations = iterations
        return self

    def set_start_key(self, start_key: str):
        self.cipher_breaker.start_key = start_key
        return self
    
    def generate_new_key(self):
        self.cipher_breaker.start_key = self.cipher_breaker.generate_random_key()
        return self

    def set_text(self, text: str):
        self.text = text
        return self
    
    def set_text_from_file(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return self

    def set_transition_matrix(self, TM_ref: np.ndarray):
        self.TM_ref = TM_ref
        return self
    
    def save_text_to_file(self, file_path: str):
        self.save_text_path = file_path
        return self
    
    def save_key_to_file(self, file_path: str):
        self.save_key_path = file_path
        return self
    
    def show_result(self, flag: bool = True):
        self.is_show_result = flag
        return self
    
    def show_plot(self, flag: bool = True):
        self.is_show_plot = flag
        return self

    def execute(self) -> tuple[str, str, float]:
        """Execute the Metropolis-Hastings algorithm with the provided parameters.

        Args:
            is_show_plot (bool): A flag indicating whether to display the plausibility plot.

        Returns:
            tuple[str, str, float]: A tuple containing the best key found, the decrypted text, and the plausibility score.
        """
        if self.text is None or self.TM_ref is None:
            raise ValueError("Text and transition matrix must be set before execution.")

        key, text, score = self.cipher_breaker.prolom_substitute(
            self.text, self.TM_ref, self.iterations, self.cipher_breaker.start_key
        )

        if self.save_text_path:
            try:
                with open(self.save_text_path, "w", encoding="utf-8") as file:
                    file.write(text)
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {self.save_text_path}")
            
        if self.save_key_path:
            try:
                with open(self.save_key_path, "w", encoding="utf-8") as file:
                    file.write(key)
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {self.save_key_path}")
            
        if self.is_show_result:
            print(f"Decrypted key: {key}")
            print(f"Decrypted text: {text}")
            print(f"Plausibility score: {score}")

        if self.is_show_plot:
            self.cipher_breaker.plot_plausibility(
                self.cipher_breaker.plausibility_scores
            )

        return key, text, score
