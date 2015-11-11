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
from Module.Raster.Fit import Fit
from Module.Laden import GuiLaden
from Module.Sonstige import Achsenbeschriftung
from Module.Strings import *


class Gui(QtGui.QMainWindow, Ui_Gui):
    """ Menüfenster mit Rohdatenanzeige """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())

        self._fit = Fit()  # Fit-Instanz kann wegen zu viele Abhängigkeiten nicht ersetzt werden!
        # (sollte es wirklich nötig werden, dann besser gleich die gesamte Gui neu instanzieren)
        self.gui_laden = GuiLaden(self)

        self.plots = []
        self.plt_resonanzkurve = Resonanzkurve(
            liste=self.plots, fit=self.fit,
            titel=gui_resonanzkurve[lang],
            beschriftung=Achsenbeschriftung(x=achse_freq[lang], y=achse_amp[lang])
        )
        self.plt_phase_schnitt = Schnitt(
            liste=self.plots, fit=self.fit,
            titel=gui_phase_schnitt[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_phase[lang])
        )
        self.plt_amp_schnitt = Schnitt(
            liste=self.plots, fit=self.fit,
            titel=gui_amp_schnitt[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_amp[lang])
        )
        self.plt_phase = Raster(
            liste=self.plots, fit=self.fit,
            resonanzkurve=self.plt_resonanzkurve,
            titel=gui_phase[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_punkt_y[lang], farbe=achse_phase[lang])
        )
        self.plt_resfreq = Raster(
            liste=self.plots, fit=self.fit,
            resonanzkurve=self.plt_resonanzkurve,
            titel=gui_resfreq[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_punkt_y[lang], farbe=achse_freq[lang])
        )
        self.plt_amplitude = Raster(
            liste=self.plots, fit=self.fit,
            resonanzkurve=self.plt_resonanzkurve,
            titel=gui_amplitude[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_punkt_y[lang], farbe=achse_amp[lang])
        )
        self.plt_qfaktor = Raster(
            liste=self.plots, fit=self.fit,
            resonanzkurve=self.plt_resonanzkurve,
            titel=gui_qfaktor[lang],
            beschriftung=Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_punkt_y[lang])
        )

        self.action_raster.triggered.connect(self.laden)
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
        self.action_spektroskopie.setText(gui_spektroskopie[lang])
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

    @property
    def fit(self):
        return self._fit

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

    def laden(self):
        self.gui_laden.show()
        self.gui_laden.raise_()

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

    def aktualisieren(self):
        for plt in self.plots:
            plt.aktualisieren()

    def zeige_alles(self):
        for plt in self.plots:  # TODO stattdessen alle Graphen in einem Fenster darstellen
            plt.zeige()
