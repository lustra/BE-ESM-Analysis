# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui

from ResonanzFit import lang
from Module.Canvas import Canvas
from Module.Plotter import Plotter
from Module.Strings import *


class Schnitt(Canvas):
    def __init__(self, liste, fit, titel, beschriftung):
        """
        :type liste: list
        :type fit: Module.Fit.Fit
        :type titel: str
        :type beschriftung: Module.Sonstige.Achsenbeschriftung
        """
        Canvas.__init__(self, liste, fit, titel)
        vertikal = QtGui.QVBoxLayout()
        self.centralWidget().setLayout(vertikal)
        horizontal = QtGui.QHBoxLayout()
        vertikal.addLayout(horizontal)
        label = QtGui.QLabel(canvas_zeile[lang])
        sp = QtGui.QSizePolicy()
        sp.setHorizontalPolicy(sp.Maximum)
        label.setSizePolicy(sp)
        horizontal.addWidget(label)
        self.zeile = QtGui.QSpinBox()
        self.zeile.setMinimum(1)
        self.zeile.setMaximum(1)
        horizontal.addWidget(self.zeile)
        self.zeile.valueChanged.connect(self.aktualisiere)

        self.plotter = Plotter(self, beschriftung)
        vertikal.addWidget(self.plotter)

    @staticmethod
    def str_status(x, y):
        """
        :type x: int
        :type y: int
        """
        return str(int(x) + 1) + " | " + str(y)

    def set_werte(self, neu):
        """
        :type neu: Module.Ergebnis.FitWerte
        """
        self.zeile.setMaximum(self.fit.par.pixel)
        Canvas.set_werte(self, neu)

    def aktualisiere(self):
        if self._werte is not None:
            self.plotter.axes.plot(
                range(self.fit.par.pixel),
                self._werte.normal[self.zeile.value() + 1],
                antialiased=True
            )
            self.plotter.draw()
