
import numpy as np
from cipher_breakers import MetropolisHastings


class MetropolisHastingsWrapper:
    """A wrapper class for the MetropolisHastings class that uses the builder pattern
    to set parameters and output results in a structured way.
    """

    def __init__(self):
        self.start_key = None
        self.iterations = 1000
        self.text = None
        self.TM_ref = None

    def set_start_key(self, start_key: str):
        self.start_key = start_key
        return self

    def set_iterations(self, iterations: int):
        self.iterations = iterations
        return self

    def set_text(self, text: str):
        self.text = text
        return self

    def set_transition_matrix(self, TM_ref: np.ndarray):
        self.TM_ref = TM_ref
        return self

    def execute(self, is_show_plot: bool = False) -> tuple[str, str, float]:
        """Execute the Metropolis-Hastings algorithm with the provided parameters.

        Args:
            is_show_plot (bool): A flag indicating whether to display the plausibility plot.

        Returns:
            tuple[str, str, float]: A tuple containing the best key found, the decrypted text, and the plausibility score.
        """
        if self.text is None or self.TM_ref is None:
            raise ValueError("Text and transition matrix must be set before execution.")

        mh = MetropolisHastings(start_key=self.start_key)
        key, text, score = mh.prolom_substitute(self.text, self.TM_ref, self.iterations, self.start_key)
        if is_show_plot:
            mh.plot_plausibility(mh.plausibility_scores)
        return key, text, score
