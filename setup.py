from setuptools import setup, find_packages

requirements = [
    'numpy',
    'pandas',
    'matplotlib',
]

test_requirements = [
    'pytest',
    'pytest-mock',
]

setup(
    name='cipher_breaker',
    version='0.1',
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=requirements,
    tests_require=test_requirements,
    description='Cipher breaker: Metropolis-Hastings algorithm',
    project_urls={
        "Source": "https://github.com/kompody/cipher_breaker",
    },
)