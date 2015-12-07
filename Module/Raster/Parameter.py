# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from Module.Abstrakt.Parameter import Parameter as AbstraktParameter


class Parameter(AbstraktParameter):
    """ Alle für den Fit einer Rastermessung nötigen Messparameter """
    def __init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung, phase_versatz,
                 pixel, messpunkte):
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
        :type pixel: int
        :type messpunkte: int
        """
        AbstraktParameter.__init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung, phase_versatz)
        self.messpunkte = messpunkte
        self.pixel = pixel
