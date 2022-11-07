# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="ptree",  # Required
    version="0.1.0",  # Required
    description="tree structure that helps url or path analysis",  # Optional
    author="Hong",  # Optional
    # This should be a valid email address corresponding to the author listed
    # above.
    author_email="hpmaatthu@gmail.com",  # Optional
    url='https://github.com/HongpengM/path_tree_python',

    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(where=".", exclude=['tests']),  # Required

    python_requires=">=3.7, <4",
)