from setuptools import setup, find_packages

setup(
    name="harnessity",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'colorama',
        'ollama',
        'ddgs',
        'mcp'
    ],
    entry_points={
        'console_scripts': [
            'harnessity = harnessity.main:main',
        ],
    },
)
