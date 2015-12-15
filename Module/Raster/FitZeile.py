# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
from scipy.signal import savgol_filter
from scipy.optimize import leastsq
from lmfit.models import Model
from lmfit import Parameters
# # from PyQt4.QtCore import QRunnable

from Module.Phase import phase_ermitteln


debug_schnell = False


class FitLeastSq:
    def __init__(self, errorfunc, p0, frequenzen, amplituden):
        self.solp, self.convx, self.infodict, self.mesg, self.ier = leastsq(
            func=errorfunc,
            x0=p0,
            args=(frequenzen, amplituden),
            Dfun=None,
            full_output=True,
            ftol=1e-9,
            xtol=1e-9,
            maxfev=50000,
            epsfcn=1e-10,
            factor=0.1
        )


class FitZeile:
    def __init__(self, messwerte, p0, norm, y):
        # # QRunnable.__init__(self)
        # # self.emit = emit
        self.messwerte = messwerte
        self.par = messwerte.par
        self.p0 = p0
        self.norm = norm
        self.y = y

        self.fitparameter = np.ones((messwerte.par.pixel, 3))
        self.error_fitparameter = np.ones((messwerte.par.pixel, 3))
        self.sphase = np.ones(messwerte.par.pixel)  # single phase point off resonance
        self.iterationen = np.ones(messwerte.par.pixel)

    def run(self):
        par = self.par
        """ :type: Module.Raster.Parameter.Parameter """
        
        if debug_schnell:
            self.fitparameter = np.random.rand(par.pixel, 3)
            self.error_fitparameter = np.random.rand(par.pixel, 3)
            self.sphase = np.random.sample(par.pixel)
            self.iterationen = np.random.sample(par.pixel)
            return

        amplituden = self.messwerte.amplituden(self.y)
        phasen = self.messwerte.phasen(self.y)

        for x in range(par.pixel):  # x-Achse
            savgol_amplituden = savgol_filter(amplituden[x], par.fenster, par.ordnung)
            
            # Fitparameter für die Fitfunktion
            params = Parameters()
            params.add('resfreq', value=par.fmin, min=par.fmin, max=par.fmax)  # TODO
            params.add('amp', value=0.1, min=0, max=10)
            params.add('guete', value=10, min=0, max=1000)
            params.add('off', value=0, min=0, max=1)

            # Fitprozess starten
            mod = Model(par.fitfunktion)
            erg = mod.fit(
                data=savgol_amplituden,
                freq=self.messwerte.frequenzen,
                params=params
            )

            # TODO Auf jeden Fall überarbeiten! Das ist nur eine Behilfslösung zur Anpassung an die veraltete Struktur.
            self.fitparameter[x, 0] = erg.best_values['resfreq']
            self.fitparameter[x, 1] = erg.best_values['amp']
            self.fitparameter[x, 2] = erg.best_values['guete']
            self.error_fitparameter[x, 0] = erg.chisqr
            self.error_fitparameter[x, 1] = erg.chisqr
            self.error_fitparameter[x, 2] = erg.chisqr

            self.sphase[x] = phase_ermitteln(
                phase_freq=phasen[x],
                resfreq=int((erg.best_values['resfreq'] - par.fmin) / par.df),
                versatz=par.phase_versatz,
                modus=par.phase_modus,
                savgol=self.filter
            ).best_fit[0]

        # # from Module.Fit import signal
        # # self.emit(signal.weiter)

    def filter(self, daten):
        return savgol_filter(daten, self.par.fenster, self.par.ordnung)
