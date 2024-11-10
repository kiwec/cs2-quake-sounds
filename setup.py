# -*- coding: utf-8 -*-
try:
    from setuptools import setup  # type: ignore
except ImportError:
    from distutils.core import setup

setup(
    name="cs2-custom-sounds",
    version="2.1.1",
    description="Play quake sounds via Gamestate Integration",
    python_requires="==3.*,>=3.7.0",
    author="kiwec",
    license="UNLICENSE",
    packages=[],
    package_dir={"": "."},
    package_data={},
    install_requires=[
        "aiofiles==0.*,>=0.4.0",
        "attrdict3==2.0.2",
        "wxasync==0.48",
    ],
)
