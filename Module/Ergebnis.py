# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
from netCDF4 import Dataset


class Ergebnis:
    def __init__(self, fitparameter, error_fitparameter, sphase):
        self.resfreq = FitWerte(
            fitparameter[:, :, 0],
            error_fitparameter[:, :, 0]
        )
        self.damp = FitWerte(
            fitparameter[:, :, 1],
            error_fitparameter[:, :, 1]
        )
        self.q = FitWerte(
            fitparameter[:, :, 2],
            error_fitparameter[:, :, 2]
        )
        self.phase = FitWerte(sphase, None)

    def speichern(self, pfad):
        nc = DatasetPlus(pfad, len(self.resfreq.normal))

        nc.grp(self.damp.normal, "damp")
        nc.grp(self.q.normal, "q")
        nc.grp(self.resfreq.normal, "resfreq")
        nc.grp(self.damp.fehler, "damp_fehler")
        nc.grp(self.q.fehler, "q_fehler")
        nc.grp(self.resfreq.fehler, "resfreq_fehler")
        nc.grp(self.damp.fehler_prozent, "damp_fehler_prozent")
        nc.grp(self.q.fehler_prozent, "q_fehler_prozent")
        nc.grp(self.resfreq.fehler_prozent, "resfreq_fehler_prozent")

        nc.close()


class DatasetPlus(Dataset):
    def __init__(self, pfad, pixel):
        Dataset.__init__(self, pfad, 'w')
        self.pixel = pixel
        self.createDimension('x', self.pixel),
        self.createDimension('y', self.pixel)

    def grp(self, werte, name):
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
        self.normal = normal

        if fehler is None:  # Nur bei Phase
            self.normal_min = -180
            self.normal_max = 180
        else:  # Normal
            self.fehler = fehler
            # Fehlerangaben in Prozent
            self.fehler_prozent = fehler * 100 / normal

            self.normal_min = normal.min()
            self.normal_max = normal.max()
            self.fehler_min = fehler.min()
            self.fehler_max = fehler.max()
