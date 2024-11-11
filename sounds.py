"""Related to sounds"""
import asyncio
import os
import random
import wx  # type: ignore
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Dict, List
from wxasync import StartCoroutine  # type: ignore

import bass
import config


class Sound:
    filename: str
    handle: int
    is_stream: bool


class SoundEngine:
    """Loads and plays sounds"""

    def __init__(self, client) -> None:
        self.playerid = None
        self.client = client
        self.lock = Lock()
        self.nb_max_sounds = 0
        self.music = None

        # Dict[category:List[sound_data]]
        self.loaded_sounds: Dict[str, List[Buffer]] = defaultdict(list)

        self.volume: int = config.config["Sounds"].getint("Volume", 50)  # type: ignore

    def max_sounds(self) -> int:
        """Returns the number of sounds that will be loaded."""
        max = 0
        for path in os.listdir("sounds"):
            for file in os.listdir(os.path.join("sounds", path)):
                if file.startswith(".git") or file == "desktop.ini":
                    continue
                max = max + 1
        return max

    def load(self, category: str, filepath: str) -> None:
        sound = Sound()
        sound.filename = filepath

        if category in ("MVP", "Round lose", "Round start", "Round win", "Timeout"):
            sound.handle = bass.StreamCreateFile(False, filepath)
            sound.is_stream = True
        else:
            sound.handle = bass.SampleLoad(False, filepath)
            sound.is_stream = False

        if sound.handle is None:
            self.client.log(f"Failed to load '{filepath}': error {bass.ErrorGetCode()}")
            return

        with self.lock:
            self.loaded_sounds[category].append(sound)
            wx.CallAfter(
                self.client.gui.SetStatusText,
                f"Loading sounds... ({len(self.loaded_sounds)}/{self.nb_max_sounds})",
            )

    async def reload(self) -> None:
        """Reloads the list of available sounds.

        The async logic is a bit complicated here, but it boils down to the following :
        - No more than 1 sound will be loaded at the same time
        - Every sound is getting loaded in a separate thread, so the GUI is not blocked
        - We're not waiting using the executor but by waiting for all tasks to end,
        so the operation stays asynchronous
        """
        with self.lock:
            for category in self.loaded_sounds:
                for sound in self.loaded_sounds[category]:
                    if sound.is_stream:
                        bass.StreamFree(sound.handle)
                    else:
                        bass.SampleFree(sound.handle)

            self.loaded_sounds = defaultdict(list)
            self.nb_max_sounds = self.max_sounds()

        executor = ThreadPoolExecutor(max_workers=1)
        loop = asyncio.get_running_loop()
        tasks: List = []
        for category in os.listdir("sounds"):
            for file in os.listdir(os.path.join("sounds", category)):
                if file.startswith(".git") or file == "desktop.ini":
                    continue

                filepath = os.path.join("sounds", category, file)
                tasks.append(
                    loop.run_in_executor(executor, self.load, category, filepath)
                )
        executor.shutdown(wait=False)
        await asyncio.gather(*tasks)

    def stop(self) -> None:
        with self.lock:
            if self.music is not None:
                bass.ChannelStop(self.music)
                self.music = None

    def play(self, sound_name: str) -> bool:
        """Tries playing a sound by its name.

        Returns True if the sound was played successfully.
        """
        with self.lock:
            if len(self.loaded_sounds[sound_name]) > 0:
                sound = random.choice(self.loaded_sounds[sound_name])

                if sound.is_stream:
                    channel = sound.handle
                    self.music = sound.handle
                else:
                    channel = bass.SampleGetChannel(sound.handle)

                # gain can be between 0.0 and 2.0 with the GUI's volume slider
                gain: float = 0.0 if self.volume == 0 else self.volume / 50.0
                if not bass.ChannelSetVolume(channel, gain):
                    self.client.log(f"Failed to set volume of '{sound.filename}': error {bass.ErrorGetCode()}")
                    return False

                if not bass.ChannelPlay(channel):
                    self.client.log(f"Failed to play '{sound.filename}': error {bass.ErrorGetCode()}")
                    return False

                self.client.log(f"Played '{sound.filename}'.")
                return True
            else:
                self.client.log(f"[!] No sound found for '{sound_name}'.")
                return False
