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
