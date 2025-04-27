# Cipher Breaker Project

This project implements a cipher-breaking tool using the Metropolis-Hastings algorithm. It allows users to decrypt text based on a given key and transition matrix, providing insights into the plausibility of the decrypted results.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

To install the project, clone the repository and install the required dependencies:

```bash
pip install git+https://github.com/kompody/cipher_breaker.git
```

## Usage

```python
from cipher_breaker import MetropolisHastings, CipherBreakerWrapper
import tm_refs as tm

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Read the plaintext and key files
plaintext = read_text_file('text_1000_sample_1_plaintext.txt')
ciphertext = read_text_file('text_1000_sample_1_ciphertext.txt')
key = read_text_file('text_1000_sample_1_key.txt')

cipher_breaker = MetropolisHastings()

TM_ref = tm.krakatit()
```

### Using wrapper

```python
wrapper = CipherBreakerWrapper(cipher_breaker)
current_key, best_decrypted_text, p_current = (
  wrapper
    .set_text(ciphertext)
    .set_transition_matrix(TM_ref)
    .set_iterations(20_000)
    .set_start_key(key)
    .execute(is_show_plot=True)
)

print(f"Decrypted Key: {current_key}")
print(f"Decrypted Text: {best_decrypted_text}")
print(f"Plausibility Score: {p_current}")
```

### Without wrapper

```python
current_key, best_decrypted_text, p_current = cipher_breaker.prolom_substitute(ciphertext, TM_ref, 20_000, cipher_breaker.start_key)

cipher_breaker.plot_plausibility(cipher_breaker.plausibility_scores)

print(f"Decrypted Key: {current_key}")
print(f"Decrypted Text: {best_decrypted_text}")
print(f"Plausibility Score: {p_current}")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.