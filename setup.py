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
    python_requires=">=3.7",
    license="MIT",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=[
        "graphviz",
        "setuptools>=60.8.2",
        "setuptools_scm[toml]>=5.0.1",
    ],
    extras_require={
        "dev": [
            "black>=22.1.0",
            "flake8>=4.0.1",
            "isort>=5.10.1",
            "mypy>=0.931",
            "pre-commit>=2.17.0",
            "pytest>=6.2.1",
            "pytest-cov>=2.10.1",
            "sphinx",
            "sphinx_rtd_theme",
            "types-setuptools",
            "types-dataclasses",
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
