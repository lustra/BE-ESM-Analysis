# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""


int_max = 2**31-1
""" Größter 32-Bit int-Wert """
int_min = -2**31
""" Kleinster 32-Bit in-Wert """


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
    :type s: str
    """
    return float(s.replace(',', '.'))
