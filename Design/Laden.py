# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dokumente/Studium/Master/BE-ESM-Analysis/Design/Laden.ui'
#
# Created: Sat Oct 17 18:23:17 2015
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

class Ui_Laden(object):
    def setupUi(self, Laden):
        Laden.setObjectName(_fromUtf8("Laden"))
        Laden.resize(388, 322)
        self.centralwidget = QtGui.QWidget(Laden)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 371, 305))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticallayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticallayout.setMargin(0)
        self.verticallayout.setObjectName(_fromUtf8("verticallayout"))
        self.horizontallayout2 = QtGui.QHBoxLayout()
        self.horizontallayout2.setObjectName(_fromUtf8("horizontallayout2"))
        self.edit_pfad = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.edit_pfad.setText(_fromUtf8(""))
        self.edit_pfad.setObjectName(_fromUtf8("edit_pfad"))
        self.horizontallayout2.addWidget(self.edit_pfad)
        self.button_aendern = QtGui.QPushButton(self.verticalLayoutWidget)
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
        self.check_konfig = QtGui.QPushButton(self.verticalLayoutWidget)
        self.check_konfig.setEnabled(False)
        self.check_konfig.setCheckable(True)
        self.check_konfig.setObjectName(_fromUtf8("check_konfig"))
        self.verticallayout.addWidget(self.check_konfig)
        self.horizontallayout1 = QtGui.QHBoxLayout()
        self.horizontallayout1.setObjectName(_fromUtf8("horizontallayout1"))
        self.gridlayout0 = QtGui.QGridLayout()
        self.gridlayout0.setObjectName(_fromUtf8("gridlayout0"))
        self.box_pixel = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.box_pixel.setStyleSheet(_fromUtf8(""))
        self.box_pixel.setMinimum(1)
        self.box_pixel.setMaximum(9999)
        self.box_pixel.setProperty("value", 1)
        self.box_pixel.setObjectName(_fromUtf8("box_pixel"))
        self.gridlayout0.addWidget(self.box_pixel, 0, 1, 1, 1)
        self.label_messpunkte = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_messpunkte.setObjectName(_fromUtf8("label_messpunkte"))
        self.gridlayout0.addWidget(self.label_messpunkte, 1, 0, 1, 1)
        self.box_messpunkte = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.box_messpunkte.setStyleSheet(_fromUtf8(""))
        self.box_messpunkte.setMinimum(1)
        self.box_messpunkte.setMaximum(9999)
        self.box_messpunkte.setProperty("value", 1)
        self.box_messpunkte.setObjectName(_fromUtf8("box_messpunkte"))
        self.gridlayout0.addWidget(self.box_messpunkte, 1, 1, 1, 1)
        self.label_pixel = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_pixel.setObjectName(_fromUtf8("label_pixel"))
        self.gridlayout0.addWidget(self.label_pixel, 0, 0, 1, 1)
        self.horizontallayout1.addLayout(self.gridlayout0)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontallayout1.addItem(spacerItem1)
        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.label_fmin = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_fmin.setObjectName(_fromUtf8("label_fmin"))
        self.gridlayout1.addWidget(self.label_fmin, 0, 0, 1, 1)
        self.label_fmax = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_fmax.setObjectName(_fromUtf8("label_fmax"))
        self.gridlayout1.addWidget(self.label_fmax, 1, 0, 1, 1)
        self.box_fmin = QtGui.QDoubleSpinBox(self.verticalLayoutWidget)
        self.box_fmin.setDecimals(3)
        self.box_fmin.setSingleStep(0.5)
        self.box_fmin.setObjectName(_fromUtf8("box_fmin"))
        self.gridlayout1.addWidget(self.box_fmin, 0, 1, 1, 1)
        self.box_fmax = QtGui.QDoubleSpinBox(self.verticalLayoutWidget)
        self.box_fmax.setDecimals(3)
        self.box_fmax.setMinimum(0.5)
        self.box_fmax.setMaximum(999.0)
        self.box_fmax.setSingleStep(0.5)
        self.box_fmax.setObjectName(_fromUtf8("box_fmax"))
        self.gridlayout1.addWidget(self.box_fmax, 1, 1, 1, 1)
        self.horizontallayout1.addLayout(self.gridlayout1)
        self.verticallayout.addLayout(self.horizontallayout1)
        self.line = QtGui.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticallayout.addWidget(self.line)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticallayout.addItem(spacerItem2)
        self.horizontallayout4 = QtGui.QHBoxLayout()
        self.horizontallayout4.setObjectName(_fromUtf8("horizontallayout4"))
        self.label_methode = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_methode.sizePolicy().hasHeightForWidth())
        self.label_methode.setSizePolicy(sizePolicy)
        self.label_methode.setObjectName(_fromUtf8("label_methode"))
        self.horizontallayout4.addWidget(self.label_methode)
        self.box_methode = QtGui.QComboBox(self.verticalLayoutWidget)
        self.box_methode.setObjectName(_fromUtf8("box_methode"))
        self.box_methode.addItem(_fromUtf8(""))
        self.box_methode.addItem(_fromUtf8(""))
        self.box_methode.addItem(_fromUtf8(""))
        self.horizontallayout4.addWidget(self.box_methode)
        self.verticallayout.addLayout(self.horizontallayout4)
        self.label_savgol = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_savgol.setObjectName(_fromUtf8("label_savgol"))
        self.verticallayout.addWidget(self.label_savgol)
        self.horizontallayout3 = QtGui.QHBoxLayout()
        self.horizontallayout3.setObjectName(_fromUtf8("horizontallayout3"))
        self.label_fenster = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_fenster.setObjectName(_fromUtf8("label_fenster"))
        self.horizontallayout3.addWidget(self.label_fenster)
        self.box_fenster = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.box_fenster.setMinimum(1)
        self.box_fenster.setProperty("value", 15)
        self.box_fenster.setObjectName(_fromUtf8("box_fenster"))
        self.horizontallayout3.addWidget(self.box_fenster)
        self.label_ordnung = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_ordnung.setObjectName(_fromUtf8("label_ordnung"))
        self.horizontallayout3.addWidget(self.label_ordnung)
        self.box_ordnung = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.box_ordnung.setMinimum(1)
        self.box_ordnung.setProperty("value", 3)
        self.box_ordnung.setObjectName(_fromUtf8("box_ordnung"))
        self.horizontallayout3.addWidget(self.box_ordnung)
        self.verticallayout.addLayout(self.horizontallayout3)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticallayout.addItem(spacerItem3)
        self.horizontallayout0 = QtGui.QHBoxLayout()
        self.horizontallayout0.setObjectName(_fromUtf8("horizontallayout0"))
        self.button_fitten = QtGui.QPushButton(self.verticalLayoutWidget)
        self.button_fitten.setEnabled(True)
        self.button_fitten.setObjectName(_fromUtf8("button_fitten"))
        self.horizontallayout0.addWidget(self.button_fitten)
        self.progress_bar = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.progress_bar.setEnabled(True)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName(_fromUtf8("progress_bar"))
        self.horizontallayout0.addWidget(self.progress_bar)
        self.verticallayout.addLayout(self.horizontallayout0)
        Laden.setCentralWidget(self.centralwidget)

        self.retranslateUi(Laden)
        QtCore.QMetaObject.connectSlotsByName(Laden)

    def retranslateUi(self, Laden):
        Laden.setWindowTitle(_translate("Laden", "Resonanz Fit - Messung einlesen", None))
        self.button_aendern.setText(_translate("Laden", "Ändern...", None))
        self.check_konfig.setText(_translate("Laden", "Messkonfiguration aus Datei einlesen", None))
        self.label_messpunkte.setText(_translate("Laden", "Messpunkte pro Pixel", None))
        self.label_pixel.setText(_translate("Laden", "Pixel", None))
        self.label_fmin.setText(_translate("Laden", "Freq Min (kHz)", None))
        self.label_fmax.setText(_translate("Laden", "Freq Max (kHz)", None))
        self.label_methode.setText(_translate("Laden", "Lorentzverteilung", None))
        self.box_methode.setItemText(0, _translate("Laden", "Antreibendes System", None))
        self.box_methode.setItemText(1, _translate("Laden", "Cantilever", None))
        self.box_methode.setItemText(2, _translate("Laden", "Phase", None))
        self.label_savgol.setText(_translate("Laden", "Savitzky-Golay-Filter:", None))
        self.label_fenster.setText(_translate("Laden", "Koeffizientenanzahl", None))
        self.label_ordnung.setText(_translate("Laden", "Ordnung des Polynoms", None))
        self.button_fitten.setText(_translate("Laden", "Fitten", None))

