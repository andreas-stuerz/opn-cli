import os
from setuptools import setup, find_packages

from opnsense_cli import __cli_name__, __version__

_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=__cli_name__,
    version=__version__,
    packages=find_packages(),
    description="OPNsense CLI written in python.",
    author='Andreas Stürz IT-Solutions',
    license='BSD-2-Clause License',
    project_urls={
        'Bug Tracker': 'https://github.com/andeman/opnsense_cli/issues',
        'CI: GitHub Actions Pipelines': 'https://github.com/andeman/opnsense_cli/actions',
        'Documentation': 'https://github.com/andeman/opnsense_cli',
        'Source Code': 'https://github.com/andeman/opnsense_cli',
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'click>=8.0.1',
        'requests',
        'PTable',
        'PyYAML',
        'jsonpath-ng',
        'beautifulsoup4',
        'lxml',
        'Jinja2'
    ],
    entry_points='''
        [console_scripts]
        opn-cli=opnsense_cli.cli:cli
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
