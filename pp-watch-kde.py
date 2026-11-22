#!/usr/bin/env python3

import sys
import urllib.request
import json
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import QTimer

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, parent=None):
        super().__init__(parent)
        menu = QtWidgets.QMenu(parent)
        self.quitAction = QtGui.QAction("&Quit", self)
        self.quitAction.triggered.connect(QtWidgets.QApplication.quit)
        menu.addAction(self.quitAction)
        self.setContextMenu(menu)

        self.icons = {}
        for i in range(0, 3600, 225):
            self.icons[str(i / 10)] = QtGui.QIcon("pics/" + str(i / 10) + ".png")

        self.checkWind()
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkWind)
        self.timer.start(3 * 60 * 1000)

    def checkWind(self):
        j = urllib.request.urlopen('http://api.pioupiou.fr/v1/live/503')
        j_obj = json.load(j)
        self.setIcon(self.icons[str(int(j_obj['data']['measurements']['wind_heading'] * 100 + 1125) // 2250 % 16 * 22.5)])
        self.setToolTip('Wind direction %s, speed %d km/h, max %d km/h, min %d km/h. Taken %s' % (j_obj['data']['measurements']['wind_heading'], round(j_obj['data']['measurements']['wind_speed_avg']), round(j_obj['data']['measurements']['wind_speed_max']), round(j_obj['data']['measurements']['wind_speed_min']), j_obj['data']['measurements']['date']))

def main():
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(w)

    trayIcon.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

