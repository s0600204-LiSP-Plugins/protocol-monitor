# -*- coding: utf-8 -*-
#
# This file is a derivation of work on - and as such shares the same
# licence as - Linux Show Player
#
# Linux Show Player:
#   Copyright 2012-2018 Francesco Ceruti <ceppofrancy@gmail.com>
#
# This file:
#   Copyright 2019 s0600204
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

import logging

# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QDialog, QPushButton, QTextEdit, QVBoxLayout

# pylint: disable=import-error
from lisp.core.plugin import Plugin
from lisp.core.signal import Connection
from lisp.plugins import get_plugin
from lisp.plugins.midi import midi_utils
from lisp.ui.ui_utils import translate

logger = logging.getLogger(__name__) # pylint: disable=invalid-name

class MidiViewer(Plugin):
    """Provides the ability to control a pre-identified MIDI fixture"""

    Name = 'Midi Events Viewer'
    Authors = ('s0600204',)
    Depends = ('Midi',)
    Description = 'Provides the ability to see incoming MIDI message events.'

    def __init__(self, app):
        super().__init__(app)

        self._dialog = MidiViewerDialog()

        self._open_viewer_action = QAction('MIDI Events Viewer', self.app.window)
        self._open_viewer_action.triggered.connect(self._open_viewer)
        self.app.window.menuTools.addAction(self._open_viewer_action)

    def _open_viewer(self):
        self._dialog.open()


class MidiViewerDialog(QDialog):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setWindowTitle('MIDI Events Viewer')
        self.setMinimumSize(600, 800)
        self.setLayout(QVBoxLayout())

        self._textfield = QTextEdit(parent=self)
        self._textfield.setReadOnly(True)
        self.layout().addWidget(self._textfield)

        self._button_clear = QPushButton(parent=self)
        self._button_clear.setText(translate('midi_viewer', 'Clear'))
        self._button_clear.setFocusPolicy(Qt.NoFocus)
        self._button_clear.pressed.connect(self.clear_textfield)
        self.layout().addWidget(self._button_clear)

        get_plugin('Midi').input.new_message.connect(self.on_new_midi_message, Connection.QtQueued)

    def on_new_midi_message(self, message):
        """Called when a new MIDI message is recieved on the connected input."""
        msg_dict = message.dict()
        simplified_msg = midi_utils.midi_dict_to_str(msg_dict)
        self._textfield.insertPlainText(simplified_msg + '\n')

    def clear_textfield(self):
        """Called to clear the textfield."""
        self._textfield.clear()
