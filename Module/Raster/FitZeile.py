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
        
        if debug_schnell:
            self.fitparameter = np.random.rand(par.pixel, 3)
            self.error_fitparameter = np.random.rand(par.pixel, 3)
            self.sphase = np.random.sample(par.pixel)
            self.iterationen = np.random.sample(par.pixel)
            return

        amplituden = self.messwerte.amplituden(self.y)
        phasen = self.messwerte.phasen(self.y)

        for x in range(par.pixel):  # x-Axis
            savgol_amplituden = savgol_filter(amplituden[x], par.fenster, par.ordnung)
            
            # Fitparameter für die Fitfunktion
            params = Parameters()
            params.add('resfreq', value=par.fmin, min=par.fmin, max=par.fmax)  # TODO
            params.add('amp', value=0.1, min=0, max=10)
            params.add('guete', value=10, min=0, max=1000)
            params.add('off', value=0, min=0, max=1)

            # Fitprozess starten
            mod = Model(par.fitfunktion)
            pixel_fit = mod.fit(
                data=savgol_amplituden,
                freq=self.messwerte.frequenzen,
                params=params
            )
            #pixel_fit = FitLeastSq(par.errorfunc, self.p0, self.messwerte.frequenzen, savgol_amplituden)
            self.fitparameter[x] = np.array(pixel_fit.solp, dtype=float)

            # Berechnung der Standardabweichung ##########
            # noinspection PyUnresolvedReferences
            s_sq = (par.errorfunc(
                self.fitparameter[x], self.messwerte.frequenzen, amplituden[x]
            ) ** 2).sum() / self.norm
            pconx = pixel_fit.convx * s_sq

            error = []
            for j in range(len(pconx)):
                error.append(np.sqrt(np.absolute(pconx[j][j])))
            self.error_fitparameter[x] = error
            # ##########

            self.iterationen[x] = pixel_fit.infodict.get("nfev")

            # Phase calculation ##########
            smoothed_phase = savgol_filter(phasen[x], par.fenster, par.ordnung)
            ind = np.argmax(savgol_amplituden) + 20  # TODO Phasenveränderung off resonanz per Frequenz nicht Punkte ändern.
            self.sphase[x] = smoothed_phase[ind]

        # # from Module.Fit import signal
        # # self.emit(signal.weiter)
