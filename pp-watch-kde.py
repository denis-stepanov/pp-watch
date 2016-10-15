#!/usr/bin/python

import sys
import urllib2
import json
from PyQt4 import QtGui
from PyQt4.QtCore import QTimer

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        menu = QtGui.QMenu(parent)
        self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)
        exitAction = menu.addAction(self.quitAction)
        self.setContextMenu(menu)

        self.icons = {}
        for i in range(0, 3600, 225):
            self.icons[str(i / 10.0)] = QtGui.QIcon("pics/" + str(i / 10.0) + ".png")

        self.checkWind()
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkWind)
        self.timer.start(3 * 60 * 1000)

    def checkWind(self):
        j = urllib2.urlopen('http://api.pioupiou.fr/v1/live/503')
        j_obj = json.load(j)
        self.setIcon(self.icons[str(int(j_obj['data']['measurements']['wind_heading'] * 100 + 1125) /2250 * 22.5)])
        self.setToolTip('Wind direction %s, speed %d km/h, max %d km/h, min %d km/h. Taken %s' % (j_obj['data']['measurements']['wind_heading'], round(j_obj['data']['measurements']['wind_speed_avg']), round(j_obj['data']['measurements']['wind_speed_max']), round(j_obj['data']['measurements']['wind_speed_min']), j_obj['data']['measurements']['date']))

def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

