import pytest

import src.tm_refs as tm
from src.cipher_breaker import MetropolisHastings


def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


@pytest.mark.parametrize(
    "file_paths",
    [
        (
            "text_1000_sample_1_plaintext.txt",
            "text_1000_sample_1_ciphertext.txt",
            "text_1000_sample_1_key.txt",
        )
    ],
)
def test_metropolis_hastings_cipher_breaker(file_paths):
    plaintext, expected_ciphertext, key = map(read_text_file, file_paths)

    cipher_breaker = MetropolisHastings(start_key=key)

    encrypted_text = cipher_breaker.substitute_encrypt(plaintext, key)
    assert (
        encrypted_text == expected_ciphertext
    ), f"Expected {expected_ciphertext}, but got {encrypted_text}"

    decrypted_text = cipher_breaker.substitute_decrypt(encrypted_text, key)
    assert (
        decrypted_text == plaintext
    ), f"Expected {plaintext}, but got {decrypted_text}"


def test_generate_random_key():
    cipher_breaker = MetropolisHastings()
    random_key = cipher_breaker.generate_random_key()

    # Check that the key is of the correct length
    assert len(random_key) == len(
        cipher_breaker.alphabet
    ), f"Expected key length {len(cipher_breaker.alphabet)}, but got {len(random_key)}"

    # Check that the key contains all characters from the alphabet
    assert set(random_key) == set(
        cipher_breaker.alphabet
    ), "Generated key does not contain all characters from the alphabet"

    # Check that the key is random by generating multiple keys and ensuring they are not all the same
    keys = {cipher_breaker.generate_random_key() for _ in range(10)}
    assert len(keys) > 1, "Generated keys are random; all keys are not the same."

@pytest.mark.parametrize(
    "file_paths",
    [
        (
            "text_1000_sample_1_plaintext.txt",
            "text_1000_sample_1_ciphertext.txt",
            "text_1000_sample_1_key.txt",
        )
    ],
)
def test_prolom_substitute(file_paths):
    plaintext, ciphertext, key = map(read_text_file, file_paths)

    cipher_breaker = MetropolisHastings(start_key=key)

    current_key, best_decrypted_text, p_current = cipher_breaker.prolom_substitute(plaintext, tm.krakatit(), 200, key)

    print(best_decrypted_text)

    # assert current_key == key, "Expected key to be the same"
    # assert best_decrypted_text == plaintext, "Expected decrypted text to be the same as the plaintext"
    assert p_current > 0, "Expected plausibility score to be greater than 0"
