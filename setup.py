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
        'pandas==0.22.0',
        'numpy==1.14.0',
        'biopython==1.70',
        'click==6.7'
    ],
    entry_points='''
        [console_scripts]
        disco=crisprdisco.cli.script:disco
    ''',
)

