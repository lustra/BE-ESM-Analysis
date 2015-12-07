# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np


in_grad = 180 / np.pi


def resonance_lorentz(freq, resfreq, amp, guete, off):
    """
    :type freq: float
    :type resfreq: float
    :type amp: float
    :type guete: float
    :type off: float
    :return: Lorentzverteilung für den Cantilever
    :rtype: float
    """
    return amp * resfreq**2 / (
        guete * np.sqrt((freq**2 - resfreq**2)**2 + (freq * resfreq / guete)**2)
    ) + off


def drive_lorentz(freq, resfreq, amp, guete, off):
    """
    :type freq: float
    :type resfreq: float
    :type amp: float
    :type guete: float
    :type off: float
    :return: Lorentzverteilung für das antreibende System
    :rtype: float
    """
    return amp * resfreq**2 / np.sqrt(
        (freq**2 - resfreq**2) ** 2 + (freq * resfreq / guete)**2
    ) + off


def phase_lorentz(freq, resfreq, guete, off):
    """
    :type freq: float
    :type resfreq: float
    :type guete: float
    :type off: float
    :return: Phase in Grad (antreibendes System)
    :rtype: float
    """
    return in_grad * np.arctan(
        resfreq * freq / (guete * (resfreq**2 - freq**2))
    ) + off


def phase_phenom(freq, resfreq, guete, off):
    """
    :type freq: float
    :type resfreq: float
    :type guete: float
    :type off: float
    :return: Phase in Grad (antreibendes System)
    :rtype: float
    """
    return (in_grad * np.arctan(
        guete * (freq - resfreq)
    ) + 180) % 360 - 180 + off


errorfunc = [  # Bessere Lösung finden oder Reihenfolge mit Strings abgleichen!
    resonance_lorentz,
    drive_lorentz
]
