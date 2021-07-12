import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

install_requires = [line.strip() for line in open("requirements.txt").readlines()]

setup(
    name="MCsniperPY",
    version="3.4.3",
    description="Minecraft name sniper written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mcsniperpy.com",
    author="Kqzz",
    license="MIT",
    packages=["mcsniperpy", "mcsniperpy.util", "mcsniperpy.util.classes"],
    install_requires=install_requires,
    entry_points={"console_scripts": ["mcsniperpy=mcsniperpy.cli:cli"]},
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    project_urls={
        'GitHub': 'https://github.com/MCsniperPY/MCsniperPY',
        'Documentation': 'https://docs.mcsniperpy.com'
    }
)
