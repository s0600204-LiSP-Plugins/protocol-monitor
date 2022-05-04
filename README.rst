
Protocol Monitor
================

The **Protocol Monitor** is a community-created plugin for `Linux Show Player`_.

This plugin adds a tabbed non-modal dialog window in which incoming MIDI and OSC
messages are listed as they arrive. This window may be opened via the "Tools"
menu.

The tab displaying OSC messages also conveniently shows the exact ip and port
*Linux Show Player* is currently listening for OSC messages on.

This plugin is most useful during the setup or debugging of system integration:

a. checking that *Linux Show Player* is receiving something, and
b. showing exactly what's being received.


Dependencies
------------

This plugin has no dependencies other than *Linux Show Player* ``v0.6``.


Installation
------------

To use, navigate to ``$XDG_DATA_HOME/LinuxShowPlayer/$LiSP_Version/plugins/``
(on most Linux systems ``$XDG_DATA_HOME`` is ``~/.local/share``), and create a
subfolder named ``protocol_monitor``.

Place the files comprising this plugin into this new folder.

When you next start *Linux Show Player*, the program should load this plugin
automatically.


.. _Linux Show Player: https://github.com/FrancescoCeruti/linux-show-player
