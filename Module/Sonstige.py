# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""


class Achsenbeschriftung:
    def __init__(self, x, y, farbe=None):
        """
        :type x: str
        :type y: str
        :type farbe: str
        """
        self.x = x
        self.y = y
        self.farbe = farbe


class Fehler(Exception):
    pass


def komma(f):
    """
    :type f: float
    """
    return str("{:.6f}".format(f)).replace('.', ',')


def punkt(s):
    """
    :param s: str
    """
    return float(s.replace(',', '.'))
