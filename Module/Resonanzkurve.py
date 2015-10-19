# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui
from Module.Canvas import Canvas

from ResonanzFit import lang
from Module.Strings import *


class Resonanzkurve(Canvas):
    def __init__(self, liste, fit, titel, beschriftung):
        """
        :type liste: list
        :type fit: Module.Fit.Fit
        :type titel: str
        :type beschriftung: Module.Sonstige.Achsenbeschriftung
        """
        Canvas.__init__(self, liste, titel, beschriftung)
        self.fit = fit
        hor = QtGui.QHBoxLayout()
        sp = QtGui.QSizePolicy()
        sp.setHorizontalPolicy(sp.Maximum)
        text = [canvas_zeile[lang], canvas_spalte[lang]]
        self.koord = [QtGui.QSpinBox(), QtGui.QSpinBox()]
        for k in range(2):
            label = QtGui.QLabel()
            label.setText(text[k])
            label.setSizePolicy(sp)
            hor.addWidget(label)
            self.koord[k].setMinimum(1)
            self.koord[k].setMaximum(1)
            hor.addWidget(self.koord[k])
            # noinspection PyUnresolvedReferences
            self.koord[k].valueChanged.connect(self.aktualisiere)
        self.l.addLayout(hor, 0, 0)

    @staticmethod
    def str_status(x, y):
        """
        :type x: int
        :type y: int
        """
        return str(x) + " | " + str(y)

    @property
    def werte(self):
        return self._werte

    @werte.setter
    def werte(self, neu):
        """
        :type neu: Module.Ergebnis.FitWerte
        """
        self._werte = neu
        for spin in self.koord:
            spin.setMaximum(self.fit.par.pixel)
        self.aktualisiere()

    def aktualisiere(self):
        if self.werte is not None:
            #  Nur x,y wird betrachtet, aber es sind in dieser Liste alle Messpunkte pro Ort hintereinander
            x_von = (self.koord[0].value() + 1) * self.fit.par.messpunkte
            x_bis = x_von + self.fit.par.messpunkte
            self.plotter.axes.plot(
                range(self.fit.par.pixel),
                self.werte[self.koord[1].value() + 1][x_von:x_bis],
                antialiased=True
            )
            self.plotter.draw()
