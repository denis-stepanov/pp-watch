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
        try:
            j = urllib.request.urlopen('http://api.pioupiou.fr/v1/live/503', timeout=30)
            m = json.load(j)['data']['measurements']
            heading = m['wind_heading']
            avg = m['wind_speed_avg']
            smax = m['wind_speed_max']
            smin = m['wind_speed_min']
        except (OSError, ValueError, KeyError, TypeError) as e:
            print('Error: failed to get wind data: %s: %s' % (type(e).__name__, e), file=sys.stderr)
            return  # Keep the previous icon and tooltip
        missing = [k for k, v in (('wind_heading', heading), ('wind_speed_avg', avg), ('wind_speed_max', smax), ('wind_speed_min', smin)) if v is None]
        if missing:
            print('Error: sensor reported no data for: %s' % ', '.join(missing), file=sys.stderr)
            return  # Keep the previous icon and tooltip

        self.setIcon(self.icons[str(int(heading * 100 + 1125) // 2250 % 16 * 22.5)])
        self.setToolTip('Wind direction %s, speed %d km/h, max %d km/h, min %d km/h. Taken %s' % (heading, round(avg), round(smax), round(smin), m['date']))

def main():
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(w)

    trayIcon.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

