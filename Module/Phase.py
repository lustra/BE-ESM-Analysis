# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import matplotlib.pyplot as plt
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

    plt.plot(range(len(phase_freq)), phase_freq, '-', label='Vorher!')
    plt.plot(range(von, bis), erg.best_fit, '-', label='Nachher!')
    plt.ylabel('PHASE')
    plt.xlabel('INDEX')
    plt.show()

    if versatz < 0:
        return erg.best_fit[0]
    elif versatz > 0:
        return erg.best_fit[-1]
    else:
        return erg.best_fit[(bis - von) // 2]


def positiv(alt):
    """
    :type alt: numpy.multiarray.ndarray
    """
    # Bei Phasen kleiner 0° umklappen auf positiven Ast
    return [ph if ph > 0 else ph + 180 for ph in alt]


def negativ(alt):
    """
    :type alt: numpy.multiarray.ndarray
    """
    # Umklappen auf negativen Ast für Phasen größer 0°
    return [ph if ph < 0 else ph - 180 for ph in alt]
