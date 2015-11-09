# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

import numpy as np

from Module.Abstrakt.Fit import Fit as AbstraktFit
from Module.Ergebnis import Ergebnis
from Module.Signal import signal


class Fit(AbstraktFit):
    def impl_fit(self):

        for j in folders:
            amps = []
            offsets = []
            freqs = []
            datax=[]
            datay=[]
            xdaten = []
            ydaten = []
            datax,datay,sorted_fnames = read_tdmsfile(j)
            xdaten,ydaten = merge_append(datax,datay,sorted_fnames)
            for i in range(len(sorted_fnames)):
                # pars=mod.guess(ydaten[i],x=xdaten[i])
                # out  = mod.fit(ydaten[i], pars, x=xdaten[i])
                out = mod.fit(ydaten[i], freq=xdaten[i], resfreq=77000, amp=5, guete=10, verbose=False)
                amps.append(out.best_values["amp"])
                freqs.append(out.best_values["resfreq"])
                offsets.append(float(sorted_fnames[i].split('/')[-1].split('.')[0].replace(',', '.')))

                if i in [10, 52, 66, 70, 72, 74]:  # Besonders problematische Fits in Messung b (kommt zuerst)
                    plt.plot(xdaten[i], ydaten[i])
                    plt.plot(xdaten[i], out.best_fit, 'r')
                    plt.show()

                self.emit(signal.weiter)

            erg_amp.append(np.array(amps))
            erg_freq.append(np.array(freqs))

        # Fitprozess abschließen ##########
        self.erg = Ergebnis(fitparameter, error_fitparameter, sphase)

        self.av_iter = int(np.average(iterationen))
