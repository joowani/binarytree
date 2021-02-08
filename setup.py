from setuptools import find_packages, setup

with open("README.md") as fp:
    description = fp.read()

setup(
    name="binarytree",
    description="Python Library for Studying Binary Trees",
    long_description=description,
    long_description_content_type="text/markdown",
    author="Joohwan Oh",
    author_email="joohwan.oh@outlook.com",
    url="https://github.com/joowani/binarytree",
    keywords=["tree", "heap", "bst", "education"],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    python_requires=">=3.6",
    license="MIT",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=[
        "graphviz",
        "setuptools>=42",
        "setuptools_scm[toml]>=3.4",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8>=3.8.4",
            "isort>=5.0.0",
            "mypy>=0.790",
            "pre-commit>=2.9.3",
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "sphinx",
            "sphinx_rtd_theme",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Education",
    ],
)
