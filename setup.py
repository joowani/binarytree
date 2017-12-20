from setuptools import setup, find_packages

from binarytree.version import __version__

setup(
    name='binarytree',
    description='Python Library for Learning Binary Trees',
    version=__version__,
    author='Joohwan Oh',
    author_email='joohwan.oh@outlook.com',
    url='https://github.com/joowani/binarytree',
    packages=find_packages(),
    include_package_data=True,
    tests_require=['pytest', 'flake8'],
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Education'
    ]
)
