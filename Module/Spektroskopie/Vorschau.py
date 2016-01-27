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
        :type gui: PyQt4.QtGui.QWidget
        """
        Plotter.__init__(self, gui, Achsenbeschriftung(achse_freq[lang], achse_amp[lang]))
