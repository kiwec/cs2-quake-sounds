# cs2-quake-sounds

Custom sounds in your CS2 matches.

### FAQ

* Does it work in matchmaking? In premier? On faceit?

Yes.

* Will I get banned for using this?

No. This is using [Game State Integration](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration), which is allowed by Valve.

* How do I add my own sounds?

Drop your sounds in the corresponding `sounds` folder. Feel free to remove the ones you don't like, too.

Please keep in mind that only OPUS files are supported.

### Running

You probably want to use the installer.

However, if you want to try the latest version, execute these commands :

* `git clone https://git.kiwec.net/kiwec/cs2-quake-sounds.git && cd cs2-quake-sounds`

* `pip install cython numpy Pillow requests six` # wxasync build bullshit

* `python setup.py install --user`

Then, run it :

* `python main.py`

### Building

Run the following commands :

* `python setup.py install --user`

* `pip install cx_Freeze`

* Run `python build.py build`
