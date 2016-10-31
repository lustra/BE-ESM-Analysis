# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os
from lmfit import Model

from Module.FitFunktion import phase_lorentz, phase_phenom
from Module.Sonstige import Fehler


class Parameter:
    """ Alle für den Fit einer Rastermessung nötigen Messparameter """
    def __init__(self, datei, fmin, fmax, fitfunktion, fenster, ordnung, phase_modus, phase_versatz,
                 df, bereich_links, bereich_rechts, amp_min, amp_max, guete_min, guete_max, off_min, off_max):
        """
        :type datei: str
        :type fmin: int
        :type fmax: int
        :param fitfunktion: Mit den Parametern Frequenz, Resonanzfrequenz, Amplitude, Güte und Offset
        :type fitfunktion: (float, float, float, float, float) -> float
        :param fenster: Breite des Savitzky-Golay-Filters (für Amplitude und Phase gegen Frequenz) in Datenpunkten.
        :type fenster: int
        :param ordnung: Ordnung des Polynoms des Savitzky-Golay-Filters.
        :type ordnung: int
        :param phase_modus: Fitmethodik für die Phase: 1 = atan(phi), 2 = Messwerte
        :type phase_modus: int
        :param phase_versatz: Die zur Resonanz gehörige Phase wird diese Anzahl an Messpunkten neben der
        Resonanzfrequenz aus der geglätteten Phasenmessung entnommen.
        :type phase_versatz: int
        :type df: int
        :type bereich_links: int
        :type bereich_rechts: int
        :type amp_min: float
        :type amp_max: float
        :type guete_min: float
        :type guete_max: float
        :type off_min: float
        :type off_max: float
        """
        if fmin >= fmax or amp_min >= amp_max or guete_min >= guete_max or off_min >= off_max:
            raise Fehler()

        self.datei = datei
        """ Pfad zum Ordner, der alle Messdateien enthält """
        self.fmin = fmin
        """ Anfangsfrequenz des Spektrums der Bandanregung in Hz """
        self.fmax = fmax
        """ Endfrequenz des Spektrums der Bandanregung in Hz """
        self.mod_amp = Model(fitfunktion)
        """ Zum Fitten der Amplitude in Abhängigkeit zur Phase für jede einzelne Messung verwendete Funktion """
        if not fenster & 1:  # Die Breite muss ungerade sein
            fenster += 1
        self.fenster = fenster
        """ Messpunkteanzahl der Breite des Savitzky-Golay-Filters, ist immer ungerade """
        self.ordnung = ordnung
        """ Grad des für den Savitzky-Golay-Filter verwendeten Polynoms """
        self.mod_ph = [
            Model(phase_lorentz),
            Model(phase_phenom),
            None
        ][phase_modus]
        """ Fit-Model für die Phase """
        self.phase_versatz = phase_versatz
        """ Die Phase wird diese Anzahl an Messpunkten neben der Resonanzfrequenz der Phasenauswertung entnommen """
        self.bereich_links = bereich_links
        """ Die Anzahl der zu entfernenden niedrigen Frequenzen """
        self.bereich_rechts = bereich_rechts
        """ Die Anzahl der zu entfernenden hohen Frequenzen """
        self.amp_min = amp_min
        """ Minimale Amplitude für den Fit """
        self.amp_max = amp_max
        """ Maximale Amplitude für den Fit """
        self.guete_min = guete_min
        """ Minimaler Gütefaktor beim Amplitudenfit """
        self.guete_max = guete_max
        """ Maximaler Gütefaktor beim Amplitudenfit """
        self.off_min = off_min
        """ Minimaler Untergrund beim Amplitudenfit """
        self.off_max = off_max
        """ Maximaler Untergrund beim Amplitudenfit """

        self.df = df
        """ Abstand der Messwerte auf der Frequenzskala in Hz """
        self.messpunkte = int((fmax - fmin) // df)
        """ Anzahl der Messpunkte bezüglich der Freqzenz """
