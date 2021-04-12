import sys
import requests
import math
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
        self.mode = 'map'
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton.setIcon(QtGui.QIcon('fi-rr-cross-small.png'))
        self.pushButton_3.setIcon(QtGui.QIcon('fi-rr-interrogation.png'))
        self.pushButton.clicked.connect(sys.exit)
        self.pushButton_2.clicked.connect(self.Right_Check)
        self.pushButton_3.clicked.connect(self.help)
        self.comboBox.activated[str].connect(self.MapMode)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(event.pos())
            pos = event.pos()
            self.getCoordinates(pos.x(), pos.y())

    def getCoordinates(self, x, y):
        global spn_, lon, lat
        spn = [float(spn_[0]), float(spn_[1])]
        lon_ = float(lon)
        lat_ = float(lat)
        w = 640
        h = 360
        max_a = lon_ + (spn[0] / 2)
        max_b = lat_ + (spn[1] / 2)
        min_a = lon_ - (spn[0] / 2)
        min_b = lat_ - (spn[1] / 2)
        s_a = w / (max_a - min_a)
        o_a = -w * min_a / (max_a - min_a)
        s_b = -h / (max_b - min_b)
        o_b = h * max_b / (max_b - min_b)
        finded_lon = str(round((x - o_a) / s_a, 6))
        finded_lat = str(round((y - o_b) / s_b, 6))
        print(finded_lon, finded_lat)
        self.ShowMap(lat, lon, spn_, [finded_lon, finded_lat, "pm2rdm"])

    def MapMode(self, text):
        a = {'Схема': 'map', 'Спутник': 'sat', 'Гибрид': 'sat,skl'}
        self.mode = a[text]

    def help(self):
        help_dialog_inst = HelpDialog()
        help_dialog_inst.show()
        help_dialog_inst.exec()

    def Right_Check(self):
        a = 'Вы ввели некорректные:'
        a1 = self.lineEdit.text()
        a2 = self.lineEdit_2.text()
        if a1[0] == '-':
            a1 = a1[1:]
        if a2[0] == '-':
            a2 = a2[1:]
        if a1.count('.') > 1 or not a1.replace('.', '').isdigit():
            a += '\nШироту'
        else:
            if float(a1) > 88:
                a += '\nШироту'
        if a2.count('.') > 1 or not a2.replace('.', '').isdigit():
            a += '\nДолготу'
        else:
            if float(a2) > 88:
                a += '\nДолготу'
        spn = self.lineEdit_3.text().split(', ')
        if ',' not in self.lineEdit_3.text():
            spn = [self.lineEdit_3.text(), self.lineEdit_3.text()]
        if spn[0].count('.') > 1 or not spn[0].replace('.', '').isdigit() or spn[1].count('.') > 1 or not spn[
            1].replace('.', '').isdigit():
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

    def ShowMap(self, Latitude, Longitude, spn, pts=[''], fulladdress=[""]):
        global lon, lat, spn_, points, address
        api_server = "http://static-maps.yandex.ru/1.x/"
        lon = str(Longitude)
        lat = str(Latitude)
        spn_ = spn
        points = pts
        address = fulladdress
        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join(spn_),
            "l": self.mode,
            "size": "640,360",
            "pt": ",".join(points)
        }
        response = requests.get(api_server, params=params)
        self.map_file = "map.png"
        a = self.lineEdit.text()
        b = self.checkBox.checkState()
        uic.loadUi('map.ui', self)
        self.lineEdit.setText(a)
        self.checkBox.setChecked(b)
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.label.setPixmap(self.pixmap)
        if self.checkBox.checkState():
            self.label_2.setText(fulladdress[0] + fulladdress[1])
        else:
            self.label_2.setText(fulladdress[0])
        self.pushButton.clicked.connect(sys.exit)
        self.pushButton.setIcon(QtGui.QIcon('fi-rr-cross-small.png'))
        self.pushButton_2.setIcon(QtGui.QIcon('search.png'))
        self.pushButton_3.setIcon(QtGui.QIcon('cil-trash.png'))
        self.pushButton_2.clicked.connect(self.SearchMap)
        self.pushButton_3.clicked.connect(self.ClearSearch)
        self.checkBox.stateChanged.connect(self.checkBoxChanged)

    def checkBoxChanged(self):
        global lat, lon, spn_, address, points
        self.ShowMap(lat, lon, spn_, points, fulladdress=address)

    def SearchMap(self):
        global spn_, points
        if self.lineEdit.text() != '':
            api_server = "http://geocode-maps.yandex.ru/1.x/"
            params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": self.lineEdit.text(),
                "format": "json"
            }
            response = requests.get(api_server, params=params)
            json = response.json()
            if json["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"] != "0":
                toponym = json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
                points = [toponym.split()[0], toponym.split()[1], "pm2rdm"]
                a = json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                    "GeocoderMetaData"]["Address"]
                a = a["formatted"], self.SearchFullAddress(a["formatted"])
                self.ShowMap(toponym.split()[1], toponym.split()[0], spn_, points, fulladdress=a)

    def SearchFullAddress(self, address):
        api_server = "http://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": address,
            "format": "json"
        }
        response = requests.get(api_server, params=params)
        json = response.json()
        if json["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"] != "0":
            a = json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                "GeocoderMetaData"]["Address"]
            if "postal_code" in a:
                return ', ' + a["postal_code"]
            else:
                return ''

    def ClearSearch(self):
        global lon, lat, spn_, points
        if self.lineEdit.text() != '':
            self.lineEdit.setText('')
        self.ShowMap(lat, lon, spn_)

    def keyPressEvent(self, event):
        global lon, lat, spn_, points
        if event.key() == Qt.Key_PageDown:
            if float(spn_[0]) * 2 > 180:
                spn_[0] = str(180)
            else:
                spn_[0] = str(float(spn_[0]) * 2)
            if float(spn_[1]) * 2 > 90:
                spn_[1] = str(90)
            else:
                spn_[1] = str(float(spn_[1]) * 2)
            self.ShowMap(lat, lon, spn_, points)
        elif event.key() == Qt.Key_PageUp:
            if float(spn_[0]) / 2 < 0.001:
                spn_[0] = str(0.0001)
            else:
                spn_[0] = str(float(spn_[0]) / 2)
            if float(spn_[1]) / 2 < 0.0001:
                spn_[1] = str(0.0001)
            else:
                spn_[1] = str(float(spn_[1]) / 2)
            self.ShowMap(lat, lon, spn_, points)
        elif event.key() == Qt.Key_Up:
            if float(lat) + 2 * float(spn_[0]) < 88:
                self.ShowMap(str(float(lat) + 4 * float(spn_[0])), lon, spn_, points)
        elif event.key() == Qt.Key_Down:
            if float(lat) - 2 * float(spn_[0]) > 0:
                self.ShowMap(str(float(lat) - 4 * float(spn_[0])), lon, spn_, points)
        elif event.key() == Qt.Key_Right:
            if float(lon) + 2 * float(spn_[1]) < 88:
                self.ShowMap(lat, str(float(lon) + 4 * float(spn_[1])), spn_, points)
        elif event.key() == Qt.Key_Left:
            if float(lon) - 2 * float(spn_[1]) > 0:
                self.ShowMap(lat, str(float(lon) - 4 * float(spn_[1])), spn_, points)


def my_excepthook(type, value, tback):
    print(value)
    sys.__excepthook__(type, value, tback)


if __name__ == '__main__':
    sys.excepthook = my_excepthook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
