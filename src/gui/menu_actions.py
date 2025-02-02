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
        'slot': "container:create_data_base"
    }, {
        'name': translate("PIREAL", "Nueva Consulta"),
        'slot': "container:new_query"
    }, "-", {
        'name': translate("PIREAL", "Abrir"),
        'slot': "container:open_file"
    }, {
        'name': translate("PIREAL", "Guardar"),
        'slot': "container:save_query"
    }, {
        'name': translate("PIREAL", "Guardar como..."),
        'slot': "container:save_query_as"
    }, "-", {
        'name': translate("PIREAL", "Cerrar"),
        'slot': "container:close_db"
    }, "-", {
        'name': translate("PIREAL", "Salir"),
        'slot': "pireal:close"}]}


# Menu Edit
MENU['edit'] = {
    'name': translate("PIREAL", "&Editar"),
    'items': [{
        'name': translate("PIREAL", "Deshacer"),
        'slot': "container:undo_action"
    }, {
        'name': translate("PIREAL", "Rehacer"),
        'slot': "container:redo_action"
    }, "-", {
        'name': translate("PIREAL", "Cortar"),
        'slot': "container:cut_action"
    }, {
        'name': translate("PIREAL", "Copiar"),
        'slot': "container:copy_action"
    }, {
        'name': translate("PIREAL", "Pegar"),
        'slot': "container:paste_action"
    }, "-", {
        'name': translate("PIREAL", "Preferencias"),
        'slot': 'container:preferences'}]}


# Menu Relation
MENU['relation'] = {
    'name': translate("PIREAL", "&Relación"),
    'items': [{
        'name': translate("PIREAL", "Nueva Relación"),
        'slot': "container:create_new_relation"
    }, {
        'name': translate("PIREAL", "Eliminar Relación"),
        'slot': "container:remove_relation"
    }, {
        'name': translate("PIREAL", "Cargar Relación"),
        'slot': "container:load_relation"
    }, "-", {
        'name': translate("PIREAL", "Agregar Registro"),
        'slot': "container:insert_tuple"
    }, {
        'name': translate("PIREAL", "Eliminar Registro"),
        'slot': "container:remove_tuple",
    }, "-", {
        'name': translate("PIREAL", "Ejecutar Consultas"),
        'slot': "container:execute_queries"}]}


# Menu Help
MENU['help'] = {
    'name': translate("PIREAL", "A&yuda"),
    'items': [{
        'name': translate("PIREAL", "Acerca de Pireal"),
        'slot': "pireal:about_pireal"
    }, {
        'name': translate("PIREAL", "Acerca de Qt"),
        'slot': "pireal:about_qt"}]}
