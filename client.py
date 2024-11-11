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

    async def reload_sounds(self) -> None:
        """Reloads all sounds.

        Do not call outside of gui, unless you disable the update sounds button first.
        """
        await self.sounds.reload()
        self.gui.updateSoundsBtn.Enable()
        self.sounds.play("Round start")
        self.log(f"{self.sounds.nb_max_sounds} sounds loaded.")
