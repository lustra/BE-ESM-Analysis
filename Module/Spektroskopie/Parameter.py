# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from Module.Abstrakt.Parameter import Parameter as AbstraktParameter


class Parameter(AbstraktParameter):
    """ Mess- und Fitparameter der Spektroskopie """
    def __init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung,
                 df, mittelungen, bereich_links, bereich_rechts, amp_min, amp_max,
                 guete, guete_min, guete_max, off_min, off_max):
        """
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
        """
        AbstraktParameter.__init__(self, verzeichnis, fmin, fmax, fitfunktion, fenster, ordnung)
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
