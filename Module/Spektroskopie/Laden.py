# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os
from PyQt4 import QtGui

from ResonanzFit import hinweis, lang
from Design.SpektrLaden import Ui_SpektrLaden
from Module.Abstrakt.Laden import GuiAbstraktLaden
from Module import FitFunktion
from Module.Sonstige import Parameter
from Module.Strings import *
from Module.Spektroskopie.BeSpektroskopieTest import test_fit, fit_datei
from Module.Spektroskopie.Fitparameter import Fitparameter


class GuiSpektrLaden(GuiAbstraktLaden, Ui_SpektrLaden):
    """ Ordnerauswahl, Einstellung der Parameter und Fit """
    def __init__(self, app):
        """
        :type app: Module.Gui.Gui
        """
        GuiAbstraktLaden.__init__(self, app, app.spektr_fit_fertig)
        self.setupUi(self)
        self.init_ui()

        self.box_omega.valueChanged.connect(self.fit_vorschau)
        self.box_ac.valueChanged.connect(self.fit_vorschau)
        self.box_dc.valueChanged.connect(self.fit_vorschau)

    def retranslateUi(self, ui):
        """
        :type ui: QtGui.QMainWindow
        """
        ui.setWindowTitle(laden_spektr_titel[lang])
        self.button_aendern.setText(laden_aendern[lang])
        self.check_konfig.setText(laden_konfiguration[lang])
        self.label_mittelungen.setText(laden_mittelungen[lang])
        self.label_df.setText(laden_df[lang])
        self.label_fmin.setText(laden_fmin[lang])
        self.label_fmax.setText(laden_fmax[lang])
        self.label_methode.setText(laden_methode[lang])
        self.box_methode.setItemText(0, laden_damp[lang])
        self.box_methode.setItemText(1, laden_camp[lang])
        self.box_methode.setItemText(2, laden_phase[lang])
        self.label_bereich.setText(laden_bereich[lang])
        self.label_bereich_links.setText(laden_links[lang])
        self.label_bereich_rechts.setText(laden_rechts[lang])
        self.label_fitparameter.setText(laden_fitparameter[lang])
        self.label_amp_min.setText(laden_amp[lang])
        self.label_amp_max.setText(laden_bis[lang])
        self.label_untergrund_min.setText(laden_untergrund[lang])
        self.label_untergrund_max.setText(laden_bis[lang])
        self.label_guete.setText(laden_guete[lang])
        self.label_guete_min.setText(laden_von[lang])
        self.label_guete_max.setText(laden_bis[lang])
        self.button_fitten.setText(laden_fitten[lang])
        self.button_vorschau.setText(laden_vorschau[lang])
        self.label_omega.setText(laden_omega[lang])
        self.label_ac.setText(laden_ac[lang])
        self.label_dc.setText(laden_dc[lang])

    def set_input_enabled(self, b):
        """
        :type b: bool
        """
        self.edit_pfad.setEnabled(b)
        self.button_aendern.setEnabled(b)
        # self.check_konfig.setEnabled(b)  # TODO Messkonfiguration abspeichern + einlesen
        self.box_mittelungen.setEnabled(b)
        self.box_df.setEnabled(b)
        self.box_fmin.setEnabled(b)
        self.box_fmax.setEnabled(b)
        self.box_methode.setEnabled(b)
        self.box_bereich_links.setEnabled(b)
        self.box_bereich_rechts.setEnabled(b)
        self.box_fmin.setEnabled(b)
        self.box_fmax.setEnabled(b)
        self.box_amp_min.setEnabled(b)
        self.box_amp_max.setEnabled(b)
        self.box_untergrund_min.setEnabled(b)
        self.box_untergrund_max.setEnabled(b)
        self.box_guete.setEnabled(b)
        self.box_guete_min.setEnabled(b)
        self.box_guete_max.setEnabled(b)

    def packe_parameter(self):
        if self.box_fmin.value() < self.box_fmax.value()\
                and self.box_amp_min.value() < self.box_amp_max.value()\
                and self.box_guete_min.value() < self.box_guete_max.value()\
                and self.box_untergrund_min.value() < self.box_untergrund_max.value():
            return Fitparameter(
                omega=1,  # TODO
                fmin=int(1000*self.box_fmin.value()),
                fmax=int(1000*self.box_fmax.value()),
                df=self.box_df.value(),
                mittelungen=self.box_mittelungen.value(),
                bereich_links=self.box_bereich_links.value(),
                bereich_rechts=self.box_bereich_rechts.value(),
                amp_min=self.box_amp_min.value(),
                amp_max=self.box_amp_max.value(),
                guete=self.box_guete.value(),
                guete_min=self.box_guete_min.value(),
                guete_max=self.box_guete_max.value(),
                off_min=self.box_untergrund_min.value(),
                off_max=self.box_untergrund_max.value()
            )
        else:
            hinweis(self, laden_min_max[lang])

    def start_fit(self):
        parameter = self.packe_parameter()

        GuiAbstraktLaden.start_fit(self)
        # Fortschrittsbalken vorbereiten
        #self.progress_bar.setMaximum(self.box.value())

        # Fitten
        test_fit(
            ordner=str(self.edit_pfad.text()),
            par=parameter
        )

    def fit_vorschau(self):
        out, ph, datx, daty = fit_datei(
            name=self.edit_pfad.text() + os.sep + "amp" + str(self.box_omega.value()) + 'w' + num(self.box_ac) + 'G' + num(self.box_dc) + "V.tdms",
            par=self.packe_parameter()
        )

        self.plotter.axes.plot(datx, daty, antialiased=True)
        self.plotter.axes.hold(True)
        self.plotter.axes.plot(datx, out.best_fit)
        self.plotter.axes.hold(False)
        self.plotter.draw()


def num(box):
    """
    :type box: PyQt4.QtGui.QSpinBox.QSpinBox
    """
    return str("{:.6f}".format(box.value())).replace('.', ',')