"""
@author: Valon Lushta
@authos: Sebastian Badur
"""
# coding=utf-8
import sys
from PyQt4 import QtGui

from Module.Strings import *


lang = de
ordner = "/ESM/06-11-14-gxsmneu21/"


def hinweis(nachricht):
    anzeige = QtGui.QMessageBox()
    anzeige.setText(nachricht)
    anzeige.exec_()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    from Module.Gui import Gui
    gui = Gui()
    gui.show()
    sys.exit(app.exec_())
