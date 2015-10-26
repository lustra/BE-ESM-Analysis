# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui

from Module.Canvas import Canvas
from Module.Plotter import Plotter
from Module.Strings import *
from ResonanzFit import lang


class Raster(Canvas):
    def __init__(self, liste, fit, resonanzkurve, titel, beschriftung):
        """
        :type liste: list
        :type fit: Module.Fit.Fit
        :type resonanzkurve: Module.Resonanzkurve.Resonanzkurve
        :type titel: str
        :type beschriftung: Module.Sonstige.Achsenbeschriftung
        """
        Canvas.__init__(self, liste, fit, titel)
        self.resonanzkurve = resonanzkurve
        vertikal = QtGui.QVBoxLayout()
        self.centralWidget().setLayout(vertikal)
        horizontal = QtGui.QHBoxLayout()
        vertikal.addLayout(horizontal)
        self.box_fehler = QtGui.QCheckBox(raster_fehler[lang])
        horizontal.addWidget(self.box_fehler)
        self.box_prozentual = QtGui.QCheckBox(raster_prozent[lang])
        horizontal.addWidget(self.box_prozentual)
        self.akt_fehler()

        self.resizeEvent = self.resize
        self.box_fehler.clicked.connect(self.akt_fehler)
        self.box_prozentual.clicked.connect(self.aktualisiere)

        self.plotter = Plotter(self, vertikal, beschriftung)
        self.plotter.mpl_connect("button_press_event", self.maus_press)

    def resize(self, event):
        """
        :type event: QtGui.QResizeEvent
        """
        # TODO
        pass

    def maus_press(self, event):
        """
        :type event: matplotlib.backend_bases.MouseEvent
        """
        self.resonanzkurve.koord[0].setValue(int(event.xdata))
        self.resonanzkurve.koord[1].setValue(int(event.ydata))
        self.resonanzkurve.zeige()

    @staticmethod
    def str_status(x, y):
        """
        :type x: int
        :type y: int
        """
        return str(int(x) + 1) + " | " + str(int(y) + 1)

    def akt_fehler(self):
        self.box_prozentual.setEnabled(self.box_fehler.isChecked())
        self.aktualisiere()

    def aktualisiere(self):
        if self.werte is not None:
            if False:  # TODO
                plot = self.plotter.axes.imshow
            else:
                plot = self.plotter.axes.matshow

            if self.box_fehler.isChecked():
                if self.box_prozentual.isChecked():
                    grafik = plot(self.werte.fehler_prozent, vmin=0, vmax=100)
                else:
                    grafik = plot(self.werte.fehler, vmin=self.werte.fehler_min, vmax=self.werte.fehler_max)
            else:
                grafik = plot(self.werte.normal, vmin=self.werte.normal_min, vmax=self.werte.normal_max, cmap='hot')

            self.plotter.draw(grafik)
