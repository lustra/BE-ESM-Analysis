# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui

from Module.Plotter import Plotter


class Canvas(QtGui.QMainWindow):
    def __init__(self, liste, fit, titel):
        """
        :type liste: list
        :type fit: Module.Fit.Fit
        :type titel: str
        """
        QtGui.QMainWindow.__init__(self)
        liste.append(self)
        self.fit = fit
        self.setWindowTitle(titel)

        self.setCentralWidget(QtGui.QWidget(self))
        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self._werte = None
        """ @type: Module.Ergebnis.FitWerte """

    def set_werte(self, neu):
        """
        :type neu: Module.Ergebnis.FitWerte
        """
        self._werte = neu
        self.aktualisiere()

    def zeige(self):
        self.aktualisiere()
        self.show()
        self.raise_()

    def aktualisiere(self):
        raise NotImplementedError()
