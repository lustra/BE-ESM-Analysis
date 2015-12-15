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
from Module.Strings import *

from Parameter import Parameter
from Fit import Fit


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
        self.beschriften()
        self.setWindowTitle(laden_raster_titel[lang])
        self.label_df.setText(laden_df[lang])
        self.label_pixel.setText(laden_pixel[lang])

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
            parameter = Parameter(
                verzeichnis=str(self.edit_pfad.text()),
                fmin=1000*self.box_fmin.value(),
                fmax=1000*self.box_fmax.value(),
                fitfunktion=FitFunktion.errorfunc[self.box_methode.currentIndex()],
                fenster=self.box_fenster.value(),
                ordnung=self.box_ordnung.value(),
                pixel=self.box_pixel.value(),
                df=self.box_df.value(),
                phase_versatz=self.box_phase_versatz.value(),
                phase_modus=self.box_phase_fit.currentIndex(),
                amp_max=self.box_amp_max.value(),
                amp_min=self.box_amp_min.value(),
                off_max=self.box_untergrund_max.value(),
                off_min=self.box_untergrund_min.value(),
                guete_max=self.box_guete_max.value(),
                guete_min=self.box_guete_min.value(),
                bereich_links=self.box_bereich_links.value(),
                bereich_rechts=self.box_bereich_rechts.value()
            )
            self.app.fit = Fit(self, parameter)
            self.app.fit.start()

        else:
            hinweis(self, laden_min_max[lang])
