# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from lmfit import Parameters, Model
from lmfit.model import ModelResult

from FitFunktion import phase_lorentz, phase_phenom


def phase_ermitteln(phase_freq, resfreq, versatz, modus, savgol=None):
    """
    :param phase_freq: Phase in Abhängigkeit der Frequenz in Grad
    :type phase_freq: numpy.multiarray.ndarray
    :param resfreq: Index der Resonanzfrequenz (ohne Versatz)
    :type resfreq: int
    :type versatz: int
    :param modus: 0=Lorentz, 1=atan(phi), 2=Messwerte
    :type modus: int
    :param savgol: Filter zum Glätten der Messwerte (nur bei Modus 2)
    :type savgol: (self: Module.Abstrakt.Fit, numpy.multiarray.ndarray) -> numpy.multiarray.ndarray
    :return: Gefittete oder geglättete Phase im Bereich um Resonanzfrequenz +/- Versatz
    :rtype: ModelResult
    """
    von = max(resfreq - abs(versatz), 0)
    bis = max(min(resfreq + abs(versatz), len(phase_freq)-1), von+1)

    def phase_fitten(funktion):
        # Fitparameter für die Fitfunktion
        params = Parameters()
        params.add('resfreq', value=resfreq, min=von, max=bis)
        params.add('guete', value=1, min=-10000, max=10000)
        params.add('off', value=0, min=-180, max=180)

        mod = Model(funktion)
        return mod.fit(
            data=phase_freq[von:bis],
            freq=range(von, bis),
            params=params
        )

    def phase_direkt():
        direkt = ModelResult(Model(None), Parameters())
        direkt.best_fit = savgol(phase_freq[von:bis])
        return direkt

    erg = [
        lambda: phase_fitten(phase_lorentz),
        lambda: phase_fitten(phase_phenom),
        phase_direkt
    ][modus]()

    erg.von = von
    erg.bis = bis
    return erg
