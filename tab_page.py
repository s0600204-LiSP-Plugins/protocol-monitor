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

# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QCheckBox, QFormLayout, QGroupBox, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from lisp.plugins import get_plugin
from lisp.ui.ui_utils import translate

class MonitorPageWidget(QWidget):

    tabname = '-'
    options = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setLayout(QVBoxLayout())

        self._caption = QLabel(parent=self)
        self._caption.setAlignment(Qt.AlignHCenter)
        self.layout().addWidget(self._caption)

        self._textfield = QTextEdit(parent=self)
        self._textfield.setReadOnly(True)
        self._textfield.setTabStopWidth(
            QFontMetrics(self._textfield.currentFont()).horizontalAdvance(" ") * 8)
        self.layout().addWidget(self._textfield)

        self._button_clear = QPushButton(parent=self)
        self._button_clear.setText(translate('protocol_monitor', 'Clear'))
        self._button_clear.setFocusPolicy(Qt.NoFocus)
        self._button_clear.pressed.connect(self.clear_textfield)
        self.layout().addWidget(self._button_clear)

        self._groupbox = QGroupBox(parent=self)
        self._groupbox.setTitle(translate('protocol_monitor', 'Options'))
        self._groupbox.setFocusPolicy(Qt.NoFocus)
        self._groupbox.setLayout(QFormLayout())

        protocol = self.__module__.split('.')[-1]
        for key, option in self.options.items():
            option['widget'] = QCheckBox(parent=self._groupbox)
            option['widget'].setFocusPolicy(Qt.NoFocus)
            option['widget'].setText(option['caption'])
            option['widget'].setChecked(get_plugin('ProtocolMonitor').Config.get('.'.join([protocol, key])))
            option['widget'].toggled.connect(self._update_option)
            self._groupbox.layout().addWidget(option['widget'])
        self.layout().addWidget(self._groupbox)

    def on_close(self):
        if self.options['clearOnClose']['widget'].isChecked():
            self.clear_textfield()

    def _update_option(self, isChecked):
        protocol = self.__module__.split('.')[-1]
        config = get_plugin('ProtocolMonitor').Config
        for key, option in self.options.items():
            if option['widget'] is not self.sender():
                continue
            config.set('.'.join([protocol, key]), isChecked)
            config.write()
            return

    def clear_textfield(self):
        """Called to clear the textfield."""
        self._textfield.clear()
