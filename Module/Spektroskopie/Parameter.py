# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from Module.Abstrakt.Parameter import Parameter as AbstraktParameter


class Parameter(AbstraktParameter):
    """ Mess- und Fitparameter der Spektroskopie """
    def __init__(self, datei, fmin, fmax, fitfunktion, fenster, ordnung, phase_modus, phase_versatz,
                 df, mittelungen, bereich_links, bereich_rechts, amp_min, amp_max,
                 guete_min, guete_max, off_min, off_max):
        """
        :type datei: str
        :type fmin: int
        :type fmax: int
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
        :type mittelungen: int
        :type bereich_links: int
        :type bereich_rechts: int
        :type amp_min: float
        :type amp_max: float
        :type guete_min: float
        :type guete_max: float
        :type off_min: float
        :type off_max: float
        """
        AbstraktParameter.__init__(
            self, datei, fmin, fmax, fitfunktion, fenster, ordnung, phase_modus, phase_versatz,
            df, bereich_links, bereich_rechts, amp_min, amp_max, guete_min, guete_max, off_min, off_max
        )

        self.mittelungen = mittelungen
