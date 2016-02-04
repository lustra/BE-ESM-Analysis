# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4.QtCore import QRunnable, QThreadPool


class Parallel(QRunnable):
    def __init__(self, fkt, p):
        """
        :type fkt: ()->
        :type p: object
        """
        QRunnable.__init__(self)
        self.fkt = fkt
        self.p = p

    def run(self):
        self.fkt(self.p)


def omap(fkt, par):
    """
    :type fkt: ()->
    :type par: list
    :rtype: list
    """
    # Die Anzahl der Prozesse ist ohne Aufwand auf einen idealen Wert beschränkt
    pool = QThreadPool()
    erg = [None] * len(par)
    for p in par:
        pool.start(QRunnable(fkt, p))
