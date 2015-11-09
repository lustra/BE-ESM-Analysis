# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
from PyQt4 import QtGui

from Module.Canvas import Canvas
from Module.Plotter import Plotter
from Module.Strings import *
from ResonanzFit import lang


class Resonanzkurve(Canvas):
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
        sp = QtGui.QSizePolicy()
        sp.setHorizontalPolicy(sp.Maximum)
        text = [canvas_zeile[lang], canvas_spalte[lang]]
        self.koord = [QtGui.QSpinBox(), QtGui.QSpinBox()]
        for k in range(2):
            label = QtGui.QLabel(text[k])
            label.setSizePolicy(sp)
            horizontal.addWidget(label)
            self.koord[k].setMinimum(1)
            self.koord[k].setMaximum(1)
            horizontal.addWidget(self.koord[k])
            self.koord[k].valueChanged.connect(self.aktualisiere)

        self.plotter = Plotter(self, vertikal, beschriftung)

    @staticmethod
    def str_status(x, y):
        """
        :type x: int
        :type y: int
        """
        return str(x) + " | " + str(y)

    def set_werte(self, neu):
        """
        :type neu: numpy.multiarray.ndarray
        """
        for spin in self.koord:
            spin.setMaximum(self.fit.par.pixel)
        self._werte = neu  # Kein super-Aufruf, weil _werte hier streng genommen einen anderen Typ hat
        self.aktualisiere()

    def aktualisiere(self):
        if self._werte is not None:
            # Nur x,y wird betrachtet, aber es sind in dieser Liste alle Messpunkte pro Ort hintereinander
            x_von = (self.koord[0].value() + 1) * self.fit.par.messpunkte
            x_bis = x_von + self.fit.par.messpunkte
            self.plotter.axes.plot(
                np.arange(  # Frequenz auf der x-Achse
                    start=self.fit.par.fmin,
                    stop=self.fit.par.fmax,
                    step=(self.fit.par.fmax - self.fit.par.fmin) / self.fit.par.messpunkte
                ),
                self._werte[self.koord[1].value() + 1][x_von:x_bis],
                antialiased=True
            )
            self.plotter.draw()