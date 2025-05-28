from setuptools import setup, find_packages

requirements = [
    'numpy',
    'matplotlib',
]

test_requirements = [
    'pytest',
    'pytest-mock',
]

setup(
    name='cipher_breaker',
    version='0.2.5',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements,
    description='Cipher breaker: Metropolis-Hastings algorithm',
    project_urls={
        "Source": "https://github.com/kompody/cipher_breaker",
    },
)