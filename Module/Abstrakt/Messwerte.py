# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np

from Module.TDMS import lade_tdms


class Messwerte:
    def __init__(self, par):
        """
        :type par: Module.Sonstige.Parameter
        :return: Werte der Amplitude und Phase für jeden Pixel einer Messung
        """
        self.par = par
        self.amplitude, self.amplitude_namen = lade_tdms(par, "amp")
        self.phase, self.phase_namen = lade_tdms(par, "phase")

        # Definition der Frequenz:
        self.frequenzen = np.arange(
            par.fmin, par.fmax,
            float((par.fmax - par.fmin) / float(par.messpunkte))  # delta f
        )
