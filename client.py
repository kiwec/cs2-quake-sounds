import datetime

from sounds import SoundEngine
from state import CS2State


class Client:
    def __init__(self, gui) -> None:
        self.gui = gui
        self.sounds = SoundEngine(self)
        self.state = CS2State(self)

    def log(self, text) -> None:
        print(text)
        self.gui.SetStatusText(text)
        self.log_to_file(text)

    def log_to_file(self, text) -> None:
        with open('log.txt', 'a', encoding='utf-8') as f:
            tms = datetime.datetime.now().strftime('%H:%M:%S')
            f.write(f"[{tms}] {text}\n")

    async def reload_sounds(self) -> None:
        """Reloads all sounds.

        Do not call outside of gui, unless you disable the update sounds button first.
        """
        await self.sounds.reload()
        self.gui.updateSoundsBtn.Enable()
        self.sounds.play("Round start")
        self.log(f"{self.sounds.nb_max_sounds} sounds loaded.")
