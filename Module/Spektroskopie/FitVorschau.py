# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from Module.Spektroskopie.Fit import Fit
from Module.Spektroskopie.Messwerte import Messwerte


class FitVorschau(Fit):
    """ Fit-Vorschau; Die Messwerte werden sofort geladen """
    def __init__(self, laden, par):
        """
        :type laden: Module.Spektroskopie.Laden.GuiSpektrLaden
        :type par: Module.Spektroskopie.Parameter.Parameter
        """
        Fit.__init__(self, laden, par)
        self.lade_messwerte()

    def impl_fit(self):
        Fit.impl_fit(self)

    def lade_messwerte(self):
        # Die Messwerte wurden bereits eingelesen, wenn der Fit startet
        if self.messwerte is None:
            self.messwerte = Messwerte(self.par, self.signal_weiter)
