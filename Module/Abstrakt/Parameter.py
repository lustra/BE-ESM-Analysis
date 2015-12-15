# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import os

from Module.Sonstige import Fehler


class Parameter:
    """ Alle für den Fit einer Rastermessung nötigen Messparameter """
    def __init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung, phase_modus, phase_versatz,
                 df, bereich_links, bereich_rechts, amp_min, amp_max, guete_min, guete_max, off_min, off_max):
        """
        :type verzeichnis: str
        :type fmin: int
        :type fmax: int
        :param fitfunktion: Mit den Parametern Frequenz, Resonanzfrequenz, Amplitude, Güte und Offset
        :type fitfunktion: (float, float, float, float, float) -> float
        :param fenster: Breite des Savitzky-Golay-Filters (für Amplitude und Phase gegen Frequenz) in Datenpunkten.
        :type fenster: int
        :param ordnung: Ordnung des Polynoms des Savitzky-Golay-Filters.
        :type ordnung: int
        :param phase_modus: Der Parameter 'modus' der Funktion Module.Phase.phase_ermitteln()
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

        self.verzeichnis = verzeichnis if verzeichnis.endswith(os.sep) else verzeichnis + os.sep
        self.fmin = fmin
        self.fmax = fmax
        self.fitfunktion = fitfunktion
        self.fenster = fenster
        self.ordnung = ordnung
        self.phase_modus = phase_modus
        self.phase_versatz = phase_versatz
        self.bereich_links = bereich_links
        self.bereich_rechts = bereich_rechts
        self.amp_min = amp_min
        self.amp_max = amp_max
        self.guete_min = guete_min
        self.guete_max = guete_max
        self.off_min = off_min
        self.off_max = off_max

        self.df = df
        self.messpunkte = int((fmax - fmin) // df)
