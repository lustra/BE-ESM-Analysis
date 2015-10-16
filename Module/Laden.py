# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import time
from PyQt4 import QtCore, QtGui

from ResonanzFit import hinweis, lang, ordner
from Design.Laden import Ui_Laden
from Module.Signal import signal
from Module.Sonstige import Parameter
from Module.Strings import *


class GuiLaden(QtGui.QMainWindow, Ui_Laden):
    """ Ordnerauswahl, Einstellung der Parameter und Fit """
    # noinspection PyUnresolvedReferences
    def __init__(self, app):
        QtGui.QMainWindow.__init__(self)
        self.app = app
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.edit_pfad.setText(ordner)
        self.entsperrt = True

        self.button_aendern.clicked.connect(self.ordnerwahl)
        self.button_fitten.clicked.connect(self.geklickt)
        self.box_fmin.valueChanged.connect(self.neues_fmin)

    def retranslateUi(self, ui):
        ui.setWindowTitle(laden_titel[lang])
        self.button_aendern.setText(laden_aendern[lang])
        self.check_konfig.setText(laden_konfiguration[lang])
        self.label_messpunkte.setText(laden_messpunkte[lang])
        self.label_pixel.setText(laden_pixel[lang])
        self.label_fmin.setText(laden_fmin[lang])
        self.label_fmax.setText(laden_fmax[lang])
        self.button_fitten.setText(laden_fitten[lang])

    def set_input_enabled(self, b):
        self.edit_pfad.setEnabled(b)
        self.button_aendern.setEnabled(b)
        #self.check_konfig.setEnabled(b)
        self.box_messpunkte.setEnabled(b)
        self.box_pixel.setEnabled(b)
        self.box_fmin.setEnabled(b)
        self.box_fmax.setEnabled(b)

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
            verzeichnis=self.edit_pfad.text(),
            pixel=self.box_pixel.value(),
            messpunkte=self.box_messpunkte.value(),
            fmin=self.box_fmin.value(),
            fmax=self.box_fmax.value()
        )
        QtCore.QObject.connect(self.app.fit, signal.importiert, self.app.importiert)
        QtCore.QObject.connect(self.app.fit, signal.fehler, self.fehler)
        QtCore.QObject.connect(self.app.fit, signal.weiter, self.weitere_zeile)
        QtCore.QObject.connect(self.app.fit, signal.fertig, self.fit_fertig)
        self.app.fit.start()

    def fehler(self, fehler):
        hinweis(fehler.args[0])
        self.entsperren()

    def weitere_zeile(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)

    def fit_fertig(self):
        self.app.fit_fertig()
        self.close()
        self.entsperren()
