#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
from gui_models.main_window import MainWindow
from gui_models.main_widget import Widget
from funcs.db import create_database

import sys
import pathlib

from PySide2.QtWidgets import QApplication






if __name__ == "__main__":


    DATABASE_FOLDER = pathlib.Path(__file__).parent.absolute() / "database"
    DATABASE_FOLDER.mkdir(parents=True, exist_ok=True)
    DATABASE_FOLDER = DATABASE_FOLDER / "sqlite3.db"
    create_database(DATABASE_FOLDER.resolve())

    # Qt Application
    app = QApplication([])
    app.setStyle("Fusion")

    #qp = QPalette()
    #qp.setColor(QPalette.ButtonText, QColor("black"))
    #qp.setColor(QPalette.Window, QColor(0, 0, 255, 127))
    #qp.setColor(QPalette.Button, QColor("gray"))
    #app.setPalette(qp)

    widget = Widget()
    window = MainWindow(widget)
    window.show()

    sys.exit(app.exec_())
