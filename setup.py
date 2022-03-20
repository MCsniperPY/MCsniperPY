import pathlib

from setuptools import setup

setup(
    name="MCsniperPY",
    version="3.4.9",
    description="Minecraft name sniper written in Python",
    long_description=(pathlib.Path(__file__).parent.resolve() / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://mcsniperpy.com",
    author="Kqzz",
    license="MIT",
    packages=["mcsniperpy", "mcsniperpy.util", "mcsniperpy.util.classes"],
    install_requires=[x.rstrip() for x in open("requirements.txt", "r")],
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
        'Documentation': 'https://docs.mcsniperpy.com',
    },
)
