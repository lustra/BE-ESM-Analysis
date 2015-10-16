# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui

from Module.Plotter import Plotter


class Canvas(QtGui.QMainWindow):
    def __init__(self, liste, titel, mit_fehler=True):
        QtGui.QMainWindow.__init__(self)
        liste.append(self)
        self.mit_fehler = mit_fehler
        self.setWindowTitle(titel)
        self.centralwidget = QtGui.QWidget(self)

        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.l = QtGui.QGridLayout(self.centralwidget)
        self.plotter = Plotter(self)
        self.l.addWidget(self.plotter, 1, 0)  # Darüber bleibt Platz für eventuelle Kontrollelemente
        if mit_fehler:
            self.fhlr_plotter = Plotter(self)
            self.l.addWidget(self.fhlr_plotter, 1, 1)

        self.centralwidget.setFocus()
        self.setCentralWidget(self.centralwidget)

        self._werte = None
        self._optionen = Optionen(False, False)

    @staticmethod
    def str_status(x, y):
        return str(int(x) + 1) + " | " + str(int(y) + 1)

    @property
    def werte(self):
        return self._werte

    @werte.setter
    def werte(self, neu):
        self._werte = neu
        self.aktualisiere()

    @property
    def optionen(self):
        return self._optionen

    @optionen.setter
    def optionen(self, neu):
        self._optionen = neu
        self.aktualisiere()

    def zeige(self):
        self.aktualisiere()
        self.show()
        self.raise_()

    def aktualisiere(self):
        if self.mit_fehler:
            self.plotte_mit_fehler()
        else:
            self.plotte_ohne_fehler()

    def plotte_mit_fehler(self):
        if self.werte is not None:
            if self.optionen.glaetten:
                plot = self.plotter.axes.imshow
                fhlr_plot = self.fhlr_plotter.axes.imshow
            else:
                plot = self.plotter.axes.matshow
                fhlr_plot = self.fhlr_plotter.axes.matshow

            plot(self.werte.normal, vmin=self.werte.normal_min, vmax=self.werte.normal_max)
            if self.optionen.prozentual:
                fhlr_plot(self.werte.fehler_prozent, vmin=0, vmax=100)
            else:
                fhlr_plot(self.werte.fehler, vmin=self.werte.fehler_min, vmax=self.werte.fehler_max)
            self.plotter.draw()
            self.fhlr_plotter.draw()

    def plotte_ohne_fehler(self):
        if self.werte is not None:
            if self.optionen.glaetten:
                plot = self.plotter.axes.imshow
            else:
                plot = self.plotter.axes.matshow
            plot(self.werte.normal, vmin=self.werte.normal_min, vmax=self.werte.normal_max)
            self.plotter.draw()


class Optionen:
    def __init__(self, glaetten, prozentual):
        self.glaetten = glaetten
        self.prozentual = prozentual
