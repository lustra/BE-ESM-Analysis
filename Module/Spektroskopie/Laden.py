# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui

from ResonanzFit import hinweis, lang
from Design.SpektrLaden import Ui_SpektrLaden
from Module.Abstrakt.Laden import GuiAbstraktLaden
from Module import FitFunktion
from Module.Strings import *

from Fit import Fit
from FitVorschau import FitVorschau
from Parameter import Parameter


class GuiSpektrLaden(GuiAbstraktLaden, Ui_SpektrLaden):
    """ Ordnerauswahl, Einstellung der Parameter und Fit """
    def __init__(self, app):
        """
        :type app: Module.Gui.Gui
        """
        GuiAbstraktLaden.__init__(self, app, app.spektr_fit_fertig)
        self.setupUi(self)
        self.init_ui()

        self.button_vorschau.clicked.connect(self.init_vorschau)
        self.box_omega.currentIndexChanged.connect(self.fit_vorschau)
        self.box_ac.currentIndexChanged.connect(self.fit_vorschau)
        self.box_dc.currentIndexChanged.connect(self.fit_vorschau)

        self.box_omega.value = lambda: int(self.box_omega.currentText())
        self.box_ac.value = lambda: float(self.box_ac.currentText())
        self.box_dc.value = lambda: float(self.box_dc.currentText())

    def retranslateUi(self, ui):
        """
        :type ui: QtGui.QMainWindow
        """
        ui.setWindowTitle(laden_spektr_titel[lang])
        self.button_aendern.setText(laden_aendern[lang])
        self.button_konfig.setText(laden_konfiguration[lang])
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
        self.button_konfig.setEnabled(b)
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

    def konfig_lesen(self):
        parser = GuiAbstraktLaden.konfig_lesen(self)
        konfig = 'konfig'
        self.box_fmin.setValue(0.001 * parser.getint(konfig, 'fmin'))
        self.box_fmax.setValue(0.001 * parser.getint(konfig, 'fmax'))
        self.box_df.setValue(float(parser.get(konfig, 'df').replace(',', '.')))
        self.box_mittelungen.setValue(parser.getint(konfig, 'mittelungen'))

    def packe_parameter(self):
        if self.box_fmin.value() < self.box_fmax.value()\
                and self.box_amp_min.value() < self.box_amp_max.value()\
                and self.box_guete_min.value() < self.box_guete_max.value()\
                and self.box_untergrund_min.value() < self.box_untergrund_max.value():
            return Parameter(
                verzeichnis=str(self.edit_pfad.text()),
                fitfunktion=FitFunktion.errorfunc[self.box_methode.currentIndex()],
                fenster=15,  # TODO
                ordnung=5,
                phase_versatz=30,
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
        GuiAbstraktLaden.start_fit(self)

        # Fit vorbereiten
        parameter = self.packe_parameter()
        self.app.fit = Fit(self, parameter)

        # Fortschrittsbalken vorbereiten
        self.progress_bar.setMaximum(2 * self.app.fit.anzahl)

        # Fitten
        self.app.fit.start()

    def init_vorschau(self):
        if self.button_vorschau.isEnabled():
            fit = FitVorschau(self, self.packe_parameter())
            self.app.fit = fit
            self.box_omega.clear()
            self.box_omega.addItems(fit.messwerte.str_omegas())
            self.box_ac.clear()
            self.box_ac.addItems(fit.messwerte.str_acs(self.box_omega.value()))
            self.box_dc.clear()
            self.box_dc.addItems(fit.messwerte.str_dcs(self.box_omega.value(), self.box_ac.value()))

    def fit_vorschau(self):
        try:
            self.app.fit.par = self.packe_parameter()
            ac = self.app.fit.messwerte.omega(self.box_omega.value()).ac(self.box_ac.value())
            dc = ac.dc.index(self.box_dc.value())

            erg, phase = self.app.fit.fit(ac.amp_freq[dc], ac.phase_freq[dc])

            self.plotter.axes.plot(self.app.fit.messwerte.frequenzen, ac.amp_freq[dc], antialiased=True)
            self.plotter.axes.hold(True)
            self.plotter.axes.plot(self.app.fit.messwerte.frequenzen, erg.best_fit)
            self.plotter.axes.hold(False)
            self.plotter.draw()
        except ValueError:
            """
            Wenn die Boxen noch gefüllt werden, dann wird diese Funktion aufgerufen, versucht aber bereits auf alle
            gleichzeitig zu verwenden. Das würde zu Fehlern führen.
            """
            pass
