from setuptools import setup, find_packages

setup(
    name='MTAF',
    version='0.1.0',
    description='LISSIA end-to-end automation project',
    packages=find_packages(include=['MTAF', 'MTAF.*']),
    install_requires=[
        'atomicwrites', 'attrs', 'boto3', 'botocore', 'certifi', 'chardet', 'colorama', 'docutils', 'enum34', 'idna', 'importlib-metadata', 'jmespath', 'lxml', 'more-itertools', 'namedlist', 'openpyxl', 'packaging', 'pandas', 'pluggy', 'py', 'pyparsing', 'pytest-html', 'pytest-metadata', 'python-dateutil', 'pytz', 'requests', 's3transfer', 'selenium', 'six', 'wcwidth', 'xlrd'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
