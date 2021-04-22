from setuptools import setup, find_packages

setup(
    name='opn_cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'PyYAML',
    ],
    entry_points='''
        [console_scripts]
        opn_cli=opnsense_cli.cli:cli
    ''',
)
