from setuptools import setup, find_packages

setup(
    name="lottery-genetic",
    version="0.1.0",
    description="Algoritmo Genético para Otimização de Jogos da Loteria",
    author="Lottery Team",
    author_email="example@example.com",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "lottery=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 
