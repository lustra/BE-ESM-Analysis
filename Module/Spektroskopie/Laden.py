# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import time
from PyQt4 import QtGui

from ResonanzFit import lang, ordner
from Design.SpektrLaden import Ui_SpektrLaden
from Module.Abstrakt.Laden import GuiAbstraktLaden
from Module import FitFunktion
from Module.Sonstige import Parameter
from Module.Strings import *


class GuiRasterLaden(GuiAbstraktLaden, Ui_SpektrLaden):
    """ Ordnerauswahl, Einstellung der Parameter und Fit """
    def __init__(self, app):
        """
        :type app: Module.Gui.Gui
        """
        GuiAbstraktLaden.__init__(self, app)
        self.setupUi(self)
        self.edit_pfad.setText(ordner)

        self.button_aendern.clicked.connect(self.ordnerwahl)
        self.button_fitten.clicked.connect(self.geklickt)
        self.box_fmin.valueChanged.connect(self.neues_fmin)

    def retranslateUi(self, ui):
        """
        :type ui: QtGui.QMainWindow
        """
        ui.setWindowTitle(laden_titel[lang])
        self.button_aendern.setText(laden_aendern[lang])
        self.check_konfig.setText(laden_konfiguration[lang])
        self.label_messpunkte.setText(laden_messpunkte[lang])
        self.label_df.setText(laden_df[lang])
        self.label_fmin.setText(laden_fmin[lang])
        self.label_fmax.setText(laden_fmax[lang])
        self.label_methode.setText(laden_methode[lang])
        self.box_methode.setItemText(0, laden_damp[lang])
        self.box_methode.setItemText(1, laden_camp[lang])
        self.box_methode.setItemText(2, laden_phase[lang])
        self.label_bereich.setText(laden_bereich[lang])
        self.label_bereich_min.setText(laden_von[lang])
        self.label_bereich_max.setText(laden_bis[lang])
        self.label_fitparameter.setText(laden_fitparameter[lang])
        self.label_amp_min.setText(laden_amp[lang])
        self.label_amp_max.setText(laden_bis[lang])
        self.label_untergrund_min.setText(laden_untergrund[lang])
        self.label_untergrund_max.setEnabled(laden_bis[lang])
        self.label_guete.setText(laden_guete[lang])
        self.label_guete_min.setText(laden_von[lang])
        self.label_guete_max.setText(laden_bis[lang])
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
        self.box_fmin.setEnabled(b)
        self.box_fmax.setEnabled(b)
        self.box_amp_min.setEnabled(b)
        self.box_amp_max.setEnabled(b)
        self.box_untergrund_min.setEnabled(b)
        self.box_untergrund_max.setEnabled(b)
        self.box_guete.setEnabled(b)
        self.box_guete_min.setEnabled(b)
        self.box_guete_max.setEnabled(b)

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
            self.app.raster_fit_fertig()
            self.entsperren()

    def entsperren(self):
        GuiAbstraktLaden.entsperren(self)
        self.progress_bar.setValue(0)
        self.button_fitten.setText(laden_fitten[lang])

    def start_fit(self):
        GuiAbstraktLaden.start_fit(self)
        self.button_fitten.setText(laden_abbrechen[lang])

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

    def weiterer_parameter(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)
