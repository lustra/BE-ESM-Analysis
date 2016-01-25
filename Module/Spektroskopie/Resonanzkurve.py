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


class Resonanzkurve(Canvas):
    def __init__(self, gui, titel, beschriftung):
        """
        :type gui: Module.Gui.Gui
        :type titel: str
        :type beschriftung: Module.Sonstige.Achsenbeschriftung
        """
        Canvas.__init__(self, gui, titel)
        vertikal = QtGui.QVBoxLayout()
        self.centralWidget().setLayout(vertikal)

        self.plotter = Plotter(self, beschriftung)
        vertikal.addWidget(self.plotter)

        horizontal = QtGui.QHBoxLayout()
        vertikal.addLayout(horizontal)
        sp = QtGui.QSizePolicy()
        sp.setHorizontalPolicy(sp.Maximum)

        def neue_cbox(text):
            """
            :param text: Beschriftung vor der Auswahlbox
            :type text: str
            """
            cbox = QtGui.QComboBox()
            label = QtGui.QLabel(text)
            label.setSizePolicy(sp)
            horizontal.addWidget(label)
            horizontal.addWidget(cbox)
            cbox.currentIndexChanged.connect(self.aktualisiere)
            return cbox

        self.box_omega = neue_cbox(wahl_omega[lang])
        self.box_ac = neue_cbox(wahl_ac[lang])
        self.box_dc = neue_cbox(wahl_dc[lang])

        self.box_omega.value = lambda: int(self.box_omega.currentText())
        self.box_ac.value = lambda: float(self.box_ac.currentText())
        self.box_dc.value = lambda: float(self.box_dc.currentText())

        self.gesperrt = False

    @staticmethod
    def str_status(x, y):
        """
        :type x: float
        :type y: float
        """
        return str(x) + " | " + str(y)

    def set_werte(self, neu):
        """
        :type neu: Spektroskopie.Messwerte.Messwerte
        """
        self.gesperrt = True
        self.box_omega.clear()
        self.box_omega.addItems(neu.str_omegas())
        self.box_ac.clear()
        self.box_ac.addItems(neu.str_acs(self.box_omega.value()))
        self.box_dc.clear()
        self.box_dc.addItems(neu.str_dcs(self.box_omega.value(), self.box_ac.value()))
        self._werte = neu  # Kein super-Aufruf, weil _werte hier streng genommen einen anderen Typ hat
        self.gesperrt = False
        self.aktualisiere()

    def aktualisiere(self):
        if self._werte is not None and not self.gesperrt:
            ac = self._werte.omega(self.box_omega.value()).ac(self.box_ac.value())
            dc = ac.dc.index(self.box_dc.value())
            self.plotter.axes.plot(
                self._werte.frequenzen,
                ac.amp_freq[dc],
                antialiased=True
            )
            self.plotter.draw()
