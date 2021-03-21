import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QMainWindow, QGraphicsView, QPushButton, 
    QHBoxLayout, QVBoxLayout, QWidget, QApplication, QGraphicsScene)

class GraphicsScene(QGraphicsScene):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._image = QImage()

  @property
  def image(self):
    return self._image

  @image.setter
  def image(self, img):
    self._image = img
    self.update()

  def drawBackground(self, painter, rect):
    if self.image.isNull():
      super().drawBackground(painter, rect)
    else:
      painter.drawImage(rect, self._image)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "parcelDeliveryIta";
        self.top = 100
        self.left = 100
        self.width = 1500
        self.height = 900
        self.initUI()

    def initUI(self):

        self.scene = GraphicsScene(self)
        self.scene._image = QImage('1513411692.png')
        view = QGraphicsView(self.scene, self)
        self.scene.setSceneRect(0, 0, view.width(), view.height())

        addLine = QPushButton('AddLine')
        addLine.clicked.connect(self.addLine)

        hbox = QHBoxLayout(self)
        hbox.addWidget(view)

        vbox = QVBoxLayout(self)
        vbox.addWidget(addLine)

        hbox.addLayout(vbox)

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setLayout(hbox)
        self.show()

    def addLine(self):
        self.scene.addLine(0, 0, 100, 100)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())