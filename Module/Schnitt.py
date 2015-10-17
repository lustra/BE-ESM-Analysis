# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui

from ResonanzFit import lang
from Module.Canvas import Canvas
from Module.Strings import *


class Schnitt(Canvas):
    def __init__(self, liste, fit, titel):
        Canvas.__init__(self, liste, titel, mit_fehler=False)
        self.fit = fit
        hor = QtGui.QHBoxLayout()
        label = QtGui.QLabel()
        label.setText(canvas_zeile[lang])
        sp = QtGui.QSizePolicy()
        sp.setHorizontalPolicy(sp.Maximum)
        label.setSizePolicy(sp)
        hor.addWidget(label)
        self.zeile = QtGui.QSpinBox()
        self.zeile.setMinimum(1)
        self.zeile.setMaximum(1)
        hor.addWidget(self.zeile)
        # noinspection PyUnresolvedReferences
        self.zeile.valueChanged.connect(self.aktualisiere)
        self.l.addLayout(hor, 0, 0)

    @staticmethod
    def str_status(x, y):
        return str(int(x) + 1) + " | " + str(y)

    @property
    def werte(self):
        return self._werte

    @werte.setter
    def werte(self, neu):
        self._werte = neu
        self.zeile.setMaximum(self.fit.par.pixel)
        self.aktualisiere()

    def aktualisiere(self):
        if self.werte is not None:
            self.plotter.axes.plot(
                range(self.fit.par.pixel),
                self.werte.normal[self.zeile.value() + 1],
                antialiased=True
            )
            self.plotter.draw()
