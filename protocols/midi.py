# This file is a derivation of work on - and as such shares the same
# licence as - Linux Show Player
#
# Linux Show Player:
#   Copyright 2012-2022 Francesco Ceruti <ceppofrancy@gmail.com>
#
# This file:
#   Copyright 2022 s0600204
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

from lisp.core.signal import Connection
from lisp.plugins import get_plugin
from lisp.core.plugin import PluginNotLoadedError
from lisp.ui.ui_utils import translate

try:
    from lisp.plugins.midi import midi_utils
except ModuleNotFoundError:
    pass

from ..tab_page import MonitorPageWidget

class Midi(MonitorPageWidget):

    tabname = 'MIDI'
    options = {
        'autoscroll': {
            'caption': translate('protocol_monitor', 'Auto scroll to show the most recently received message'),
        },
        'clearOnClose': {
            'caption': translate('protocol_monitor', 'Clear on dialog close'),
        },
        'inactiveWhenClosed': {
            'caption': translate('protocol_monitor', 'Ignore MIDI events when this dialog is closed'),
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            self._midi_plugin = get_plugin('Midi')
        except PluginNotLoadedError:
            self._caption.setText('MIDI Plugin either not Installed or Enabled')
            return

        if not self._midi_plugin.is_loaded():
            self._caption.setText('MIDI Plugin is not Enabled')
            return

        self._caption.hide()

        if hasattr(self._midi_plugin, "received"):
            self._midi_plugin.received.connect(self.on_received_midi_message, Connection.QtQueued)
        else:
            self._midi_plugin.input.new_message.connect(self.on_new_midi_message, Connection.QtQueued)

    def on_received_midi_message(self, source, message):
        """Called when a new MIDI message is received on any connected inputs."""
        if self.options['inactiveWhenClosed']['widget'].isChecked() and not self.isVisible():
            return

        source_name = self._midi_plugin.input_name(source)
        simplified_msg = midi_utils.midi_dict_to_str(message.dict())
        self._textfield.insertPlainText(f"{source} :: {source_name}\n\t{simplified_msg}\n\n")

        if self.options['autoscroll']['widget'].isChecked():
            self._textfield.ensureCursorVisible()

    def on_new_midi_message(self, message):
        """Called when a new MIDI message is recieved on the connected input."""
        if self.options['inactiveWhenClosed']['widget'].isChecked() and not self.isVisible():
            return

        msg_dict = message.dict()
        simplified_msg = midi_utils.midi_dict_to_str(msg_dict)
        self._textfield.insertPlainText(simplified_msg + '\n')
        if self.options['autoscroll']['widget'].isChecked():
            self._textfield.ensureCursorVisible()
