# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np

from ResonanzFit import lang
from Module.Abstrakt.Messwerte import Messwerte as AbstraktMesswerte
from Module.Sonstige import Fehler
from Module.Strings import *


class Messwerte(AbstraktMesswerte):
    def __init__(self, par):
        """
        :type par: Module.Sonstige.Parameter
        """
        AbstraktMesswerte.__init__(self, par)
        if par.pixel != len(self.amplitude[0]) / par.messpunkte:
            raise Fehler(mw_pixelzahl[lang])

    def amplituden(self, y):
        """
        :type y: numpy.multiarray.ndarray
        """
        return split_list(
            np.array(np.multiply(self.amplitude[y], 100), dtype=np.double),
            wanted_parts=self.par.pixel
        )

    def phasen(self, y):
        """
        :type y: numpy.multiarray.ndarray
        """
        return split_list(
            np.array(self.phase[y], dtype=np.double),
            wanted_parts=self.par.pixel
        )


def split_list(alist, wanted_parts=1):
    """
    :type alist: numpy.multiarray.ndarray
    """
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]
