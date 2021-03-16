from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name="MCsniperPY",
    version='0.18.1',
    description='Minecraft name sniper written in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/MCsniperPY/MCsniperPY',
    author='Kqzz',
    license='MIT',
    packages=['mcsniperpy', 'mcsniperpy.util', 'mcsniperpy.util.classes'],
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
