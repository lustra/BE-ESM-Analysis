# coding=utf-8
"""
@author: Valon Lushta
@author: Sebastian Badur
"""

from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# noinspection PyAbstractClass
class Plotter(FigureCanvas):
    def __init__(self, canvas, beschriftung, width=5, height=5, dpi=75):
        """
        :type canvas: [Module.Canvas.Canvas | QtGui.QWidget]
        :type beschriftung: Module.Sonstige.Achsenbeschriftung
        :type width: int
        :type height: int
        :type dpi: int
        """
        self.canvas = canvas
        self.beschriftung = beschriftung
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111, xlabel=beschriftung.x, ylabel=beschriftung.y)
        """ :type: matplotlib.axes.Axes """
        self.axes.hold(False)
        self.colorbar = None

        FigureCanvas.__init__(self, self.figure)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.updateGeometry()

        try:  # QWidget ohne Statusleiste
            self.statusbar = canvas.statusbar
            self.mpl_connect("motion_notify_event", self.maus_bewegt)
        except AttributeError:
            pass

    def maus_bewegt(self, event):
        """
        :type event: matplotlib.backend_bases.MouseEvent
        """
        if event.inaxes is not None:
            canvas = self.canvas  # Das ist nur sinnvoll für ein Canvas
            """ :type: Module.Canvas.Canvas """
            self.statusbar.showMessage(
                canvas.str_status(event.xdata, event.ydata)
            )
        else:
            self.statusbar.clearMessage()

    def mit_skala(self, plot):
        """
        :type plot: matplotlib.image.AxesImage
        """
        if self.colorbar is None:
            self.colorbar = self.figure.colorbar(plot)
            self.colorbar.set_label(self.beschriftung.farbe)
        else:
            self.colorbar.update_normal(plot)
        self.draw()

    def draw(self):
        self.axes.set_xlabel(self.beschriftung.x)
        self.axes.set_ylabel(self.beschriftung.y)
        super(Plotter, self).draw()
