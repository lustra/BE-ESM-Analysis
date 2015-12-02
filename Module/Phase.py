# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
import matplotlib.pyplot as plt


epsilon = 20  # TODO


def phase_ermitteln(phase_freq, resfreq, versatz, filter_fkt):
    """
    :param phase_freq: Phase in Abhängigkeit der Frequenz in Grad
    :type phase_freq: numpy.multiarray.ndarray
    :param resfreq: Index der Resonanzfrequenz (ohne Versatz)
    :type resfreq: int
    :type versatz: int
    :type filter_fkt: (self: Module.Abstrakt.Fit.Fit, numpy.multiarray.ndarray) -> numpy.multiarray.ndarray
    :return: Phase neben der Resonanzfrequenz, wobei Phasensprünge jenseits der Resonanzfrequenz entfernt wurden
    """

    plt.plot(range(len(phase_freq)), filter_fkt(phase_freq), '.', label='Oh!')
    plt.ylabel('PHASE')
    plt.xlabel('INDEX')
    plt.show()


    phase_null = phase_freq[resfreq]
    phase_freq -= phase_null

    """
    Betrachten kleinen Bereich jenseits der Resonanzfrequenz zur Bestimmung der Phasenlage. Die Phase rauscht hier
    möglichst noch nicht über +/- 90°. Aber kleine Fehler im Amplitudenfit wirken sich hingegen durch größere Bereiche
    weniger stark aus.
    """
    if np.median(phase_freq[resfreq:resfreq+epsilon]) > 0:
        phase_freq[resfreq:] = positiv(phase_freq[resfreq:])
        phase_freq[:resfreq] = negativ(phase_freq[:resfreq])
    else:  # Für den Fall 0 streng genommen undefiniert (hier raten)
        phase_freq[resfreq:] = negativ(phase_freq[resfreq:])
        phase_freq[:resfreq] = positiv(phase_freq[:resfreq])

    resfreq = max(min(resfreq + versatz, len(phase_freq)-1), 0)  # Bereichsüberschreitung verhindern


    plt.plot(range(len(phase_freq)), filter_fkt(phase_freq), '.', label='Oh!')
    plt.ylabel('PHASE')
    plt.xlabel('INDEX')
    plt.show()


    return filter_fkt(phase_freq)[resfreq]


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
