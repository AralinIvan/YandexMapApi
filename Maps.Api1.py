import sys
import requests
from help_dialog import Ui_Dialog as help_dialog_ui
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QDialog


class HelpDialog(QDialog, help_dialog_ui):
    def __init__(self, text='help'):
        QDialog.__init__(self)
        self.setupUi(self)
        if text != 'help':
            self.textBrowser.setText(text)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('one.ui', self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(sys.exit)
        self.pushButton_2.clicked.connect(self.Right_Check)
        self.pushButton_3.clicked.connect(self.help)

    def help(self):
        help_dialog_inst = HelpDialog()
        help_dialog_inst.show()
        help_dialog_inst.exec()


    def Right_Check(self):
        a = 'Вы ввели некорректные:'
        if self.lineEdit.text().count('.') > 1 or not self.lineEdit.text().replace('.', '').isdigit():
            a += '\nДолготу'
            print(1)
        else:
            if float(self.lineEdit.text()) > 179 or float(self.lineEdit.text()) < -179:
                a += '\nДолготу'
        if self.lineEdit_2.text().count('.') > 1 or not self.lineEdit_2.text().replace('.', '').isdigit():
            a += '\nШироту'
        else:
            if float(self.lineEdit_2.text()) > 88 or float(self.lineEdit_2.text()) < -88:
                a += '\nШироту'
        spn = self.lineEdit_3.text().split(', ')
        if ',' not in self.lineEdit_3.text():
            spn = [self.lineEdit_3.text(), self.lineEdit_3.text()]
        if spn[0].count('.') > 1 or not spn[0].replace('.', '').isdigit() or spn[1].count('.') > 1 or not spn[1].replace('.', '').isdigit():
            a += '\nМасштаб'
        else:
            if float(spn[0]) > 180 or float(spn[0]) < -180 or float(spn[1]) > 90 or float(spn[1]) < -90:
                a += '\nМасштаб'

        if a[-1] == ',':
           a = a[0:-1]
        if a == 'Вы ввели некорректные:':
            self.LoadMapUI(float(self.lineEdit.text()), float(self.lineEdit_2.text()), spn)
        else:
            error_dialog_inst = HelpDialog(a)
            error_dialog_inst.show()
            error_dialog_inst.exec()


    def LoadMapUI(self, Longitude, Latitude, spn, pts=['']):
        uic.loadUi('map.ui', self)
        self.ShowMap(Longitude, Latitude, spn, pts)

    def ShowMap(self, Longitude, Latitude, spn, pts=['']):
        global lon, lat, spn_, points
        api_server = "http://static-maps.yandex.ru/1.x/"
        lon = str(Latitude)
        lat = str(Longitude)
        spn_ = spn
        points = pts
        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join(spn_),
            "l": "map",
            "size": "640,360",
            "pt": ",".join(points)
        }
        response = requests.get(api_server, params=params)
        self.map_file = "map.png"
        a = self.lineEdit.text()
        uic.loadUi('map.ui', self)
        self.lineEdit.setText(a)
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.label.setPixmap(self.pixmap)
        self.pushButton.clicked.connect(sys.exit)
        self.pushButton_2.setIcon(QtGui.QIcon('lupa.png'))
        self.pushButton_3.setIcon(QtGui.QIcon('cil-trash.png'))
        self.pushButton_2.clicked.connect(self.SearchMap)
        self.pushButton_3.clicked.connect(self.ClearSearch)

    def SearchMap(self):
        global spn_, points
        print(1)
        api_server = "http://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.lineEdit.text(),
            "format": "json"
        }
        response = requests.get(api_server, params=params)
        json = response.json()
        toponym = json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        points = [toponym.split()[0], toponym.split()[1]]
        print(2)
        self.ShowMap(toponym.split()[1], toponym.split()[0], spn_, points)


    def ClearSearch(self):
        global lon, lat, spn_, points
        if self.lineEdit.text() != '':
            self.lineEdit.setText('')
        self.ShowMap(lat, lon, spn_)



    def keyPressEvent(self, event):
        global lon, lat, spn_, points
        spnn = [1, 1]
        if event.key() == Qt.Key_PageDown:
            if float(spn_[0]) * 2 > 180:
                spnn[0] = str(180)
            else:
                spnn[0] = str(float(spn_[0]) * 2)
            if float(spn_[1]) * 2 > 90:
                spnn[1] = str(90)
            else:
                spnn[1] = str(float(spn_[1]) * 2)
            print(spnn)
            self.ShowMap(lat, lon, spnn, points)
        elif event.key() == Qt.Key_PageUp:
            if float(spn_[0]) / 2 < 0.001:
                spnn[0] = str(0.0001)
            else:
                spnn[0] = str(float(spn_[0]) / 2)
            if float(spn_[1]) / 2 < 0.0001:
                spnn[1] = str(0.0001)
            else:
                spnn[1] = str(float(spn_[1]) / 2)
            print(spnn)
            self.ShowMap(lat, lon, spnn, points)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())