from setuptools import setup, find_packages
from distutils.core import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Rigol_ds1000z',
    version='0.3.0',
    author="Jeremiah Heilman (@jaheilman)",
    author_email="jeremiah.heilman@gmail.com",
    description="Python based library to control Rigol DS1000z series oscilloscopes using VISA (USB and Ethernet).",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/jaheilman/Rigol_ds1000z",
    # packages=['rigol_ds1000z'],
    packages=find_packages(),
    install_requires=['pyvisa', 'numpy', 'strenum'],

    keywords=['python', 'Rigol', 'oscilloscope'],
    classifiers= [
        "Development Status :: beta",
        "Intended Audience :: Test Engineering",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Linux",
    ]
)
