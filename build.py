import sys
from cx_Freeze import setup, Executable  # type: ignore
from typing import Dict

from version import __version__

buildOptions: Dict = dict(
    packages=["aiofiles", "wx", "wxasync"],
    excludes=["tkinter"],
    include_files=[
        "sounds",
        "gamestate_integration_cqs.cfg",
        "icon.ico",
        "config.ini",
        "bass.dll",
        "bassloud.dll",
        "bassflac.dll",
        "bassopus.dll",
    ],
    optimize=2,
    include_msvcr=True,
)

base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("main.py", base=base, icon="icon.ico")]

setup(
    name="cs2-quake-sounds",
    version=__version__,
    description="Play quake sounds via Gamestate Integration",
    options=dict(build_exe=buildOptions),
    executables=executables,
)
