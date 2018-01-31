from setuptools import setup

setup(
    name='crisprdisco',
    version='development',
    py_modules=[
    ],
    setup_requires =[
    ],
    tests_require=[
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

