# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np


def resonance_lorentz(freq, resfreq, amp, guete):
    """
    :type freq: numpy.multiarray.ndarray
    :type resfreq: numpy.multiarray.ndarray
    :type amp: numpy.multiarray.ndarray
    :type guete: numpy.multiarray.ndarray
    :return Lorentzverteilung für den Cantilever
    """
    return amp * resfreq**2 / (
        guete * np.sqrt((freq**2 - resfreq**2)**2 + (freq * resfreq / guete)**2)
    )


def drive_lorentz(freq, resfreq, amp, guete):
    """
    :type freq: numpy.multiarray.ndarray
    :type resfreq: numpy.multiarray.ndarray
    :type amp: numpy.multiarray.ndarray
    :type guete: numpy.multiarray.ndarray
    :return: Lorentzverteilung für das antreibende System
    """
    return amp * resfreq**2 / np.sqrt(
        (freq**2 - resfreq**2) ** 2 + (freq * resfreq / guete)**2
    )


def phase_lorentz(p, x):
    return np.arctan(
        (x * p[0] / p[2]) / (np.power(x, 2) - np.power(p[0], 2))
    )


def errlambda(lorentz):
    return lambda p, x, z: lorentz(p, x) - z

errorfunc = [  # Bessere Lösung finden oder Reihenfolge mit Strings abgleichen!
    errlambda(resonance_lorentz),
    errlambda(drive_lorentz),
    # errlambda(phase_lorentz) #TODO Das würde natürlich nicht funktionieren. Es muss dann auch die PHASE gefittet werden!
]
