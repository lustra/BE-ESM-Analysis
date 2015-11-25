# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np

from Module.Abstrakt.Fit import Fit as AbstraktFit
from Module.Raster.FitZeile import FitZeile
from Module.Raster.Messwerte import Messwerte
from Module.Ergebnis import Ergebnis
from Module.Signal import signal


class Fit(AbstraktFit):
    def __init__(self, laden, par):
        """
        :type laden: Module.Raster.Laden.GuiRasterLaden
        :type par: Module.Raster.Parameter.Parameter
        """
        AbstraktFit.__init__(self, laden, par)
        self.messwerte = None
        """ @type: Module.Raster.Messwerte.Messwerte """

    def impl_fit(self):
        # p0 = Initial guess
        p0 = np.array([(self.par.fmax - self.par.fmin) / 2 + self.par.fmin, 0.1, 5], dtype=np.double)

        norm = len(self.messwerte.amplitude) - len(p0)

        fitparameter = np.ones((self.par.pixel, self.par.pixel, 3))
        error_fitparameter = np.ones((self.par.pixel, self.par.pixel, 3))
        sphase = np.ones((self.par.pixel, self.par.pixel))  # single phase point off resonance
        iterationen = np.ones((self.par.pixel, self.par.pixel))

        def weitere_zeile(z):
            fitparameter[z.y] = z.fitparameter
            error_fitparameter[z.y] = z.error_fitparameter
            sphase[z.y] = z.sphase
            iterationen[z.y] = z.iterationen
            self.emit(signal.weiter)

        # TODO Multi-Prozessierung
        """# Multi-Prozessierung, aber Vorsicht: jeder Prozess arbeitet zwangsweise mit seiner eigenen Speicherkopie
        pool = QtCore.QThreadPool()
        QtCore.QObject.connect(pool, signal.weiter, weitere_zeile)
        for y in range(self.par.pixel):
            if self.weiter:
                while not pool.tryStart(
                    # Eine Zeile fitten
                    FitZeile(self.messwerte, p0, norm, y)
                ):
                    pass
        pool.waitForDone()"""

        # Single-Processing
        for y in range(self.par.pixel):
            if self.weiter:
                zeile = FitZeile(self.messwerte, p0, norm, y)
                zeile.run()
                weitere_zeile(zeile)
            else:
                break

        # Fitprozess abschließen ##########
        self.erg = Ergebnis(fitparameter, error_fitparameter, sphase)

        self.av_iter = int(np.average(iterationen))

    def lade_messwerte(self):
        self.messwerte = Messwerte(self.par)
