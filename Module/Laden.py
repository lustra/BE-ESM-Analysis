# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import time
from PyQt4 import QtCore, QtGui

from ResonanzFit import hinweis, lang, ordner
from Design.Laden import Ui_Laden
from Module import FitFunktion
from Module.Signal import signal
from Module.Sonstige import Parameter
from Module.Strings import *


class GuiLaden(QtGui.QMainWindow, Ui_Laden):
    """ Ordnerauswahl, Einstellung der Parameter und Fit """
    def __init__(self, app):
        """
        :type app: Module.Gui.Gui
        """
        QtGui.QMainWindow.__init__(self)
        self.app = app
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.edit_pfad.setText(ordner)
        self.entsperrt = True

        self.button_aendern.clicked.connect(self.ordnerwahl)
        self.button_fitten.clicked.connect(self.geklickt)
        self.box_fmin.valueChanged.connect(self.neues_fmin)

        QtCore.QObject.connect(self.app.fit, signal.importiert, self.app.importiert)
        QtCore.QObject.connect(self.app.fit, signal.fehler, self.fehler)
        QtCore.QObject.connect(self.app.fit, signal.weiter, self.weitere_zeile)
        QtCore.QObject.connect(self.app.fit, signal.fertig, self.fit_fertig)

    def retranslateUi(self, ui):
        """
        :type ui: QtGui.QMainWindow
        """
        ui.setWindowTitle(laden_titel[lang])
        self.button_aendern.setText(laden_aendern[lang])
        self.check_konfig.setText(laden_konfiguration[lang])
        self.label_messpunkte.setText(laden_messpunkte[lang])
        self.label_pixel.setText(laden_pixel[lang])
        self.label_fmin.setText(laden_fmin[lang])
        self.label_fmax.setText(laden_fmax[lang])
        self.label_methode.setText(laden_methode[lang])
        self.box_methode.setItemText(0, laden_damp[lang])
        self.box_methode.setItemText(1, laden_camp[lang])
        self.box_methode.setItemText(2, laden_phase[lang])
        self.label_savgol.setText(laden_savgol[lang])
        self.label_fenster.setText(laden_fenster[lang])
        self.label_ordnung.setText(laden_ordnung[lang])
        self.button_fitten.setText(laden_fitten[lang])

    def set_input_enabled(self, b):
        """
        :type b: bool
        """
        self.edit_pfad.setEnabled(b)
        self.button_aendern.setEnabled(b)
        # self.check_konfig.setEnabled(b)  # TODO Messkonfiguration abspeichern + einlesen
        self.box_messpunkte.setEnabled(b)
        self.box_pixel.setEnabled(b)
        self.box_fmin.setEnabled(b)
        self.box_fmax.setEnabled(b)
        self.box_methode.setEnabled(b)
        self.box_fenster.setEnabled(b)
        self.box_ordnung.setEnabled(b)

    def ordnerwahl(self):
        self.edit_pfad.setText(
            QtGui.QFileDialog().getExistingDirectory(self, rf_ordner[lang], ordner)
        )

    def neues_fmin(self):
        self.box_fmax.setMinimum(self.box_fmin.value() + 1)

    def geklickt(self):
        if self.entsperrt:
            self.start_fit()
        else:
            self.app.fit.abbruch()
            while self.app.fit.isRunning():
                time.sleep(0.01)
            self.app.fit_fertig()
            self.entsperren()

    def entsperren(self):
        self.entsperrt = True
        self.set_input_enabled(True)
        self.progress_bar.setValue(0)
        self.button_fitten.setText(laden_fitten[lang])

    def start_fit(self):
        self.set_input_enabled(False)
        self.button_fitten.setText(laden_abbrechen[lang])
        self.entsperrt = False

        # Fortschrittsbalken vorbereiten
        self.progress_bar.setMaximum(self.box_pixel.value())

        # Fitten
        self.app.fit.par = Parameter(
            verzeichnis=str(self.edit_pfad.text()),
            messpunkte=self.box_messpunkte.value(),
            fmin=self.box_fmin.value(),
            fmax=self.box_fmax.value(),
            errorfunc=FitFunktion.errorfunc[self.box_methode.currentIndex()],
            fenster=self.box_fenster.value(),
            ordnung=self.box_ordnung.value(),
            pixel=self.box_pixel.value()
        )
        self.app.fit.start()

    def fehler(self, fehler):
        """
        :type fehler: Module.Sonstige.Fehler
        """
        hinweis(self, fehler.args[0])
        self.entsperren()

    def weitere_zeile(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)

    def fit_fertig(self):
        self.app.fit_fertig()
        self.close()
        self.entsperren()
        hinweis(self, laden_fertig[lang])
