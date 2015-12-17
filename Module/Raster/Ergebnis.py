# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
from netCDF4 import Dataset


class Ergebnis:
    def __init__(self, resfreq, amp, q, phase):
        """
        :type resfreq: FitWerte
        :type amp: FitWerte
        :type q: FitWerte
        :type phase: FitWerte
        """
        self.resfreq = resfreq
        self.amp = amp
        self.q = q
        self.phase = phase

    def speichern(self, wohin):
        """
        :type wohin: str
        """
        nc = DatasetPlus(wohin, len(self.resfreq.normal))

        nc.grp(self.resfreq.normal, "resfreq")
        nc.grp(self.amp.normal, "damp")
        nc.grp(self.q.normal, "q")
        nc.grp(self.phase.normal, "phase")

        nc.grp(self.resfreq.fehler, "resfreq_fehler")
        nc.grp(self.amp.fehler, "damp_fehler")
        nc.grp(self.q.fehler, "q_fehler")
        nc.grp(self.phase.fehler, "phase_fehler")

        nc.grp(self.resfreq.fehler_prozent, "resfreq_fehler_prozent")
        nc.grp(self.amp.fehler_prozent, "damp_fehler_prozent")
        nc.grp(self.q.fehler_prozent, "q_fehler_prozent")
        nc.grp(self.phase.fehler_prozent, "phase_fehler_prozent")

        nc.close()


class DatasetPlus(Dataset):
    def __init__(self, pfad, pixel):
        """
        :type pfad: str
        :type pixel: int
        """
        Dataset.__init__(self, pfad, 'w')
        self.pixel = pixel
        self.createDimension('x', self.pixel),
        self.createDimension('y', self.pixel)

    def grp(self, werte, name):
        """
        :type werte: numpy.multiarray.ndarray
        :type name: str
        """
        grp = self.createGroup(name)
        dat = grp.createVariable(
            varname=name,
            datatype=np.int32,
            dimensions=('x', 'y'),
            zlib=True,  # Komprimieren
            fletcher32=True  # mit Prüfsumme
        )
        dat[:] = werte
        # np.int32(((data_out+abs(data_out.min()))/(data_out.max()-data_out.min()))*(np.power(2,31)-1))


class FitWerte:
    def __init__(self, normal, fehler):
        """
        :type normal: numpy.multiarray.ndarray
        :type fehler: numpy.multiarray.ndarray
        """
        self.normal = normal

        self.fehler = fehler
        # Fehlerangaben in Prozent
        self.fehler_prozent = fehler * 100 / normal

        self.normal_min = normal.min()
        self.normal_max = normal.max()
        self.fehler_min = fehler.min()
        self.fehler_max = fehler.max()
