# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import sys
from PyQt4 import QtGui

from Module.Strings import *

lang = de
ordner = "~/Dokumente"


def hinweis(ursprung, nachricht):
    anzeige = QtGui.QMessageBox(ursprung)
    anzeige.setText(nachricht)
    anzeige.exec_()


if __name__ == '__main__':
    if 'debug_schnell' in sys.argv:
        from Module.Abstrakt.Fit import Fit
        Fit.debug_schnell = True

    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('Design/Raster.png'))
    from Module.Gui import Gui
    gui = Gui()
    gui.show()
    sys.exit(app.exec_())
