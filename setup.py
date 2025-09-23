from setuptools import setup, find_packages

# Read the README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="px-xtras",  # The name of your package on PyPI and for import
    version="0.1.0",   # Matches the version in your library header
    author="Alan Jones",
    author_email="your.email@example.com",  # Replace with your actual email
    description="A library of helper functions for creating advanced visualizations using Plotly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alanjones2/px-xtras2",  # Your GitHub repository URL
    packages=find_packages(),  # Automatically finds packages (e.g., 'px_xtras')
    install_requires=[
        "plotly>=5.0.0",
        "pandas>=1.0.0",
        "numpy>=1.20.0",
        "matplotlib>=3.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.7',
)