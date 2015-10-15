# coding=utf-8
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Plotter(FigureCanvas):
    def __init__(self, canvas, width=5, height=5, dpi=75):
        self.canvas = canvas
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(canvas.centralwidget)
        self.statusbar = canvas.statusbar

        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.updateGeometry()

        self.mpl_connect("motion_notify_event", self.maus_bewegt)

    def maus_bewegt(self, event):
        if event.inaxes is not None:
            self.statusbar.showMessage(
                self.canvas.str_status(event.xdata, event.ydata)
            )
        else:
            self.statusbar.clearMessage()

    # Diese abstrakte Methoden müssen implementiert werden, werden aber nicht benötigt:

    def start_event_loop(self, timeout):
        pass

    def flush_events(self):
        pass

    def stop_event_loop(self):
        pass
