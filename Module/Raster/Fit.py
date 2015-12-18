# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np

from Module.Abstrakt.Fit import Fit as AbstraktFit
from Module.Pool import omap

from Messwerte import Messwerte
from Ergebnis import Ergebnis, FitWerte


class Fit(AbstraktFit):
    def __init__(self, laden, par):
        """
        :type laden: Module.Raster.Laden.GuiRasterLaden
        :type par: Module.Raster.Parameter.Parameter
        """
        AbstraktFit.__init__(self, laden, par)
        self.messwerte = None
        """ :type: Messwerte """
        self.erg = None
        """ :type: Ergebnis """

    def impl_fit(self):
        par = self.par
        pixel = par.pixel

        # TODO Multi-Prozessierung

        def neu():
            return np.ones((pixel, pixel))
        erg_resfreq = neu()
        fhlr_resfreq = neu()
        erg_amp = neu()
        fhlr_amp = neu()
        erg_q = neu()
        fhlr_q = neu()
        erg_phase = neu()  # single phase point off resonance
        fhlr_phase = neu()

        if Fit.debug_schnell:
            pixel = 0

        """Pool().map(
            lambda y: Pool().map(
                lambda x: self.fit(amplituden[x], phasen[y]),
                range(pixel)
            ),
            range(pixel)
        )"""

        for y in range(pixel):
            amplituden = self.messwerte.amplituden(y)
            phasen = self.messwerte.phasen(y)
            
            for x in range(pixel):
                amp, ph = self.fit(amplituden[x], phasen[y])
                
                erg_resfreq[y, x] = amp.best_values['resfreq']
                fhlr_resfreq[y, x] = amp.params['resfreq'].stderr
                erg_amp[y, x] = amp.best_values['amp']
                fhlr_amp[y, x] = amp.params['amp'].stderr
                erg_q[y, x] = amp.best_values['guete']
                fhlr_q[y, x] = amp.params['guete'].stderr
                erg_phase[y, x] = ph.mit_versatz
                fhlr_phase[y, x] = ph.chisqr  # TODO

            self.signal_weiter()

        # Fitprozess abschließen ##########
        self.erg = Ergebnis(
            FitWerte(erg_resfreq, fhlr_resfreq),
            FitWerte(erg_amp, fhlr_amp),
            FitWerte(erg_q, fhlr_q),
            FitWerte(erg_phase, fhlr_phase)
        )

    def lade_messwerte(self):
        self.messwerte = Messwerte(self.par)

    def speichern(self, wohin):
        """
        :type wohin: str
        """
        self.erg.speichern(wohin)
