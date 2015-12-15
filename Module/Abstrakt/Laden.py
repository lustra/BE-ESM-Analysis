# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os
import time
from PyQt4 import QtGui
from ConfigParser import ConfigParser, NoSectionError

from ResonanzFit import hinweis, lang, ordner
from Module.Strings import *
from Module.Sonstige import Fehler


class GuiAbstraktLaden(QtGui.QMainWindow):
    """ Ordnerauswahl, Einstellung der Parameter und Fit """
    def __init__(self, app, app_fit_fertig):
        """
        :type app: Module.Gui.Gui
        :type app_fit_fertig: () -> None
        """
        QtGui.QMainWindow.__init__(self)
        self.app = app
        self.app_fit_fertig = app_fit_fertig
        self.entsperrt = True

    def init_ui(self):
        self.setFixedSize(self.size())
        self.edit_pfad.setText(ordner)

        self.button_aendern.clicked.connect(self.ordnerwahl)
        self.button_konfig.clicked.connect(self.konfig_lesen)
        self.button_fitten.clicked.connect(self.geklickt)

    def beschriften(self):
        self.button_aendern.setText(laden_aendern[lang])
        self.button_konfig.setText(laden_konfiguration[lang])
        self.label_fmin.setText(laden_fmin[lang])
        self.label_fmax.setText(laden_fmax[lang])
        self.label_methode.setText(laden_methode[lang])
        self.box_methode.setItemText(0, laden_damp[lang])
        self.box_methode.setItemText(1, laden_camp[lang])
        self.label_bereich.setText(laden_bereich[lang])
        self.label_bereich_links.setText(laden_links[lang])
        self.label_bereich_rechts.setText(laden_rechts[lang])
        self.label_fitparameter.setText(laden_fitparameter[lang])
        self.label_min.setText(laden_min[lang])
        self.label_max.setText(laden_max[lang])
        self.label_amp.setText(laden_amp[lang])
        self.label_untergrund.setText(laden_untergrund[lang])
        self.label_guete.setText(laden_guete[lang])
        self.button_fitten.setText(laden_fitten[lang])
        self.button_vorschau.setText(laden_vorschau[lang])
        self.label_phase_fit.setText(laden_phase[lang])
        self.label_phase_versatz.setText(laden_versatz[lang])
        self.label_savgol.setText(laden_savgol[lang])
        self.label_fenster.setText(laden_fenster[lang])
        self.label_ordnung.setText(laden_ordnung[lang])
        self.box_phase_fit.setItemText(0, laden_ph_lorentz[lang])
        self.box_phase_fit.setItemText(1, laden_ph_penom[lang])
        self.box_phase_fit.setItemText(2, laden_ph_direkt[lang])

    def ordnerwahl(self):
        self.edit_pfad.setText(
            QtGui.QFileDialog().getExistingDirectory(self, rf_ordner[lang], ordner)
        )
        try:
            self.konfig_lesen()
        except NoSectionError:
            print('Messkonfigurationsdatei fehlerhaft / nicht gefunden')

    def konfig_lesen(self):
        parser = ConfigParser()
        parser.read(str(self.edit_pfad.text()) + os.sep + 'konfig.ini')
        return parser

    def geklickt(self):
        if self.entsperrt:
            try:
                self.start_fit()
            except Fehler:
                self.entsperren()
                hinweis(self, laden_min_max[lang])
        else:
            self.app.fit.abbruch()
            while self.app.fit.isRunning():
                time.sleep(0.01)
            self.app_fit_fertig()
            self.entsperren()

    def entsperren(self):
        self.entsperrt = True
        self.progress_bar.setValue(0)
        self.button_fitten.setChecked(False)
        self.button_fitten.setText(laden_fitten[lang])

    def start_fit(self):
        self.entsperrt = False
        self.button_fitten.setText(laden_abbrechen[lang])

    def fehler(self, fehler):
        """
        :type fehler: Module.Sonstige.Fehler
        """
        hinweis(self, fehler.args[0])
        self.entsperren()

    def mehr_fortschritt(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)

    def fit_fertig(self):
        self.app_fit_fertig()
        self.close()
        self.entsperren()
        hinweis(self, laden_fertig[lang])
