# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np


def resonance_lorentz(p, x):
    """
    :param p: [Resonanzfrequenz, Drive Amplitude, Güte]
    :type p: numpy.multiarray.ndarray
    :param x: Frequenz
    :type x: numpy.multiarray.ndarray
    :return Lorentzverteilung für den Cantilever
    """
    return p[1] * p[0]**2 / (
        p[2] * np.sqrt((x**2 - p[0]**2)**2 + (x * p[0] / p[2])**2)
    )


def drive_lorentz(p, x):
    """
    :param p: [Resonanzfrequenz, Drive Amplitude, Güte]
    :type p: numpy.multiarray.ndarray
    :param x: Frequenz
    :type x: numpy.multiarray.ndarray
    :return: Lorentzverteilung für das antreibende System
    """
    return p[1] * p[0]**2 / np.sqrt(
        (x**2 - p[0]**2) ** 2 + (x * p[0] / p[2])**2
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
    errlambda(phase_lorentz) #TODO Das wird natürlich noch nicht funktionieren! Es muss dann auch die PHASE gefittet werden!
]
