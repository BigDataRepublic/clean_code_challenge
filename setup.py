"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_namespace_packages

# The version of this tool is based on the following steps:
# https://packaging.python.org/guides/single-sourcing-package-version/
VERSION = {}

with open("src/dishwasher/__init__.py") as fp:
    # pylint: disable=W0122
    exec(fp.read(), VERSION)

setup(
    name="dishwasher",
    author="Bart Hazen",
    author_email="bart.hazen@bigdatarepublic.nl",
    url="https://bigdatarepublic.nl",
    description="Model that predicts the number of times the dishwasher has to run on a particular day at the office.",
    version=VERSION.get("__version__", "0.0.1"),
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", exclude=["tests"]),
    install_requires=["setuptools>=45.0", "coloredlogs~=15.0", "pandas==1.3.5", "scikit-learn==1.0.2"],
    entry_points={
        "console_scripts": [
            "dishwasher=dishwasher.__main__:main",
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
    ],
)
