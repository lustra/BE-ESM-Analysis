# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dokumente/BE-ESM-Analysis/Design/SpektrLaden.ui'
#
# Created: Mon Nov 30 13:37:03 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SpektrLaden(object):
    def setupUi(self, SpektrLaden):
        SpektrLaden.setObjectName(_fromUtf8("SpektrLaden"))
        SpektrLaden.resize(964, 445)
        self.centralwidget = QtGui.QWidget(SpektrLaden)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 947, 425))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticallayout = QtGui.QVBoxLayout()
        self.verticallayout.setObjectName(_fromUtf8("verticallayout"))
        self.horizontallayout2 = QtGui.QHBoxLayout()
        self.horizontallayout2.setObjectName(_fromUtf8("horizontallayout2"))
        self.edit_pfad = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.edit_pfad.setText(_fromUtf8(""))
        self.edit_pfad.setObjectName(_fromUtf8("edit_pfad"))
        self.horizontallayout2.addWidget(self.edit_pfad)
        self.button_aendern = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.button_aendern.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_aendern.sizePolicy().hasHeightForWidth())
        self.button_aendern.setSizePolicy(sizePolicy)
        self.button_aendern.setObjectName(_fromUtf8("button_aendern"))
        self.horizontallayout2.addWidget(self.button_aendern)
        self.verticallayout.addLayout(self.horizontallayout2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticallayout.addItem(spacerItem)
        self.button_konfig = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.button_konfig.setObjectName(_fromUtf8("button_konfig"))
        self.verticallayout.addWidget(self.button_konfig)
        self.horizontallayout1 = QtGui.QHBoxLayout()
        self.horizontallayout1.setObjectName(_fromUtf8("horizontallayout1"))
        self.gridlayout0 = QtGui.QGridLayout()
        self.gridlayout0.setObjectName(_fromUtf8("gridlayout0"))
        self.box_df = QtGui.QSpinBox(self.horizontalLayoutWidget)
        self.box_df.setStyleSheet(_fromUtf8(""))
        self.box_df.setMinimum(1)
        self.box_df.setMaximum(9999)
        self.box_df.setProperty("value", 1)
        self.box_df.setObjectName(_fromUtf8("box_df"))
        self.gridlayout0.addWidget(self.box_df, 0, 1, 1, 1)
        self.label_mittelungen = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_mittelungen.setObjectName(_fromUtf8("label_mittelungen"))
        self.gridlayout0.addWidget(self.label_mittelungen, 1, 0, 1, 1)
        self.box_mittelungen = QtGui.QSpinBox(self.horizontalLayoutWidget)
        self.box_mittelungen.setStyleSheet(_fromUtf8(""))
        self.box_mittelungen.setMinimum(1)
        self.box_mittelungen.setMaximum(9999)
        self.box_mittelungen.setProperty("value", 1)
        self.box_mittelungen.setObjectName(_fromUtf8("box_mittelungen"))
        self.gridlayout0.addWidget(self.box_mittelungen, 1, 1, 1, 1)
        self.label_df = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_df.setObjectName(_fromUtf8("label_df"))
        self.gridlayout0.addWidget(self.label_df, 0, 0, 1, 1)
        self.horizontallayout1.addLayout(self.gridlayout0)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontallayout1.addItem(spacerItem1)
        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.label_fmin = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_fmin.setObjectName(_fromUtf8("label_fmin"))
        self.gridlayout1.addWidget(self.label_fmin, 0, 0, 1, 1)
        self.label_fmax = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_fmax.setObjectName(_fromUtf8("label_fmax"))
        self.gridlayout1.addWidget(self.label_fmax, 1, 0, 1, 1)
        self.box_fmin = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_fmin.setDecimals(3)
        self.box_fmin.setMaximum(999.0)
        self.box_fmin.setSingleStep(0.5)
        self.box_fmin.setObjectName(_fromUtf8("box_fmin"))
        self.gridlayout1.addWidget(self.box_fmin, 0, 1, 1, 1)
        self.box_fmax = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_fmax.setDecimals(3)
        self.box_fmax.setMinimum(0.5)
        self.box_fmax.setMaximum(999.0)
        self.box_fmax.setSingleStep(0.5)
        self.box_fmax.setObjectName(_fromUtf8("box_fmax"))
        self.gridlayout1.addWidget(self.box_fmax, 1, 1, 1, 1)
        self.horizontallayout1.addLayout(self.gridlayout1)
        self.verticallayout.addLayout(self.horizontallayout1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticallayout.addItem(spacerItem2)
        self.line = QtGui.QFrame(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticallayout.addWidget(self.line)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticallayout.addItem(spacerItem3)
        self.horizontallayout4 = QtGui.QHBoxLayout()
        self.horizontallayout4.setObjectName(_fromUtf8("horizontallayout4"))
        self.label_methode = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_methode.sizePolicy().hasHeightForWidth())
        self.label_methode.setSizePolicy(sizePolicy)
        self.label_methode.setObjectName(_fromUtf8("label_methode"))
        self.horizontallayout4.addWidget(self.label_methode)
        self.box_methode = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.box_methode.setObjectName(_fromUtf8("box_methode"))
        self.box_methode.addItem(_fromUtf8(""))
        self.box_methode.addItem(_fromUtf8(""))
        self.box_methode.addItem(_fromUtf8(""))
        self.horizontallayout4.addWidget(self.box_methode)
        self.verticallayout.addLayout(self.horizontallayout4)
        self.label_bereich = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_bereich.setObjectName(_fromUtf8("label_bereich"))
        self.verticallayout.addWidget(self.label_bereich)
        self.horizontallayout3 = QtGui.QHBoxLayout()
        self.horizontallayout3.setObjectName(_fromUtf8("horizontallayout3"))
        self.label_bereich_links = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_bereich_links.sizePolicy().hasHeightForWidth())
        self.label_bereich_links.setSizePolicy(sizePolicy)
        self.label_bereich_links.setObjectName(_fromUtf8("label_bereich_links"))
        self.horizontallayout3.addWidget(self.label_bereich_links)
        self.box_bereich_links = QtGui.QSpinBox(self.horizontalLayoutWidget)
        self.box_bereich_links.setMaximum(999999999)
        self.box_bereich_links.setObjectName(_fromUtf8("box_bereich_links"))
        self.horizontallayout3.addWidget(self.box_bereich_links)
        self.label_bereich_rechts = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_bereich_rechts.sizePolicy().hasHeightForWidth())
        self.label_bereich_rechts.setSizePolicy(sizePolicy)
        self.label_bereich_rechts.setObjectName(_fromUtf8("label_bereich_rechts"))
        self.horizontallayout3.addWidget(self.label_bereich_rechts)
        self.box_bereich_rechts = QtGui.QSpinBox(self.horizontalLayoutWidget)
        self.box_bereich_rechts.setMinimum(-999999999)
        self.box_bereich_rechts.setMaximum(0)
        self.box_bereich_rechts.setObjectName(_fromUtf8("box_bereich_rechts"))
        self.horizontallayout3.addWidget(self.box_bereich_rechts)
        self.verticallayout.addLayout(self.horizontallayout3)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticallayout.addItem(spacerItem4)
        self.label_fitparameter = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_fitparameter.setObjectName(_fromUtf8("label_fitparameter"))
        self.verticallayout.addWidget(self.label_fitparameter)
        self.horizontallayout5 = QtGui.QHBoxLayout()
        self.horizontallayout5.setObjectName(_fromUtf8("horizontallayout5"))
        self.label_amp_min = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_amp_min.sizePolicy().hasHeightForWidth())
        self.label_amp_min.setSizePolicy(sizePolicy)
        self.label_amp_min.setObjectName(_fromUtf8("label_amp_min"))
        self.horizontallayout5.addWidget(self.label_amp_min)
        self.box_amp_min = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_amp_min.setDecimals(6)
        self.box_amp_min.setProperty("value", 1e-05)
        self.box_amp_min.setObjectName(_fromUtf8("box_amp_min"))
        self.horizontallayout5.addWidget(self.box_amp_min)
        self.label_amp_max = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_amp_max.sizePolicy().hasHeightForWidth())
        self.label_amp_max.setSizePolicy(sizePolicy)
        self.label_amp_max.setObjectName(_fromUtf8("label_amp_max"))
        self.horizontallayout5.addWidget(self.label_amp_max)
        self.box_amp_max = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_amp_max.setDecimals(6)
        self.box_amp_max.setProperty("value", 0.1)
        self.box_amp_max.setObjectName(_fromUtf8("box_amp_max"))
        self.horizontallayout5.addWidget(self.box_amp_max)
        self.verticallayout.addLayout(self.horizontallayout5)
        self.horizontallayout7 = QtGui.QHBoxLayout()
        self.horizontallayout7.setObjectName(_fromUtf8("horizontallayout7"))
        self.label_untergrund_min = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_untergrund_min.sizePolicy().hasHeightForWidth())
        self.label_untergrund_min.setSizePolicy(sizePolicy)
        self.label_untergrund_min.setObjectName(_fromUtf8("label_untergrund_min"))
        self.horizontallayout7.addWidget(self.label_untergrund_min)
        self.box_untergrund_min = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_untergrund_min.setDecimals(6)
        self.box_untergrund_min.setObjectName(_fromUtf8("box_untergrund_min"))
        self.horizontallayout7.addWidget(self.box_untergrund_min)
        self.label_untergrund_max = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_untergrund_max.sizePolicy().hasHeightForWidth())
        self.label_untergrund_max.setSizePolicy(sizePolicy)
        self.label_untergrund_max.setObjectName(_fromUtf8("label_untergrund_max"))
        self.horizontallayout7.addWidget(self.label_untergrund_max)
        self.box_untergrund_max = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_untergrund_max.setDecimals(6)
        self.box_untergrund_max.setProperty("value", 0.005)
        self.box_untergrund_max.setObjectName(_fromUtf8("box_untergrund_max"))
        self.horizontallayout7.addWidget(self.box_untergrund_max)
        self.verticallayout.addLayout(self.horizontallayout7)
        self.horizontallayout6 = QtGui.QHBoxLayout()
        self.horizontallayout6.setObjectName(_fromUtf8("horizontallayout6"))
        self.label_guete = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_guete.sizePolicy().hasHeightForWidth())
        self.label_guete.setSizePolicy(sizePolicy)
        self.label_guete.setObjectName(_fromUtf8("label_guete"))
        self.horizontallayout6.addWidget(self.label_guete)
        self.box_guete = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_guete.setProperty("value", 20.0)
        self.box_guete.setObjectName(_fromUtf8("box_guete"))
        self.horizontallayout6.addWidget(self.box_guete)
        self.label_guete_min = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_guete_min.sizePolicy().hasHeightForWidth())
        self.label_guete_min.setSizePolicy(sizePolicy)
        self.label_guete_min.setObjectName(_fromUtf8("label_guete_min"))
        self.horizontallayout6.addWidget(self.label_guete_min)
        self.box_guete_min = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_guete_min.setProperty("value", 5.0)
        self.box_guete_min.setObjectName(_fromUtf8("box_guete_min"))
        self.horizontallayout6.addWidget(self.box_guete_min)
        self.label_guete_max = QtGui.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_guete_max.sizePolicy().hasHeightForWidth())
        self.label_guete_max.setSizePolicy(sizePolicy)
        self.label_guete_max.setObjectName(_fromUtf8("label_guete_max"))
        self.horizontallayout6.addWidget(self.label_guete_max)
        self.box_guete_max = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_guete_max.setProperty("value", 25.0)
        self.box_guete_max.setObjectName(_fromUtf8("box_guete_max"))
        self.horizontallayout6.addWidget(self.box_guete_max)
        self.verticallayout.addLayout(self.horizontallayout6)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticallayout.addItem(spacerItem5)
        self.horizontallayout0 = QtGui.QHBoxLayout()
        self.horizontallayout0.setObjectName(_fromUtf8("horizontallayout0"))
        self.button_fitten = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.button_fitten.setEnabled(True)
        self.button_fitten.setObjectName(_fromUtf8("button_fitten"))
        self.horizontallayout0.addWidget(self.button_fitten)
        self.progress_bar = QtGui.QProgressBar(self.horizontalLayoutWidget)
        self.progress_bar.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_bar.sizePolicy().hasHeightForWidth())
        self.progress_bar.setSizePolicy(sizePolicy)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName(_fromUtf8("progress_bar"))
        self.horizontallayout0.addWidget(self.progress_bar)
        self.verticallayout.addLayout(self.horizontallayout0)
        self.horizontalLayout.addLayout(self.verticallayout)
        self.verticallayout1 = QtGui.QVBoxLayout()
        self.verticallayout1.setObjectName(_fromUtf8("verticallayout1"))
        self.plotter = Vorschau(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotter.sizePolicy().hasHeightForWidth())
        self.plotter.setSizePolicy(sizePolicy)
        self.plotter.setObjectName(_fromUtf8("plotter"))
        self.verticallayout1.addWidget(self.plotter)
        self.horizontallayout8 = QtGui.QHBoxLayout()
        self.horizontallayout8.setObjectName(_fromUtf8("horizontallayout8"))
        self.button_vorschau = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.button_vorschau.setCheckable(True)
        self.button_vorschau.setObjectName(_fromUtf8("button_vorschau"))
        self.horizontallayout8.addWidget(self.button_vorschau)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontallayout8.addItem(spacerItem6)
        self.label_omega = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_omega.setEnabled(False)
        self.label_omega.setObjectName(_fromUtf8("label_omega"))
        self.horizontallayout8.addWidget(self.label_omega)
        self.box_omega = QtGui.QSpinBox(self.horizontalLayoutWidget)
        self.box_omega.setEnabled(False)
        self.box_omega.setObjectName(_fromUtf8("box_omega"))
        self.horizontallayout8.addWidget(self.box_omega)
        self.label_ac = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_ac.setEnabled(False)
        self.label_ac.setObjectName(_fromUtf8("label_ac"))
        self.horizontallayout8.addWidget(self.label_ac)
        self.box_ac = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_ac.setEnabled(False)
        self.box_ac.setDecimals(6)
        self.box_ac.setMinimum(-99.999999)
        self.box_ac.setMaximum(99.999999)
        self.box_ac.setSingleStep(0.1)
        self.box_ac.setObjectName(_fromUtf8("box_ac"))
        self.horizontallayout8.addWidget(self.box_ac)
        self.label_dc = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_dc.setEnabled(False)
        self.label_dc.setObjectName(_fromUtf8("label_dc"))
        self.horizontallayout8.addWidget(self.label_dc)
        self.box_dc = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.box_dc.setEnabled(False)
        self.box_dc.setDecimals(6)
        self.box_dc.setMinimum(-99.999999)
        self.box_dc.setMaximum(99.999999)
        self.box_dc.setSingleStep(0.1)
        self.box_dc.setObjectName(_fromUtf8("box_dc"))
        self.horizontallayout8.addWidget(self.box_dc)
        self.verticallayout1.addLayout(self.horizontallayout8)
        self.horizontalLayout.addLayout(self.verticallayout1)
        SpektrLaden.setCentralWidget(self.centralwidget)

        self.retranslateUi(SpektrLaden)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.box_omega.setEnabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.box_ac.setEnabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.box_dc.setEnabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label_omega.setEnabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label_ac.setEnabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label_dc.setEnabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.box_fmax.setDisabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.box_fmin.setDisabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.box_mittelungen.setDisabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.box_df.setDisabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.button_konfig.setDisabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.button_aendern.setDisabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edit_pfad.setDisabled)
        QtCore.QObject.connect(self.button_vorschau, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.plotter.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(SpektrLaden)

    def retranslateUi(self, SpektrLaden):
        SpektrLaden.setWindowTitle(_translate("SpektrLaden", "Spektroskopie - Messung einlesen", None))
        self.button_aendern.setText(_translate("SpektrLaden", "Ändern...", None))
        self.button_konfig.setText(_translate("SpektrLaden", "Messkonfiguration aus Datei einlesen", None))
        self.label_mittelungen.setText(_translate("SpektrLaden", "Anzahl Mittelungen", None))
        self.label_df.setText(_translate("SpektrLaden", "delta f (Hz)", None))
        self.label_fmin.setText(_translate("SpektrLaden", "Freq Min (kHz)", None))
        self.label_fmax.setText(_translate("SpektrLaden", "Freq Max (kHz)", None))
        self.label_methode.setText(_translate("SpektrLaden", "Lorentzverteilung", None))
        self.box_methode.setItemText(0, _translate("SpektrLaden", "Antreibendes System", None))
        self.box_methode.setItemText(1, _translate("SpektrLaden", "Cantilever", None))
        self.box_methode.setItemText(2, _translate("SpektrLaden", "Phase", None))
        self.label_bereich.setText(_translate("SpektrLaden", "Frequenzbereich begrenzen (in Messpunkten):", None))
        self.label_bereich_links.setText(_translate("SpektrLaden", "links:", None))
        self.label_bereich_rechts.setText(_translate("SpektrLaden", "rechts:", None))
        self.label_fitparameter.setText(_translate("SpektrLaden", "Fitparameter:", None))
        self.label_amp_min.setText(_translate("SpektrLaden", "Amplitude von", None))
        self.label_amp_max.setText(_translate("SpektrLaden", "bis", None))
        self.label_untergrund_min.setText(_translate("SpektrLaden", "Untergrund von", None))
        self.label_untergrund_max.setText(_translate("SpektrLaden", "bis", None))
        self.label_guete.setText(_translate("SpektrLaden", "Güte =", None))
        self.label_guete_min.setText(_translate("SpektrLaden", "von", None))
        self.label_guete_max.setText(_translate("SpektrLaden", "bis", None))
        self.button_fitten.setText(_translate("SpektrLaden", "Fitten", None))
        self.button_vorschau.setText(_translate("SpektrLaden", "Fitvorschau anzeigen", None))
        self.label_omega.setText(_translate("SpektrLaden", "Omega:", None))
        self.label_ac.setText(_translate("SpektrLaden", "AC (V):", None))
        self.label_dc.setText(_translate("SpektrLaden", "DC (V):", None))

from Module.Spektroskopie.Vorschau import Vorschau
