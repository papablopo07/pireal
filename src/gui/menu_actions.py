# -*- coding: utf-8 -*-
#
# Copyright 2015 - Gabriel Acosta <acostadariogabriel@gmail.com>
#
# This file is part of Pireal.
#
# Pireal is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Pireal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pireal; If not, see <http://www.gnu.org/licenses/>.

"""
This module contains an ordered dictionary, in turn this has a dictionary
with the name and a list of items with properties as an icon , shortcut,
slot for each item in a menu, by default, strings they are in Spanish.

"""

from collections import OrderedDict
from PyQt4.QtGui import QApplication

translate = QApplication.translate


MENU = OrderedDict()


# Menu File
MENU['file'] = {
    'name': translate("PIREAL", "&Archivo"),
    'items': [{
        'name': translate("PIREAL", "Nueva Base de Datos"),
        'slot': "actions:create_data_base"
    }, {
        'name': "Nueva Consulta",
        'slot': "actions:new_query"
    }, "-", {
        'name': "Abrir",
        'slot': "actions:open_file"
    }, {
        'name': "Guardar",
        'slot': "actions:save_file"
    }, {
        'name': "Guardar como...",
        'slot': "actions:save_file_as"
    }, "-", {
        'name': "Salir",
        'slot': "pireal:close"}]}