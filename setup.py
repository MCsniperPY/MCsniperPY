from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="MCsniperPY",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.15.2',
    py_modules=['mcsniperpy'],
    license='MIT',
    author='Kqzz',
    url='https://github.com/MCsniperPY/MCsniperPY',
    install_requires=[
        'typer',
        'aiohttp',
        'colorama',
        'bs4'
    ],
    entry_points={
        'console_scripts': ['mcsniperpy=mcsniperpy.cli:cli']
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
