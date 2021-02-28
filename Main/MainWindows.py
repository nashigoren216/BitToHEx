# - * - coding: utf8 - * -

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
from bmpread import *



class ExampleWidget(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):      

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        # メニューバーのアイコン設定
        openFile = QAction(QIcon('1513411692.png'), 'Open', self)
        # ショートカット設定
        openFile.setShortcut('Ctrl+O')
        # ステータスバー設定
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        # メニューバー作成
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)       

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()


    def showDialog(self):

        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        # fname[0]は選択したファイルのパス（ファイル名を含む）
        if fname[0]:
            # ファイル読み込み
            f = open(fname[0], 'r')

            # テキストエディタにファイル内容書き込み
            BmpRead(f)
            """
                with f:
                data = f.read()
                self.textEdit.setText(data)
            """