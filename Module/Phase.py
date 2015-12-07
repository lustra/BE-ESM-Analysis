# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from lmfit import Parameters, Model

from FitFunktion import phase_lorentz, phase_phenom


def phase_ermitteln(phase_freq, resfreq, versatz):
    """
    :param phase_freq: Phase in Abhängigkeit der Frequenz in Grad
    :type phase_freq: numpy.multiarray.ndarray
    :param resfreq: Index der Resonanzfrequenz (ohne Versatz)
    :type resfreq: int
    :type versatz: int
    :return: Phase neben der Resonanzfrequenz, wobei Phasensprünge jenseits der Resonanzfrequenz entfernt wurden
    """
    von = max(resfreq - abs(versatz), 0)
    bis = min(resfreq + abs(versatz), len(phase_freq)-1)

    # Fitparameter für die Fitfunktion
    params = Parameters()
    params.add('resfreq', value=resfreq, min=von, max=bis)
    params.add('guete', value=1, min=-10000, max=10000)
    params.add('off', value=0, min=-180, max=180)

    mod = Model(phase_phenom)  # phase_lorentz
    erg = mod.fit(
        data=phase_freq[von:bis],
        freq=range(von, bis),
        params=params
    )

    erg.von = von
    erg.bis = bis

    return erg
