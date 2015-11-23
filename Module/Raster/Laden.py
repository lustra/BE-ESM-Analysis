# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui

from ResonanzFit import hinweis, lang
from Design.RasterLaden import Ui_RasterLaden
from Module.Abstrakt.Laden import GuiAbstraktLaden
from Module import FitFunktion
from Module.Sonstige import Parameter
from Module.Strings import *


class GuiRasterLaden(GuiAbstraktLaden, Ui_RasterLaden):
    """ Ordnerauswahl, Einstellung der Parameter und Fit """
    def __init__(self, app):
        """
        :type app: Module.Gui.Gui
        """
        GuiAbstraktLaden.__init__(self, app, app.raster_fit_fertig)
        self.setupUi(self)
        self.init_ui()

    def retranslateUi(self, ui):
        """
        :type ui: QtGui.QMainWindow
        """
        ui.setWindowTitle(laden_raster_titel[lang])
        self.button_aendern.setText(laden_aendern[lang])
        self.button_konfig.setText(laden_konfiguration[lang])
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
        self.button_konfig.setEnabled(b)
        self.box_messpunkte.setEnabled(b)
        self.box_pixel.setEnabled(b)
        self.box_fmin.setEnabled(b)
        self.box_fmax.setEnabled(b)
        self.box_methode.setEnabled(b)
        self.box_fenster.setEnabled(b)
        self.box_ordnung.setEnabled(b)

    def konfig_lesen(self):
        parser = GuiAbstraktLaden.konfig_lesen(self)
        konfig = "konfig"
        self.box_fmin.setValue(0.001 * parser.getint(konfig, "fmin"))
        self.box_fmax.setValue(0.001 * parser.getint(konfig, "fmax"))
        self.box_df.setValue(parser.getfloat(konfig, "df"))
        self.box_mittelungen.setValue(parser.getint(konfig, "mittelungen"))

    def start_fit(self):
        if self.box_fmin.value() < self.box_fmax.value():
            GuiAbstraktLaden.start_fit(self)
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
        else:
            hinweis(self, laden_min_max[lang])
