# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import sys
from PyQt4 import QtGui

from Module.Canvas import Canvas
from Module.Plotter import Plotter
from Module.Strings import *
from ResonanzFit import lang


def genauigkeit(box):
    """
    :type box: QtGui.QDoubleSpinBox
    """
    box.setSingleStep(0.00001)
    box.setDecimals(10)
    box.setMaximum(2000000)
    box.setMinimum(-2000000)


class Raster(Canvas):
    def __init__(self, gui, resonanzkurve, titel, beschriftung):
        """
        :type gui: Module.Gui.Gui
        :type resonanzkurve: Module.Resonanzkurve.Resonanzkurve
        :type titel: str
        :type beschriftung: Module.Sonstige.Achsenbeschriftung
        """
        Canvas.__init__(self, gui, titel)
        self.resonanzkurve = resonanzkurve
        vertikal = QtGui.QVBoxLayout()
        self.centralWidget().setLayout(vertikal)
        horizontal = QtGui.QHBoxLayout()
        vertikal.addLayout(horizontal)

        label = QtGui.QLabel(raster_bereich[lang])
        horizontal.addWidget(label)

        self.box_min = QtGui.QDoubleSpinBox()
        self.box_min.setMinimum(-sys.float_info.max)
        genauigkeit(self.box_min)
        horizontal.addWidget(self.box_min)

        self.box_max = QtGui.QDoubleSpinBox()
        self.box_max.setMaximum(sys.float_info.max)
        genauigkeit(self.box_max)
        horizontal.addWidget(self.box_max)

        self.box_fehler = QtGui.QCheckBox(raster_fehler[lang])
        horizontal.addWidget(self.box_fehler)

        self.box_prozentual = QtGui.QCheckBox(raster_prozent[lang])
        self.box_prozentual.setEnabled(False)
        horizontal.addWidget(self.box_prozentual)
        horizontal.addItem(QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))

        self.box_min.valueChanged.connect(self.aktualisiere)
        self.box_max.valueChanged.connect(self.aktualisiere)
        self.box_fehler.clicked.connect(self.akt_fehler)
        self.box_prozentual.clicked.connect(self.aktualisiere)

        self.plotter = Plotter(self, beschriftung)
        vertikal.addWidget(self.plotter)
        self.plotter.mpl_connect("button_press_event", self.maus_press)

    def resizeEvent(self, event):
        """
        :type event: QtGui.QResizeEvent
        """
        # TODO
        pass

    def maus_press(self, event):
        """
        :type event: matplotlib.backend_bases.MouseEvent
        """
        if event.inaxes:
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

    def set_werte(self, neu):
        """
        :type neu: Module.Ergebnis.FitWerte
        """
        self.box_min.setValue(neu.normal_min)
        self.box_max.setValue(neu.normal_max)
        Canvas.set_werte(self, neu)

    def akt_fehler(self):
        self.box_prozentual.setEnabled(self.box_fehler.isChecked())
        self.aktualisiere()

    def aktualisiere(self):
        if self._werte is not None:
            if False:  # TODO
                plot = self.plotter.axes.imshow
            else:
                plot = self.plotter.axes.matshow

            if self.box_fehler.isChecked():
                if self.box_prozentual.isChecked():
                    grafik = plot(self._werte.fehler_prozent, vmin=0, vmax=100)
                else:
                    grafik = plot(self._werte.fehler, vmin=self._werte.fehler_min, vmax=self._werte.fehler_max)
            else:
                grafik = plot(self._werte.normal, vmin=self.box_min.value(), vmax=self.box_max.value(), cmap='hot')

            self.plotter.mit_skala(grafik)
