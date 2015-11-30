# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""


class Messwerte:
    def __init__(self, par):
        """
        :type par: Module.Raster.Parameter.Parameter
        """
        self.par = par
        self.amplitude_namen = []
        self.phase_namen = []
