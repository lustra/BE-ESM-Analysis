# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os
import sys
from PyQt4 import QtGui

from ResonanzFit import hinweis, lang
from Module.Canvas import Canvas, Optionen
from Module.Resonanzkurve import Resonanzkurve
from Module.Schnitt import Schnitt
from Design.Gui import Ui_Gui
from Module.Fit import Fit
from Module.Laden import GuiLaden
from Module.Sonstige import Achsenbeschriftung
from Module.Strings import *


class Gui(QtGui.QMainWindow, Ui_Gui):
    """ Menüfenster mit Rohdatenanzeige """
    # noinspection PyUnresolvedReferences
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
            beschriftung=Achsenbeschriftung(x=achse_amp[lang], y=achse_freq[lang])
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
        achse_raster = Achsenbeschriftung(x=achse_punkt_x[lang], y=achse_punkt_y[lang])
        self.plt_phase = Canvas(self.plots, gui_phase[lang], achse_raster, mit_fehler=False)
        self.plt_resfreq = Canvas(self.plots, gui_resfreq[lang],achse_raster, mit_fehler=True)
        self.plt_amplitude = Canvas(self.plots, gui_amplitude[lang], achse_raster, mit_fehler=True)
        self.plt_qfaktor = Canvas(self.plots, gui_qfaktor[lang], achse_raster, mit_fehler=True)

        self.action_laden.triggered.connect(self.laden)
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
        self.action_glaetten.triggered.connect(self.aktualisieren)
        self.action_prozent.triggered.connect(self.aktualisieren)

    def retranslateUi(self, ui):
        """
        :type ui: QtGui.QMainWindow
        """
        ui.setWindowTitle(gui_titel[lang])
        self.label_amplitude.setText(gui_amplitude[lang])
        self.label_phase.setText(gui_phase[lang])
        self.menu_messung.setTitle(gui_auswertung[lang])
        self.menu_ansicht.setTitle(gui_ansicht[lang])
        self.menu_darstellung.setTitle(gui_darstellung[lang])
        self.action_laden.setText(gui_oeffnen[lang])
        self.action_speichern.setText(gui_speichern[lang])
        self.action_resonanzkurve.setText(gui_resonanzkurve[lang])
        self.action_phase_schnitt.setText(gui_phase_schnitt[lang])
        self.action_amp_schnitt.setText(gui_amp_schnitt[lang])
        self.action_resfreq.setText(gui_resfreq[lang])
        self.action_amplitude.setText(gui_amplitude[lang])
        self.action_phase.setText(gui_phase[lang])
        self.action_qfaktor.setText(gui_qfaktor[lang])
        self.action_alles.setText(gui_alles[lang])
        self.action_aktualisieren.setText(gui_aktualisieren[lang])
        self.action_glaetten.setText(gui_glaetten[lang])
        self.action_prozent.setText(gui_prozent[lang])

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
        self.plt_resonanzkurve.werte = self.fit.messwerte.amplitude

    def laden(self):
        self.gui_laden.show()
        self.gui_laden.raise_()

    def speichern(self):
        wohin = QtGui.QFileDialog().getSaveFileName(self, rf_ordner[lang], self.fit.par.verzeichnis)
        self.fit.erg.speichern(str(wohin))
        hinweis(gui_gespeichert[lang] + wohin)

    def fit_fertig(self):
        self.action_speichern.setEnabled(True)
        self.plt_phase_schnitt.werte = self.fit.erg.phase
        self.plt_amp_schnitt.werte = self.fit.erg.damp
        self.plt_phase.werte = self.fit.erg.phase
        self.plt_resfreq.werte = self.fit.erg.resfreq
        self.plt_amplitude.werte = self.fit.erg.damp
        self.plt_qfaktor.werte = self.fit.erg.q

    def aktualisieren(self):
        for plt in self.plots:
            plt.optionen = Optionen(
                glaetten=self.action_glaetten.isChecked(),
                prozentual=self.action_prozent.isChecked()
            )

    def zeige_alles(self):
        for plt in self.plots:  # TODO stattdessen alle Graphen in einem Fenster darstellen
            plt.zeige()
