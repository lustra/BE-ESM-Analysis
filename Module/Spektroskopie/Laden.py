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
from Module.Sonstige import Fehler

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

        self.breite_ohne_vorschau = self.widget_param.width() + 2 * self.widget_param.x()
        self.breite_mit_vorschau = self.width()

        self.widget_vorschau.setVisible(False)
        self.setFixedWidth(self.breite_ohne_vorschau)

        # Vorschau einrichten
        self.button_vorschau.clicked.connect(self.init_vorschau)

        # Messreihe auswählen
        self.button_zeige_amp.clicked.connect(self.fit_vorschau)
        self.button_zeige_phase.clicked.connect(self.fit_vorschau)
        self.box_omega.currentIndexChanged.connect(self.fit_vorschau)
        self.box_ac.currentIndexChanged.connect(self.fit_vorschau)
        self.box_dc.currentIndexChanged.connect(self.fit_vorschau)

        # Fitparameter variieren
        self.box_methode.currentIndexChanged.connect(self.fit_var)
        self.box_phase_fit.currentIndexChanged.connect(self.fit_var)
        self.box_phase_versatz.valueChanged.connect(self.fit_var)
        self.box_amp_min.valueChanged.connect(self.fit_var)
        self.box_amp_max.valueChanged.connect(self.fit_var)
        self.box_untergrund_min.valueChanged.connect(self.fit_var)
        self.box_untergrund_max.valueChanged.connect(self.fit_var)
        self.box_guete_min.valueChanged.connect(self.fit_var)
        self.box_guete_max.valueChanged.connect(self.fit_var)

        # Methoden zur typengerechten Abfrage der aktuell ausgewählten Werte
        self.box_omega.value = lambda: int(self.box_omega.currentText())
        self.box_ac.value = lambda: float(self.box_ac.currentText())
        self.box_dc.value = lambda: float(self.box_dc.currentText())

    def retranslateUi(self, ui):
        """
        :type ui: QtGui.QMainWindow
        """
        self.beschriften()
        self.setWindowTitle(laden_spektr_titel[lang])
        self.label_df.setText(laden_df[lang])
        self.label_mittelungen.setText(laden_mittelungen[lang])
        self.label_omega.setText(wahl_omega[lang])
        self.label_ac.setText(wahl_ac[lang])
        self.label_dc.setText(wahl_dc[lang])
        self.button_zeige_amp.setText(gui_amplitude[lang])
        self.button_zeige_phase.setText(laden_phase[lang])

    def konfig_lesen(self):
        parser = GuiAbstraktLaden.konfig_lesen(self)
        konfig = 'konfig'
        self.box_fmin.setValue(0.001 * parser.getint(konfig, 'fmin'))
        self.box_fmax.setValue(0.001 * parser.getint(konfig, 'fmax'))
        self.box_df.setValue(float(parser.get(konfig, 'df').replace(',', '.')))
        self.box_mittelungen.setValue(parser.getint(konfig, 'mittelungen'))

    def packe_parameter(self):
        return Parameter(
            verzeichnis=str(self.edit_pfad.text()),
            fitfunktion=FitFunktion.errorfunc[self.box_methode.currentIndex()],
            fenster=self.box_fenster.value(),
            ordnung=self.box_ordnung.value(),
            phase_modus=self.box_phase_fit.currentIndex(),
            phase_versatz=self.box_phase_versatz.value(),
            fmin=int(1000*self.box_fmin.value()),
            fmax=int(1000*self.box_fmax.value()),
            df=self.box_df.value(),
            mittelungen=self.box_mittelungen.value(),
            bereich_links=self.box_bereich_links.value(),
            bereich_rechts=self.box_bereich_rechts.value(),
            amp_min=self.box_amp_min.value(),
            amp_max=self.box_amp_max.value(),
            guete_min=self.box_guete_min.value(),
            guete_max=self.box_guete_max.value(),
            off_min=self.box_untergrund_min.value(),
            off_max=self.box_untergrund_max.value()
        )

    def start_fit(self):
        GuiAbstraktLaden.start_fit(self)

        # Fit vorbereiten
        parameter = self.packe_parameter()
        self.app.fit = Fit(self, parameter)

        # Fortschrittsbalken vorbereiten
        self.progress_bar.setMaximum(2 * self.app.fit.anzahl)

        # Fitten
        self.app.fit.start()

    def init_vorschau(self, aktiviert):
        if aktiviert:
            try:
                fit = FitVorschau(self, self.packe_parameter())
                self.app.fit = fit
                self.box_omega.clear()
                self.box_omega.addItems(fit.messwerte.str_omegas())
                self.box_ac.clear()
                self.box_ac.addItems(fit.messwerte.str_acs(self.box_omega.value()))
                self.box_dc.clear()
                self.box_dc.addItems(fit.messwerte.str_dcs(self.box_omega.value(), self.box_ac.value()))
                self.setFixedWidth(self.breite_mit_vorschau)
            except Fehler:
                self.button_vorschau.setChecked(False)
                hinweis(self, laden_min_max[lang])
        else:
            self.setFixedWidth(self.breite_ohne_vorschau)

    def fit_vorschau(self):
        try:
            fit = self.app.fit
            """ :type: Fit """
            fit.par = self.packe_parameter()
            ac = fit.messwerte.omega(self.box_omega.value()).ac(self.box_ac.value())
            dc = ac.dc.index(self.box_dc.value())

            amp, phase = fit.fit(ac.amp_freq[dc], ac.phase_freq[dc])

            if self.button_zeige_amp.isChecked():
                self.fit_plot(
                    x1=fit.messwerte.frequenzen,
                    y1=ac.amp_freq[dc],
                    x2=fit.messwerte.frequenzen,
                    y2=amp.best_fit
                )
            else:
                self.fit_plot(
                    x1=fit.messwerte.frequenzen,
                    y1=ac.phase_freq[dc],
                    x2=phase.frequenzen,
                    y2=phase.best_fit
                )
        except ValueError:
            """
            Wenn die Boxen noch gefüllt werden, dann wird diese Funktion aufgerufen, versucht aber bereits auf alle
            gleichzeitig zu verwenden. Das würde zu Fehlern führen.
            """
            pass

    def fit_var(self):
        """
        Wenn ein Fitparameter verändert wurde, dann soll, sofern die Fitvorschau aktiviert wurde, diese aktualisiert
        werden. Ansonsten passiert nichts, weil die Werte unmittelbar vor dem Fit noch einmal abgerufen werden.
        """
        if self.widget_vorschau.isVisible():
            try:
                self.fit_vorschau()
            except Fehler:
                """
                Bei der Eingabe von Fitparametern sollen Fehler noch unterdrückt werden.
                """
                pass

    def fit_plot(self, x1, y1, x2, y2):
        """
        Es sind (x1 | y1) zu glättende Messwerte und (x2 | y2) der Fit darüber.
        :type x1: list
        :type y1: list
        :type x2: list
        :type y2: list
        """
        self.plotter.axes.hold(False)
        self.plotter.axes.plot(x1, y1, antialiased=True)
        self.plotter.axes.hold(True)
        self.plotter.axes.plot(x2, y2)
        self.plotter.draw()
