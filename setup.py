from setuptools import setup

setup(
    name="MCsniperPY",
    version='0.15',
    py_modules=['mcsniperpy'],
    install_requires=[
        'typer',
        'aiohttp',
        'colorama',
        'requests',
        'python-dateutil',
        'bs4'
    ],
    entry_points='''
        [console_scripts]
        mcsniperpy=mcsniperpy.cli:cli
    ''',
    python_requires='>=3.7'
)
