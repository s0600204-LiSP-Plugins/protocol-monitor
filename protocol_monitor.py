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

import logging

# pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QAction, QDialog, QTabWidget, QVBoxLayout

from lisp.core.plugin import Plugin
from lisp.ui.ui_utils import translate

from protocol_monitor import protocols

logger = logging.getLogger(__name__) # pylint: disable=invalid-name

class ProtocolMonitor(Plugin):
    """Provides the ability to see incoming MIDI/OSC messages"""

    Name = 'Protocol Events Viewer'
    Authors = ('s0600204',)
    OptDepends = ('Midi', 'Osc',)
    Description = 'Provides the ability to see incoming MIDI & OSC messages.'

    def __init__(self, app):
        super().__init__(app)

        self._dialog = None

        protocols.load()

        self._open_viewer_action = QAction(translate('protocol_viewer', 'Protocol Events Viewer'), self.app.window)
        self._open_viewer_action.triggered.connect(self._open_viewer)
        self.app.window.menuTools.addAction(self._open_viewer_action)

    def _open_viewer(self):
        if not self._dialog:
            self._dialog = ProtocolViewerDialog()
        self._dialog.open()


class ProtocolViewerDialog(QDialog):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setWindowTitle('Protocol Viewer')
        self.setMinimumSize(600, 800)

        self.setLayout(QVBoxLayout())

        self.tab_widget = QTabWidget(parent=self)
        self.tab_widget.tabBar().setDrawBase(False)

        for tab in protocols.Tabs:
            self.tab_widget.addTab(tab(parent=self.tab_widget), tab.tabname)
        self.layout().addWidget(self.tab_widget)

    def done(self, *args, **kwargs):
        super().done(*args, **kwargs)
        for idx in range(self.tab_widget.count()):
            self.tab_widget.widget(idx).on_close()

    def view(self):
        return self.tab_widget
