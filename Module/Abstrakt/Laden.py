# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import time
from PyQt4 import QtCore, QtGui

from ResonanzFit import hinweis, lang, ordner
from Module import FitFunktion
from Module.Signal import signal
from Module.Sonstige import Parameter
from Module.Strings import *


class GuiAbstraktLaden(QtGui.QMainWindow):
    """ Ordnerauswahl, Einstellung der Parameter und Fit """
    def __init__(self, app):
        """
        :type app: Module.Gui.Gui
        """
        QtGui.QMainWindow.__init__(self)
        self.app = app
        self.setFixedSize(self.size())
        self.entsperrt = True

        QtCore.QObject.connect(self.app.fit, signal.importiert, self.app.importiert)
        QtCore.QObject.connect(self.app.fit, signal.fehler, self.fehler)
        QtCore.QObject.connect(self.app.fit, signal.weiter, self.weitere_zeile)
        QtCore.QObject.connect(self.app.fit, signal.fertig, self.fit_fertig)

    def set_input_enabled(self, b):
        """
        :type b: bool
        """
        raise NotImplementedError()

    def ordnerwahl(self):
        self.edit_pfad.setText(
            QtGui.QFileDialog().getExistingDirectory(self, rf_ordner[lang], ordner)
        )

    def geklickt(self):
        if self.entsperrt:
            self.start_fit()
        else:
            self.app.fit.abbruch()
            while self.app.fit.isRunning():
                time.sleep(0.01)
            self.app.raster_fit_fertig()
            self.entsperren()

    def entsperren(self):
        self.entsperrt = True
        self.set_input_enabled(True)

    def start_fit(self):
        self.set_input_enabled(False)
        self.entsperrt = False

    def fehler(self, fehler):
        """
        :type fehler: Module.Sonstige.Fehler
        """
        hinweis(self, fehler.args[0])
        self.entsperren()

    def weitere_zeile(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)

    def fit_fertig(self):
        self.app.raster_fit_fertig()
        self.close()
        self.entsperren()
        hinweis(self, laden_fertig[lang])
