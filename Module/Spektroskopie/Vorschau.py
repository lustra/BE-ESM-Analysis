# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from ResonanzFit import lang
from Module.Plotter import Plotter
from Module.Sonstige import Achsenbeschriftung
from Module.Strings import *


# noinspection PyAbstractClass
class Vorschau(Plotter):
    def __init__(self, gui):
        """
        :type gui:
        """
        Plotter.__init__(self, gui, Achsenbeschriftung(spektr_dc[lang], spektr_amp[lang]))
