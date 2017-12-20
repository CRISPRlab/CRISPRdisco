from setuptools import setup

setup(
    name='crisprdisco',
    version='development',
    py_modules=[
    ],
    setup_requires =[
        "pytest-runner",
    ],
    tests_require=[
        "pytest==3.0.4",
    ],
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'biopython',
        'click',
        'regex',
    ],
    entry_points='''
        [console_scripts]
        disco=crisprdisco.cli.script:disco
    ''',
)

