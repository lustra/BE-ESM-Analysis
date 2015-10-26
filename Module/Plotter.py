# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Plotter(FigureCanvas):
    def __init__(self, canvas, layout, beschriftung, width=5, height=5, dpi=75):
        """
        :type canvas: Module.Canvas.Canvas
        :type layout: QtGui.QLayout
        :type beschriftung: Module.Sonstige.Achsenbeschriftung
        """
        self.canvas = canvas
        self.beschriftung = beschriftung
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111, xlabel=beschriftung.x, ylabel=beschriftung.y)
        """ @type: matplotlib.axes.Axes """
        self.axes.hold(False)
        self.colorbar = None

        FigureCanvas.__init__(self, self.figure)
        layout.addWidget(self)
        self.statusbar = canvas.statusbar

        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.updateGeometry()

        self.mpl_connect("motion_notify_event", self.maus_bewegt)

    def maus_bewegt(self, event):
        """
        :type event: matplotlib.backend_bases.MouseEvent
        """
        if event.inaxes is not None:
            self.statusbar.showMessage(
                self.canvas.str_status(event.xdata, event.ydata)
            )
        else:
            self.statusbar.clearMessage()

    def draw(self, falschfarben=None):
        if falschfarben is not None:
            if self.colorbar is None:
                self.colorbar = self.figure.colorbar(falschfarben)
                self.colorbar.set_label(self.beschriftung.farbe)
            else:
                self.colorbar.update_normal(falschfarben)
        self.axes.set_xlabel(self.beschriftung.x)
        self.axes.set_ylabel(self.beschriftung.y)
        super(Plotter, self).draw()

    # Diese abstrakte Methoden müssen implementiert werden, werden aber nicht benötigt:

    def start_event_loop(self, timeout):
        pass

    def flush_events(self):
        pass

    def stop_event_loop(self):
        pass
