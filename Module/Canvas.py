# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui

from Module.Plotter import Plotter


class Canvas(QtGui.QMainWindow):
    def __init__(self, liste, titel, beschriftung, mit_fehler=False):
        """
        :type liste: list
        :type titel: str
        :type beschriftung: Module.Sonstige.Achsenbeschriftung
        """
        QtGui.QMainWindow.__init__(self)
        liste.append(self)
        self.mit_fehler = mit_fehler
        self.setWindowTitle(titel)
        self.centralwidget = QtGui.QWidget(self)

        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.l = QtGui.QGridLayout(self.centralwidget)
        self.plotter = Plotter(self, beschriftung)
        self.l.addWidget(self.plotter, 1, 0)  # Darüber bleibt Platz für eventuelle Kontrollelemente
        if self.mit_fehler:  # TODO Fehler nur optional anzeigen
            self.fhlr_plotter = Plotter(self, beschriftung)
            self.l.addWidget(self.fhlr_plotter, 1, 1)

        self.centralwidget.setFocus()
        self.setCentralWidget(self.centralwidget)

        self._werte = None
        self._optionen = Optionen(False, False)

    @staticmethod
    def str_status(x, y):
        """
        :type x: int
        :type y: int
        """
        return str(int(x) + 1) + " | " + str(int(y) + 1)

    @property
    def werte(self):
        return self._werte

    @werte.setter
    def werte(self, neu):
        """
        :type neu: Module.Ergebnis.FitWerte
        """
        self._werte = neu
        self.aktualisiere()

    @property
    def optionen(self):
        return self._optionen

    @optionen.setter
    def optionen(self, neu):
        """
        :type neu: Module.Canvas.Optionen
        """
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

    def plotte_mit_fehler(self):  # TODO das ist noch nicht objektorientiert genug
        if self.werte is not None:
            if self.optionen.glaetten:
                plot = self.plotter.axes.imshow
                fhlr_plot = self.fhlr_plotter.axes.imshow
            else:
                plot = self.plotter.axes.matshow
                fhlr_plot = self.fhlr_plotter.axes.matshow

            grafik = plot(self.werte.normal, vmin=self.werte.normal_min, vmax=self.werte.normal_max)
            if self.optionen.prozentual:
                fhlr_grafik = fhlr_plot(self.werte.fehler_prozent, vmin=0, vmax=100)
            else:
                fhlr_grafik = fhlr_plot(self.werte.fehler, vmin=self.werte.fehler_min, vmax=self.werte.fehler_max)
            self.plotter.draw(grafik)  # TODO Dopplungen hier und insgesamt der unteren Fkt. zu ähnlich
            self.fhlr_plotter.draw(fhlr_grafik)

    def plotte_ohne_fehler(self):
        if self.werte is not None:
            if self.optionen.glaetten:
                plot = self.plotter.axes.imshow
            else:
                plot = self.plotter.axes.matshow
            grafik = plot(self.werte.normal, vmin=self.werte.normal_min, vmax=self.werte.normal_max)
            self.plotter.draw(grafik)


class Optionen:
    def __init__(self, glaetten, prozentual):
        """
        :type glaetten: bool
        :type prozentual: bool
        """
        self.glaetten = glaetten
        self.prozentual = prozentual
