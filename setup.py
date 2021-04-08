from setuptools import setup

setup(
    name='opn_cli',
    version='1.0',
    py_modules=['opn_cli'],
    install_requires=[
        'click',
        'requests',
        'PyYAML'
    ],
    entry_points='''
        [console_scripts]
        opn_cli=opn_cli:cli
    ''',
)
