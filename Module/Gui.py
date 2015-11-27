# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os
import sys
from PyQt4 import QtGui

from ResonanzFit import hinweis, lang
from Module.Raster.Raster import Raster
from Module.Raster.Resonanzkurve import Resonanzkurve
from Module.Raster.Schnitt import Schnitt
from Design.Gui import Ui_Gui
from Module.Raster.Laden import GuiRasterLaden
from Module.Spektroskopie.Laden import GuiSpektrLaden
from Module.Sonstige import Achsenbeschriftung
from Module.Strings import *


class Gui(QtGui.QMainWindow, Ui_Gui):
    """ Menüfenster mit Rohdatenanzeige """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.fit = None
        """ @type: Module.Abstrakt.Fit.Fit """
        self.gui_raster_laden = GuiRasterLaden(self)
        self.gui_spektr_laden = GuiSpektrLaden(self)

        self.plots = []
        self.plt_resonanzkurve = Resonanzkurve(
            app=self,
            titel=gui_resonanzkurve[lang],
            beschriftung=Achsenbeschriftung(x=achse_freq[lang], y=achse_amp[lang])
        )
        self.plt_phase_schnitt = Schnitt(
            app=self,
            titel=gui_phase_schnitt[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_phase[lang])
        )
        self.plt_amp_schnitt = Schnitt(
            app=self,
            titel=gui_amp_schnitt[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_amp[lang])
        )
        self.plt_phase = Raster(
            app=self,
            resonanzkurve=self.plt_resonanzkurve,
            titel=gui_phase[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_punkt_y[lang], farbe=achse_phase[lang])
        )
        self.plt_resfreq = Raster(
            app=self,
            resonanzkurve=self.plt_resonanzkurve,
            titel=gui_resfreq[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_punkt_y[lang], farbe=achse_freq[lang])
        )
        self.plt_amplitude = Raster(
            app=self,
            resonanzkurve=self.plt_resonanzkurve,
            titel=gui_amplitude[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_punkt_y[lang], farbe=achse_amp[lang])
        )
        self.plt_qfaktor = Raster(
            app=self,
            resonanzkurve=self.plt_resonanzkurve,
            titel=gui_qfaktor[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_punkt_y[lang])
        )

        self.action_raster.triggered.connect(self.raster_laden)
        self.action_spektroskopie.triggered.connect(self.spektr_laden)
        self.action_speichern.triggered.connect(self.speichern)
        self.action_resonanzkurve.triggered.connect(self.plt_resonanzkurve.zeige)
        self.action_phase_schnitt.triggered.connect(self.plt_phase_schnitt.zeige)
        self.action_amp_schnitt.triggered.connect(self.plt_amp_schnitt.zeige)
        self.action_resfreq.triggered.connect(self.plt_resfreq.zeige)
        self.action_amplitude.triggered.connect(self.plt_amplitude.zeige)
        self.action_phase.triggered.connect(self.plt_phase.zeige)
        self.action_qfaktor.triggered.connect(self.plt_qfaktor.zeige)
        self.action_alles.triggered.connect(self.zeige_alles)
        self.action_aktualisieren.triggered.connect(self.aktualisieren)

    def retranslateUi(self, ui):
        """
        :type ui: QtGui.QMainWindow
        """
        ui.setWindowTitle(gui_titel[lang])
        self.label_amplitude.setText(gui_amplitude[lang])
        self.label_phase.setText(gui_phase[lang])
        self.menu_auswertung.setTitle(gui_auswertung[lang])
        self.menu_raster.setTitle(gui_raster[lang])
        self.menu_spektroskopie.setTitle(gui_spektroskopie[lang])
        self.action_spektroskopie.setText(gui_lade_spektroskopie[lang])
        self.action_messparameter.setText(gui_messparameter[lang])
        self.action_raster.setText(gui_lade_raster[lang])
        self.action_speichern.setText(gui_speichern[lang])
        self.action_resonanzkurve.setText(gui_resonanzkurve[lang])
        self.action_phase_schnitt.setText(gui_phase_schnitt[lang])
        self.action_amp_schnitt.setText(gui_amp_schnitt[lang])
        self.action_resfreq.setText(gui_resfreq[lang])
        self.action_amplitude.setText(gui_amplitude[lang])
        self.action_phase.setText(gui_phase[lang])
        self.action_qfaktor.setText(gui_qfaktor[lang])
        self.action_alles.setText(gui_alles[lang])

    def closeEvent(self, event):
        """
        :type event: PyQt4.QtCore.QEvent
        """
        sys.exit(0)

    def importiert(self):
        #  Name der Messung anzeigen
        self.label_name.setText(os.path.basename(self.fit.par.verzeichnis))

        #  Dateiliste befüllen
        def model(namen):
            item_model = QtGui.QStandardItemModel()
            for name in namen:
                item_model.appendRow(QtGui.QStandardItem(name))
            return item_model
        self.list_amplitude.setModel(model(self.fit.messwerte.amplitude_namen))
        self.list_phase.setModel(model(self.fit.messwerte.phase_namen))

        #  Resonanzplots bereitstellen
        self.plt_resonanzkurve.set_werte(self.fit.messwerte.amplitude)

    def raster_laden(self):
        self.gui_raster_laden.show()
        self.gui_raster_laden.raise_()

    def spektr_laden(self):
        self.gui_spektr_laden.show()
        self.gui_spektr_laden.raise_()

    def speichern(self):
        wohin = QtGui.QFileDialog().getSaveFileName(self, rf_ordner[lang], self.fit.par.verzeichnis)
        self.fit.erg.speichern(str(wohin))
        hinweis(self, gui_gespeichert[lang] + wohin)

    def raster_fit_fertig(self):
        self.action_speichern.setEnabled(True)
        self.menu_raster.setEnabled(True)
        self.plt_phase_schnitt.set_werte(self.fit.erg.phase)
        self.plt_amp_schnitt.set_werte(self.fit.erg.damp)
        self.plt_phase.set_werte(self.fit.erg.phase)
        self.plt_resfreq.set_werte(self.fit.erg.resfreq)
        self.plt_amplitude.set_werte(self.fit.erg.damp)
        self.plt_qfaktor.set_werte(self.fit.erg.q)

    def spektr_fit_fertig(self):
        self.action_speichern.setEnabled(True)
        self.menu_spektroskopie.setEnabled(True)
        print("TODO")

        ac = self.fit.messwerte.omega(1).ac(10)
        """ @type: Module.Spektroskopie.Messreihe.AC """
        from matplotlib import pyplot as plt
        plt.plot(ac.dc, ac.amp_dc, '.', label="Test")
        plt.legend(loc=9)
        plt.ylabel('Amplitude (XKorr a.u.)')
        plt.xlabel('Offset (V)')
        plt.show()

    def aktualisieren(self):
        for plt in self.plots:
            plt.aktualisieren()

    def zeige_alles(self):
        for plt in self.plots:  # TODO stattdessen alle Graphen in einem Fenster darstellen
            plt.zeige()
