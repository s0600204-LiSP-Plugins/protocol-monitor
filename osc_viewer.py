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
from PyQt5.QtWidgets import QAction, QCheckBox, QDialog, QFormLayout, QGroupBox, QLabel, QPushButton, QTextEdit, QVBoxLayout

# pylint: disable=import-error
from lisp.core.plugin import Plugin
from lisp.core.signal import Connection
from lisp.core.util import get_lan_ip
from lisp.plugins import get_plugin
from lisp.ui.ui_utils import translate

logger = logging.getLogger(__name__) # pylint: disable=invalid-name

class OscViewer(Plugin):
    """Provides the ability to see incoming OSC messages"""

    Name = 'OSC Events Viewer'
    Authors = ('s0600204',)
    Depends = ('Osc',)
    Description = 'Provides the ability to see incoming OSC messages.'

    def __init__(self, app):
        super().__init__(app)

        self._dialog = None

        self._open_viewer_action = QAction('OSC Events Viewer', self.app.window)
        self._open_viewer_action.triggered.connect(self._open_viewer)
        self.app.window.menuTools.addAction(self._open_viewer_action)

    def _open_viewer(self):
        if not self._dialog:
            self._dialog = OscViewerDialog()
        self._dialog.open()


class OscViewerDialog(QDialog):

    options = {
        'autoscroll': {
            'caption': translate('osc_viewer', 'Auto scroll to show most recently received message'),
        },
        'clearOnClose': {
            'caption': translate('osc_viewer', 'Clear on dialog close'),
        },
        'inactiveWhenClosed': {
            'caption': translate('osc_viewer', 'Ignore OSC events when this dialog is closed'),
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setWindowTitle('OSC Events Viewer')
        self.setMinimumSize(600, 800)
        self.setLayout(QVBoxLayout())

        self._caption = QLabel(parent=self)
        self._caption.setAlignment(Qt.AlignHCenter)
        self.layout().addWidget(self._caption)

        self._textfield = QTextEdit(parent=self)
        self._textfield.setReadOnly(True)
        self.layout().addWidget(self._textfield)

        self._button_clear = QPushButton(parent=self)
        self._button_clear.setText(translate('osc_viewer', 'Clear'))
        self._button_clear.setFocusPolicy(Qt.NoFocus)
        self._button_clear.pressed.connect(self.clear_textfield)
        self.layout().addWidget(self._button_clear)

        self._groupbox = QGroupBox(parent=self)
        self._groupbox.setTitle(translate('osc_viewer', 'Options'))
        self._groupbox.setFocusPolicy(Qt.NoFocus)
        self._groupbox.setLayout(QFormLayout())

        for key, option in self.options.items():
            option['widget'] = QCheckBox(parent=self._groupbox)
            option['widget'].setFocusPolicy(Qt.NoFocus)
            option['widget'].setText(option['caption'])
            option['widget'].setChecked(get_plugin('OscViewer').Config.get(key))
            option['widget'].toggled.connect(self._update_option)
            self._groupbox.layout().addWidget(option['widget'])

        self.layout().addWidget(self._groupbox)

        osc_plugin = get_plugin('Osc')
        osc_plugin.server.new_message.connect(self.on_new_osc_message, Connection.QtQueued)
        osc_plugin.Config.changed.connect(self._update_caption)
        osc_plugin.Config.updated.connect(self._update_caption)
        self._update_caption()

    # pylint: disable=invalid-name
    def closeEvent(self, _):
        if self.options['clearOnClose']['widget'].isChecked():
            self.clear_textfield()

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

    def _update_option(self, isChecked):
        config = get_plugin('OscViewer').Config
        for key, option in self.options.items():
            if option['widget'] is not self.sender():
                continue
            config.set(key, isChecked)
            config.write()
            return

    def on_new_osc_message(self, path, args, types, src, user_data):
        """Called when a new OSC message is recieved on the connected input."""
        if self.options['inactiveWhenClosed']['widget'].isChecked() and not self.isVisible():
            return

        message = translate(
            "OscServerDebug", 'Message from {} -> path: "{}" args: {}'
        ).format(src.get_url(), path, args)
        self._textfield.insertPlainText(message + '\n')
        if self.options['autoscroll']['widget'].isChecked():
            self._textfield.ensureCursorVisible()

    def clear_textfield(self):
        """Called to clear the textfield."""
        self._textfield.clear()
