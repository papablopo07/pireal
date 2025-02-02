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


import os
from PyQt4.QtGui import (
    QVBoxLayout,
    QStackedWidget,
    QInputDialog,
    QFileDialog,
    QMessageBox,
    QSplitter,
)
from PyQt4.QtCore import (
    Qt,
    SIGNAL
)
from src.gui.main_window import Pireal
from src.gui import (
    start_page,
    table_widget,
    new_relation_dialog
)
from src.core import (
    settings,
    file_manager,
    logger,
    #relation
)
# FIXME: refactoring
log = logger.get_logger(__name__)
DEBUG = log.debug
ERROR = log.error


class Container(QSplitter):

    def __init__(self, orientation=Qt.Vertical):
        super(Container, self).__init__(orientation)
        self.__last_open_folder = None
        self.__filename = ""
        self.__created = False
        self.__modified = False
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        # Stacked
        self.stacked = QStackedWidget()
        vbox.addWidget(self.stacked)

        # Table
        self.table_widget = table_widget.TableWidget()

        Pireal.load_service("container", self)

    def create_data_base(self, filename=''):
        """ This function opens or creates a database

        :param filename: Database filename
        """

        if self.__created:
            QMessageBox.critical(self, self.tr("Error"),
                                 self.tr("Solo puede tener una base de datos "
                                         "abierta a la vez."))
            return
        if not filename:
            db_name, ok = QInputDialog.getText(self, self.tr("Nueva DB"),
                                               self.tr("Nombre:"))
            if not ok:
                return
        else:
            # From file
            try:
                db_name, data = file_manager.open_database(filename)
            except Exception as reason:
                QMessageBox.critical(self, self.tr("Error!"),
                                     reason.__str__())
                return

            self.table_widget.add_data_base(data)

        # Remove Start Page widget
        if isinstance(self.stacked.widget(0), start_page.StartPage):
            self.stacked.removeWidget(self.stacked.widget(0))
        self.stacked.addWidget(self.table_widget)
        # Title
        pireal = Pireal.get_service("pireal")
        pireal.change_title(db_name)
        # Enable QAction's
        pireal.enable_disable_db_actions()
        self.__created = True

    def create_new_relation(self):
        dialog = new_relation_dialog.NewRelationDialog(self)
        dialog.show()

    def remove_relation(self):
        lateral = Pireal.get_service("lateral")
        rname = lateral.get_relation_name()
        if not rname:
            QMessageBox.critical(self, self.tr("Error"),
                                 self.tr("No se ha seleccionado ninguna "
                                         "relación."))
            return
        r = QMessageBox.question(self, self.tr("Confirmación"),
                                 self.tr("Seguro que quieres eliminar la "
                                         "relación <b>{}</b>").format(rname),
                                             QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.No:
            return
        index = lateral.current_index()
        # Remove table
        self.table_widget.remove_table(index)
        # Remove item from list widget
        lateral.remove_item(index)

    def new_query(self, filename=''):
        query_widget = Pireal.get_service("query_widget")
        self.addWidget(query_widget)
        if not query_widget.isVisible():
            query_widget.show()
        pireal = Pireal.get_service("pireal")
        pireal.enable_disable_query_actions()
        query_widget.new_query(filename)

        self.connect(query_widget,
                     SIGNAL("currentEditorSaved(QPlainTextEdit)"),
                     self.save_query)

    @property
    def modified(self):
        return self.__modified

    def show_start_page(self):
        sp = start_page.StartPage()
        self.stacked.addWidget(sp)

    def close_db(self):
        """ Close data base """

        widget = self.stacked.currentWidget()
        if isinstance(widget, table_widget.TableWidget):
            # Clear list of relations
            lateral = Pireal.get_service("lateral")
            lateral.clear_items()
            lateral.hide()
            # Close table widget
            self.stacked.removeWidget(widget)
            # Add start page
            self.show_start_page()

            self.__created = False

    def save_query(self, weditor=None):
        if weditor is None:
            query_widget = Pireal.get_service("query_widget")
            # Editor instance
            weditor = query_widget.get_active_editor()
        if weditor.rfile.is_new:
            return self.save_query_as(weditor)
        content = weditor.toPlainText()
        weditor.rfile.write(content)
        weditor.document().setModified(False)

        self.emit(SIGNAL("currentFileSaved(QString)"),
                  self.tr("Archivo guardado: {}").format(weditor.filename))

    def open_file(self):

        if self.__last_open_folder is None:
            directory = os.path.expanduser("~")
        else:
            directory = self.__last_open_folder
        filename = QFileDialog.getOpenFileName(self, self.tr("Abrir Archivo"),
                                               directory, settings.DBFILE,
                                               QFileDialog.DontUseNativeDialog)
        if not filename:
            return
        # Save folder
        self.__last_open_folder = file_manager.get_path(filename)

        ext = file_manager.get_extension(filename)
        if ext == '.pqf':
            # Query file
            self.new_query(filename)
        elif ext == '.rdb':
            self.load_rdb_database(file_manager.read_rdb_file(filename))
        else:
            self.create_data_base(filename)

    def load_rdb_database(self, content):
        csv_content = ""
        for line in content.splitlines():
            if line.startswith('@'):
                csv_content += '@'
                portion = line.split('(')
                name = portion[0][1:]
                csv_content += name + ':'
                for i in portion[1].split(','):
                    if not i.startswith(' '):
                        field = i.split('/')[0].strip()
                        csv_content += field + ','
            else:
                if not line:
                    continue
                csv_content += line
            csv_content += '\n'

        self.table_widget.add_table_from_rdb_content(csv_content)

    def save_query_as(self, editor=None):
        if editor is None:
            query_widget = Pireal.get_service("query_widget")
            editor = query_widget.get_active_editor()
        directory = os.path.expanduser("~")
        filename = QFileDialog.getSaveFileName(self,
                                               self.tr("Guardar Archivo"),
                                               directory)
        if not filename:
            return
        content = editor.toPlainText()
        editor.rfile.write(content, filename)
        editor.document().setModified(False)

    def load_relation(self, filenames=[]):
        """ Load relation from file """

        if not filenames:
            native_dialog = QFileDialog.DontUseNativeDialog
            if self.__last_open_folder is None:
                directory = os.path.expanduser("~")
            else:
                directory = self.__last_open_folder
            ffilter = settings.RFILES.split(';;')[-1]
            filenames = QFileDialog.getOpenFileNames(self,
                                                     self.tr("Abrir Archivo"),
                                                     directory, ffilter,
                                                     native_dialog)
            if not filenames:
                return
            # Save folder
            self.__last_open_folder = file_manager.get_path(filenames[0])
            self.__modified = True

        # Load tables
        self.table_widget.load_relation(filenames)

    def execute_queries(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.execute_queries()

    def undo_action(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.undo()

    def redo_action(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.redo()

    def cut_action(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.cut()

    def copy_action(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.copy()

    def paste_action(self):
        query_widget = Pireal.get_service("query_widget")
        query_widget.paste()

    def check_opened_query_files(self):
        query_widget = Pireal.get_service("query_widget")
        return query_widget.opened_files()


container = Container()
