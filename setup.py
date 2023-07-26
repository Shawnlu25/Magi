from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'An attempt to build an autonomous agent'
LONG_DESCRIPTION = 'An attempt to build an autonomous agent'

setup(
    name="magi",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Shawn Lu",
    author_email="shawnlu25@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='llm, agi',
    classifiers= [
        'License :: OSI Approved :: MIT License',
    ]
)
