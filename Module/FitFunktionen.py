# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
from scipy.signal import savgol_filter
from scipy.optimize import leastsq
# # from PyQt4.QtCore import QRunnable
# # from multiprocessing import Lock
# # scilock = Lock()


class FitLeastSq:
    def __init__(self, errorfunc, p0, frequenzen, amplituden):
        # # scilock.acquire()
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
        # # scilock.release()


class FitZeile:
    def __init__(self, messwerte, p0, norm, y):
        # # QRunnable.__init__(self)
        # # self.emit = emit
        self.messwerte = messwerte
        self.p0 = p0
        self.norm = norm
        self.y = y

        self.fitparameter = np.ones((messwerte.par.pixel, 3))
        self.error_fitparameter = np.ones((messwerte.par.pixel, 3))
        self.sphase = np.ones(messwerte.par.pixel)  # single phase point off resonance
        self.iterationen = np.ones(messwerte.par.pixel)

    def run(self):
        amplituden = self.messwerte.amplituden(self.y)
        phasen = self.messwerte.phasen(self.y)

        for x in range(self.messwerte.par.pixel):  # x-Axis
            savgol_amplituden = savgol_filter(amplituden[x], 15, 3)
            # Fitprozess starten
            pixel_fit = FitLeastSq(resonance_lorentz_errorfunc, self.p0, self.messwerte.frequenzen, savgol_amplituden)
            self.fitparameter[x] = np.array(pixel_fit.solp, dtype=float)

            # Berechnung der Standardabweichung ##########
            s_sq = (resonance_lorentz_errorfunc(
                self.fitparameter[x], self.messwerte.frequenzen, amplituden[x]
            ) ** 2).sum() / self.norm
            pconx = pixel_fit.convx * s_sq

            error = []
            for j in range(len(pconx)):
                error.append(np.absolute(pconx[j][j]) ** 0.5)
            self.error_fitparameter[x] = error
            # ##########

            self.iterationen[x] = pixel_fit.infodict.get("nfev")

            # Phase calculation ##########
            smoothed_phase = savgol_filter(phasen[x], 15, 3)
            ind = np.argmax(savgol_amplituden) + 20
            self.sphase[x] = smoothed_phase[ind]

        # # from Module.Fit import signal
        # # self.emit(signal.weiter)


def resonance_lorentz_errorfunc(p, x, z):
    return resonance_lorentz(p, x) - z


def resonance_lorentz(p, x):
    """
    :param p: [Resonanzfrequenz, Drive Amplitude, Güte]
    :param x: Frequenz
    :return Lorentzverteilung
    """
    # noinspection PyTypeChecker
    return p[1] * (np.power(p[0], 2) / p[2]) / np.sqrt(
        np.power(np.power(x, 2) - np.power(p[0], 2), 2) + np.power((x * p[0] / p[2]), 2)
    )


"""
def drive_lorentz(p,x):   #x ist freq, p[1] drive amplitude, p[o] resonanzfreq, p[2] ist die Guete
    return p[1]*np.power(p[0],2)/(np.sqrt((np.power(np.power(x,2)-np.power(p[0],2),2)+np.power((x*p[0]/p[2]),2))))    #lorentz funktion


def drive_lorentz_errorfunc(p,x,z):
        return drive_lorentz(p,x)-z


def phase_lorentz(p,x):
    return np.arctan((x*p[0]/p[2])/(np.power(x,2)-np.power(p[0],2)))


def phase_errorfunc(p,x,z):
        return phase_lorentz(p,x)-z
"""
