# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dokumente/BE-ESM-Analysis/Design/Gui.ui'
#
# Created: Mon Oct 26 12:02:03 2015
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

class Ui_Gui(object):
    def setupUi(self, Gui):
        Gui.setObjectName(_fromUtf8("Gui"))
        Gui.resize(429, 424)
        self.centralwidget = QtGui.QWidget(Gui)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 411, 391))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticallayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticallayout.setMargin(0)
        self.verticallayout.setObjectName(_fromUtf8("verticallayout"))
        self.label_name = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_name.setText(_fromUtf8(""))
        self.label_name.setObjectName(_fromUtf8("label_name"))
        self.verticallayout.addWidget(self.label_name)
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.label_amplitude = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_amplitude.setObjectName(_fromUtf8("label_amplitude"))
        self.gridlayout.addWidget(self.label_amplitude, 0, 0, 1, 1)
        self.label_phase = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_phase.setObjectName(_fromUtf8("label_phase"))
        self.gridlayout.addWidget(self.label_phase, 0, 1, 1, 1)
        self.list_amplitude = QtGui.QListView(self.verticalLayoutWidget)
        self.list_amplitude.setUniformItemSizes(True)
        self.list_amplitude.setObjectName(_fromUtf8("list_amplitude"))
        self.gridlayout.addWidget(self.list_amplitude, 1, 0, 1, 1)
        self.list_phase = QtGui.QListView(self.verticalLayoutWidget)
        self.list_phase.setUniformItemSizes(True)
        self.list_phase.setObjectName(_fromUtf8("list_phase"))
        self.gridlayout.addWidget(self.list_phase, 1, 1, 1, 1)
        self.verticallayout.addLayout(self.gridlayout)
        Gui.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Gui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 429, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_messung = QtGui.QMenu(self.menubar)
        self.menu_messung.setObjectName(_fromUtf8("menu_messung"))
        self.menu_ansicht = QtGui.QMenu(self.menubar)
        self.menu_ansicht.setObjectName(_fromUtf8("menu_ansicht"))
        Gui.setMenuBar(self.menubar)
        self.action_laden = QtGui.QAction(Gui)
        self.action_laden.setObjectName(_fromUtf8("action_laden"))
        self.action_messparameter = QtGui.QAction(Gui)
        self.action_messparameter.setObjectName(_fromUtf8("action_messparameter"))
        self.action_phase_schnitt = QtGui.QAction(Gui)
        self.action_phase_schnitt.setObjectName(_fromUtf8("action_phase_schnitt"))
        self.action_amplitude = QtGui.QAction(Gui)
        self.action_amplitude.setObjectName(_fromUtf8("action_amplitude"))
        self.action_phase = QtGui.QAction(Gui)
        self.action_phase.setObjectName(_fromUtf8("action_phase"))
        self.action_qfaktor = QtGui.QAction(Gui)
        self.action_qfaktor.setObjectName(_fromUtf8("action_qfaktor"))
        self.action_alles = QtGui.QAction(Gui)
        self.action_alles.setObjectName(_fromUtf8("action_alles"))
        self.action_glaetten = QtGui.QAction(Gui)
        self.action_glaetten.setCheckable(True)
        self.action_glaetten.setChecked(False)
        self.action_glaetten.setObjectName(_fromUtf8("action_glaetten"))
        self.action_aktualisieren = QtGui.QAction(Gui)
        self.action_aktualisieren.setObjectName(_fromUtf8("action_aktualisieren"))
        self.action_prozent = QtGui.QAction(Gui)
        self.action_prozent.setCheckable(True)
        self.action_prozent.setObjectName(_fromUtf8("action_prozent"))
        self.action_resfreq = QtGui.QAction(Gui)
        self.action_resfreq.setObjectName(_fromUtf8("action_resfreq"))
        self.action_amp_schnitt = QtGui.QAction(Gui)
        self.action_amp_schnitt.setObjectName(_fromUtf8("action_amp_schnitt"))
        self.action_resonanzkurve = QtGui.QAction(Gui)
        self.action_resonanzkurve.setObjectName(_fromUtf8("action_resonanzkurve"))
        self.action_speichern = QtGui.QAction(Gui)
        self.action_speichern.setEnabled(False)
        self.action_speichern.setObjectName(_fromUtf8("action_speichern"))
        self.menu_messung.addAction(self.action_laden)
        self.menu_messung.addAction(self.action_speichern)
        self.menu_ansicht.addAction(self.action_resonanzkurve)
        self.menu_ansicht.addAction(self.action_phase_schnitt)
        self.menu_ansicht.addAction(self.action_amp_schnitt)
        self.menu_ansicht.addSeparator()
        self.menu_ansicht.addAction(self.action_resfreq)
        self.menu_ansicht.addAction(self.action_amplitude)
        self.menu_ansicht.addAction(self.action_phase)
        self.menu_ansicht.addAction(self.action_qfaktor)
        self.menu_ansicht.addSeparator()
        self.menu_ansicht.addAction(self.action_alles)
        self.menubar.addAction(self.menu_messung.menuAction())
        self.menubar.addAction(self.menu_ansicht.menuAction())

        self.retranslateUi(Gui)
        QtCore.QMetaObject.connectSlotsByName(Gui)

    def retranslateUi(self, Gui):
        Gui.setWindowTitle(_translate("Gui", "Resonanz Fit", None))
        self.label_amplitude.setText(_translate("Gui", "Amplitude", None))
        self.label_phase.setText(_translate("Gui", "Phase", None))
        self.menu_messung.setTitle(_translate("Gui", "Auswertung", None))
        self.menu_ansicht.setTitle(_translate("Gui", "Ansicht", None))
        self.action_laden.setText(_translate("Gui", "Öffnen...", None))
        self.action_messparameter.setText(_translate("Gui", "Messparameter...", None))
        self.action_phase_schnitt.setText(_translate("Gui", "Phasenschnitt", None))
        self.action_amplitude.setText(_translate("Gui", "Amplitude", None))
        self.action_phase.setText(_translate("Gui", "Phase", None))
        self.action_qfaktor.setText(_translate("Gui", "Q-Faktor", None))
        self.action_alles.setText(_translate("Gui", "Alles anzeigen", None))
        self.action_glaetten.setText(_translate("Gui", "Glätten", None))
        self.action_aktualisieren.setText(_translate("Gui", "Aktualisieren", None))
        self.action_prozent.setText(_translate("Gui", "Fehler in Prozent", None))
        self.action_resfreq.setText(_translate("Gui", "Resonanzfrequenz", None))
        self.action_amp_schnitt.setText(_translate("Gui", "Amplitudenschnitt", None))
        self.action_resonanzkurve.setText(_translate("Gui", "Resonanzkurve", None))
        self.action_speichern.setText(_translate("Gui", "Fit speichern...", None))

