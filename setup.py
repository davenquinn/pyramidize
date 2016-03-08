from setuptools import setup

setup(
    name='pyramidize',
    version='0.1',
    py_modules=['pyramidize'],
    install_requires=[
        'click',
        'sqlalchemy',
        'psycopg2'],
    entry_points='''
        [console_scripts]
        pyramidize=pyramidize:cli
    ''')
