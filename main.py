"""Plays quake sounds according to CS2 Gamestate"""
import asyncio
import os
import wx  # type: ignore  # type: ignore
from pathlib import Path
from shutil import copyfile
from wxasync import WxAsyncApp  # type: ignore

# Local files
import bass
import gui
import steamfiles


def get_steam_path() -> str:
    if os.name == "nt":  # windows
        import winreg  # type: ignore

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            "SOFTWARE\\WOW6432Node\\Valve\\Steam",
            0,
            winreg.KEY_READ,
        )
        value, regtype = winreg.QueryValueEx(key, "InstallPath")
        winreg.CloseKey(key)
        return value
    else:
        return os.path.join(Path.home(), ".steam/root")


def get_cs2_path(steamapps_folder):
    # Get every SteamLibrary folder
    with open(os.path.join(steamapps_folder, "libraryfolders.vdf")) as infile:
        libraryfolders = steamfiles.load(infile)
    folders = [steamapps_folder]
    i = 1
    while True:
        try:
            steamapps = os.path.join(
                libraryfolders["LibraryFolders"][str(i)], "steamapps"
            )
            print(f"Found steamapps folder {steamapps}")
            folders.append(steamapps)
        except KeyError:
            break
        i = i + 1

    # Find the one CS2 is in
    for folder in folders:
        try:
            appmanifest = os.path.join(folder, "appmanifest_730.acf")
            print(f"Opening appmanifest {appmanifest}...")
            with open(appmanifest) as infile:
                appmanifest = steamfiles.load(infile)
                installdir = os.path.join(
                    folder, "common", appmanifest["AppState"]["installdir"]
                )
            print(f"Valid installdir found: {installdir}")
            return installdir
        except FileNotFoundError:
            continue

    print("CS2 not found :/")


async def main():
    # Ensure gamestate integration cfg is in csgo's cfg directory
    cs2_dir = get_cs2_path(os.path.join(get_steam_path(), "steamapps"))
    if cs2_dir is not None:
        copyfile(
            "gamestate_integration_cqs.cfg",
            os.path.join(cs2_dir, "game", "csgo", "cfg", "gamestate_integration_cqs.cfg"),
        )

    # Clear logs
    with open('log.txt', 'w', encoding='utf-8') as f:
        f.write('')

    if not bass.Init():
        print(f"Failed to initialize sound engine: error {bass.ErrorGetCode()}")
        return
    if not bass.PluginLoad("bassflac"):
        print(f"Failed to initialize BASSFLAC module: error {bass.ErrorGetCode()}")
    if not bass.PluginLoad("bassopus"):
        print(f"Failed to initialize BASSOPUS module: error {bass.ErrorGetCode()}")
    if not bass.PluginLoad("basswebm"):
        print(f"Failed to initialize BASSWEBM module: error {bass.ErrorGetCode()}")
    if not bass.PluginLoad("bassalac"):
        print(f"Failed to initialize BASSALAC module: error {bass.ErrorGetCode()}")

    app = WxAsyncApp()
    gui.MainFrame(
        None,
        title="CS2 Quake Sounds",
        size=wx.Size(320, 230),
        style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX),
    )
    await app.MainLoop()

    bass.Free();


if __name__ == "__main__":
    asyncio.run(main())
