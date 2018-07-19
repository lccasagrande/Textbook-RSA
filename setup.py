
import sys
from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info.major
REQUIRED_PYTHON = 3

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
        ==========================
        Unsupported Python version
        ==========================

        This project requires Python {}.{}, but you're trying to install it on Python {}.{}.
        """.format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))

    sys.exit(1)

setup(name='Textbook-RSA'
    , version=0.1
    , python_requires='>={}'.format(REQUIRED_PYTHON)
    , author='lccasagrande'
    , description=('A Textbook RSA implementation in Python')
    , packages=find_packages()
    , include_package_data=True
    , install_requires=['pyasn1','gmpy2'])