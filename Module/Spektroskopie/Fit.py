# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np
from glob import glob

from Module.Abstrakt.Fit import Fit as AbstraktFit
from Module.Spektroskopie.Messwerte import Messwerte
from Module.Ergebnis import Ergebnis
from Module.Signal import signal


class Fit(AbstraktFit):
    """ Der parallelisierte Fit """
    def __init__(self, laden, par):
        """
        :type laden: Module.Spektroskopie.Laden.GuiSpektrLaden
        :type par: Module.Spektroskopie.Parameter.Parameter
        """
        AbstraktFit.__init__(self, laden, par)
        self.messwerte = None
        """ @type: Module.Spektroskopie.Messwerte.Messwerte """

    def impl_fit(self):
        erg_amp = []
        erg_freq = []
        erg_phase = []
        erg_offsets = []

        dateien = glob(self.par.verzeichnis + 'amp' + str(self.par.omega) + '*.tdms')
        for datei in dateien:
            amps = []
            freqs = []
            phase = []
            offsets = []

            out, ph, datx, daty = fit_datei(datei, par)

            amps.append(out.best_values["amp"])
            freqs.append(out.best_values["resfreq"])
            phase.append(ph)
            offsets.append(float(name.split('G')[-1].split('V')[0].replace(',', '.')))

            erg_amp.append(np.array(amps))
            erg_freq.append(np.array(freqs))
            erg_phase.append(np.array(phase))
            erg_offsets.append(np.array(offsets))

        self.emit(signal.weiter)

        self.erg = Ergebnis(fitparameter, error_fitparameter, sphase)

        self.av_iter = int(np.average(iterationen))

    def lade_messwerte(self):
        self.messwerte = Messwerte(self.par)
