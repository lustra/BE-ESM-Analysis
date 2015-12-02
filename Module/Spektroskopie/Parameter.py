# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from Module.Abstrakt.Parameter import Parameter as AbstraktParameter


class Parameter(AbstraktParameter):
    """ Mess- und Fitparameter der Spektroskopie """
    def __init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung, phase_versatz,
                 df, mittelungen, bereich_links, bereich_rechts, amp_min, amp_max,
                 guete, guete_min, guete_max, off_min, off_max):
        """
        :type verzeichnis: str
        :type fmin: int
        :type fmax: int
        :type fitfunktion: (float, float, float, float, float) -> float
        :param fenster: Breite des Savitzky-Golay-Filters (für Amplitude und Phase gegen Frequenz) in Datenpunkten.
        :type fenster: int
        :param ordnung: Ordnung des Polynoms des Savitzky-Golay-Filters.
        :type ordnung: int
        :param phase_versatz: Die zur Resonanz gehörige Phase wird diese Anzahl an Messpunkten neben der
        Resonanzfrequenz aus der geglätteten Phasenmessung entnommen.
        :type phase_versatz: int
        :type df: int
        :type mittelungen: int
        :type bereich_links: int
        :type bereich_rechts: int
        :type amp_min: float
        :type amp_max: float
        :type guete: float
        :type guete_min: float
        :type guete_max: float
        :type off_min: float
        :type off_max: float
        """
        AbstraktParameter.__init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung, phase_versatz)
        self.df = df
        self.mittelungen = mittelungen
        self.bereich_links = bereich_links
        self.bereich_rechts = bereich_rechts
        self.amp_min = amp_min
        self.amp_max = amp_max
        self.guete = guete
        self.guete_min = guete_min
        self.guete_max = guete_max
        self.off_min = off_min
        self.off_max = off_max

        self.messpunkte = (fmax - fmin) // df
