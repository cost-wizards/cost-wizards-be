from setuptools import find_packages, setup

setup(
    name="cost_wizards",
    version="1.0.0",
    description="Backend cost wizards",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux/WINDOWS",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyYAML>=6.0.1",
        "requests>=2.26.0",
        "loguru==0.7.2",
        "boto3==1.34.78",
        "botocore==1.34.78",
        "pandas==1.3.4",
        "pydantic-settings==2.2.1",
    ]
)
