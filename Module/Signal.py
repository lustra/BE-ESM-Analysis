# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4.QtCore import SIGNAL


class Signal:
    def __init__(self):
        self.importiert = SIGNAL("importiert")  # Messwerte eingelesen -> in Spalten anzeigen
        self.fehler = SIGNAL("fehler")  # Ein Fehler ist aufgetreten -> anzeigen
        self.weiter = SIGNAL("weiter")  # Eine Zeile im Pixelraster wurde gefittet -> Fortschrittsbalken
        self.fertig = SIGNAL("fertig")  # Fitprozess vollständig beendet -> Lade-UI verbergen
signal = Signal()
