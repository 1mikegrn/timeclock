from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='timeclock',
    version='0.1.0',
    description='CLI tool for logging productivity',
    author = 'Michael Green',
    author_email = '1mikegrn@gmail.com',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],

    packages=find_packages(),

    include_package_data=True,

    python_requires='>=3.6',

    install_requires=[
        'pandas >= 1.0.1'
    ],

    entry_points={
        'console_scripts': ['clk=timeclock.app:main']
    },

    project_urls={
        'Webpage': 'https://1mikegrn.github.io/pages/timeclock/',
        'Github': 'https://github.com/1mikegrn/timeclock/',
        'Personal Webpage': 'https://1mikegrn.github.io/',
    }
)