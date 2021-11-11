#!/usr/bin/python

"""
ZetCode PyQt6 tutorial

This example shows a QSlider widget.

Author: Jan Bodnar
Website: zetcode.com
"""

from PyQt6.QtWidgets import (QWidget, QSlider,
        QLabel, QApplication,QPushButton,QProgressBar, QLineEdit)
from PyQt6.QtCore import Qt, QBasicTimer,pyqtSignal, QObject
from PyQt6.QtGui import QPixmap
import sys
import re

def has_wav_extension(path):
    return path.endswith(".wav")

class Communicate(QObject):

    musicDropped = pyqtSignal(str)

class Button(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.setAcceptDrops(True)

        self.c = Communicate()
        self.c.musicDropped.connect(parent.musicDropped)


    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            print('accepted')
            links = []
            for url in e.mimeData().urls():
                str_url = str(url.toLocalFile())
                if has_wav_extension(str_url):

                    links.append(str_url)
                else:
                    print("No wav file")
                    e.ignore()
                    return
            self.c.musicDropped.emit(links[0] or "yeah")
            e.accept()
        else:
            print('rejected')
            print(e.mimeData().data('audio/wav'))
            e.ignore()


    def dropEvent(self, e):

        self.setText('accepted')


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def musicDropped(self,links):
        print('It dropped')
        print(links)

    def initUI(self):
        lbl1 = QLabel('ZetCode', self)
        lbl1.move(15, 10)

        sld = QSlider(Qt.Orientation.Horizontal, self)
        sld.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        sld.setGeometry(30, 40, 200, 30)
        sld.valueChanged[int].connect(self.changeValue)

        # self.label = QLabel(self)
        # self.label.setPixmap(QPixmap('mute.png'))
        # self.label.setGeometry(250, 40, 80, 30)

        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)

        greenb.clicked[bool].connect(self.setColor)


        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        edit = QLineEdit('', self)
        edit.setDragEnabled(True)
        edit.move(30, 225)

        button = Button("Button", self)
        button.move(190, 225)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QSlider')
        self.show()


    def changeValue(self, value):
        pass
        # if value == 0:

        #     self.label.setPixmap(QPixmap('mute.png'))
        # elif 0 < value <= 30:

        #     self.label.setPixmap(QPixmap('min.png'))
        # elif 30 < value < 80:

        #     self.label.setPixmap(QPixmap('med.png'))
        # else:

        #     self.label.setPixmap(QPixmap('max.png'))

    def setColor(self, pressed):

        source = self.sender()

        if pressed:
            val = 255
        else:
            val = 0

        if source.text() == "Blue":
            self.col.setBlue(val)
    
    def timerEvent(self, e):

        if self.step >= 100:

            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)


    def doAction(self):

        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()