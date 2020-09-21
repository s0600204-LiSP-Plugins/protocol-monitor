# This file is a derivation of work on - and as such shares the same
# licence as - Linux Show Player
#
# Linux Show Player:
#   Copyright 2012-2020 Francesco Ceruti <ceppofrancy@gmail.com>
#
# This file:
#   Copyright 2020 s0600204
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

# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt

from lisp.core.signal import Connection
from lisp.core.util import get_lan_ip
from lisp.plugins import get_plugin, PluginNotLoadedError
from lisp.ui.ui_utils import translate

from ..tab_page import MonitorPageWidget

class Osc(MonitorPageWidget):

    tabname = 'OSC'
    options = {
        'autoscroll': {
            'caption': translate('protocol_monitor', 'Auto scroll to show the most recently received message'),
        },
        'clearOnClose': {
            'caption': translate('protocol_monitor', 'Clear on dialog close'),
        },
        'inactiveWhenClosed': {
            'caption': translate('protocol_monitor', 'Ignore OSC events when this dialog is closed'),
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            osc_plugin = get_plugin('Osc')
        except PluginNotLoadedError:
            self._caption.setText('OSC Plugin either not Installed or Enabled')
            return

        osc_plugin.server.new_message.connect(self.on_new_osc_message, Connection.QtQueued)
        osc_plugin.Config.changed.connect(self._update_caption)
        osc_plugin.Config.updated.connect(self._update_caption)
        self._update_caption()

        try:
            qlab_mimic = get_plugin('QlabMimic')
            qlab_mimic.server.new_message.connect(self.on_new_osc_message, Connection.QtQueued)
        except PluginNotLoadedError:
            pass

    def _update_caption(self):
        self._caption.setText(
            translate(
                'osc_viewer',
                'Listening on <b>{}</b>, port <b>{}</b>'
            ).format(
                get_lan_ip(),
                get_plugin('Osc').server.in_port
            )
        )

    def on_new_osc_message(self, path, args, types, src, user_data):
        """Called when a new OSC message is recieved on the connected input."""
        if self.options['inactiveWhenClosed']['widget'].isChecked() and not self.isVisible():
            return

        message = translate(
            "OscServerDebug", '{} :: "{}" {}'
        ).format(src.get_url(), path, args)
        self._textfield.insertPlainText(message + '\n')
        if self.options['autoscroll']['widget'].isChecked():
            self._textfield.ensureCursorVisible()
