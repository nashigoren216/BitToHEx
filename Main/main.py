#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import cv2
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QGraphicsPixmapItem, QGraphicsScene)
from PyQt5 import QtGui,QtCore
from PIL import Image
import image 

# テキストフォーム中心の画面のためQMainWindowを継承する
class BMPtoArray(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):      

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        # メニューバーのアイコン設定
        openFile = QAction(QtGui.QIcon('1513411692.png'), 'Open', self)
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
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', '/home/Development')
        filepath = str(self.fname[0])
        
        path,ext = os.path.splitext(filepath)
        # fname[0]は選択したファイルのパス（ファイル名を含む）
        if self.fname[0]:
            # ファイル読み込み
            f = open(self.fname[0], 'r')
           
            if ext != '.bmp':
                # テキストエディタにファイル内容書き込み
                with f:
                    data = f.read()
                    self.textEdit.setText(data)
            else :
                im = cv2.imread(self.fname[0])
                cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)  # この一文、なくてもよい
                cv2.imshow("image",im)
                '''
                height, width, dim = im.shape
                bytesPerLine = dim * width
                im = QtGui.QImage(im.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
                pic_Item = QGraphicsPixmapItem(QtGui.QPixmap.fromImage(im))
                self.scene = QGraphicsScene(self)
                self.scene.addItem(pic_Item)
                self.setScene(scene)
                '''
                self.BmpFormat()

    def BmpFormat(self):
        # ファイル読み込み
        print(self.fname[0])
        file = open(self.fname[0],"rb")
        fw = open(r"output.bmp","wb")
        ### BMPファイルヘッダ ###
        bfType         = file.read(2)
        bfSize         = file.read(4)
        bfReserved1    = file.read(2)
        bfReserved2    = file.read(2)
        bfOffBitsbfOffBits = file.read(4)

        ### 情報ヘッダ ###
        bcSize         = file.read(4)
        bcWidth        = file.read(4)
        bcHeight       = file.read(4)
        bcPlanes       = file.read(2)
        bcBitCount     = file.read(2)
        biCompression  = file.read(4)
        biSizeImage    = file.read(4)
        biXPixPerMeter = file.read(4)
        biYPixPerMeter = file.read(4)
        biClrUsed      = file.read(4)
        biCirImportant = file.read(4)

        ### 出力ファイルのヘッダ作成 ###
        fw.write(bfType            )
        fw.write(bfSize            )
        fw.write(bfReserved1       )
        fw.write(bfReserved2       )
        fw.write((54).to_bytes(4,"little"))
        fw.write(bcSize            )
        fw.write(bcWidth           )
        fw.write(bcHeight          )
        fw.write(bcPlanes          )
        fw.write(bcBitCount        )
        fw.write(biCompression     )
        fw.write(biSizeImage       )
        fw.write(biXPixPerMeter    )
        fw.write(biYPixPerMeter    )
        fw.write(biClrUsed         )
        fw.write(biCirImportant    )

        ### 処理に必要そうなデータはデータとして持っておく ###
        bfType_str             = bfType.decode()
        bfOffBitsbfOffBits_int = int.from_bytes(bfOffBitsbfOffBits, "little")
        bcSize_int             = int.from_bytes(bcSize,             "little")
        bcWidth_int            = int.from_bytes(bcWidth,            "little")
        bcHeight_int           = int.from_bytes(bcHeight,           "little")
        bcBitCount_int         = int.from_bytes(bcBitCount,         "little")
        biCompression_int      = int.from_bytes(biCompression,      "little")

        ### 想定する画像フォーマットでない場合は、ここで処理を終了 ###

        if  (bfType_str!="BM") or \
            (bcSize_int!=40)   or \
            (bcBitCount_int!=24) or \
            (biCompression_int!=0):
            print ("This file format is not supported!")
            sys.exit()


        ### 画像サイズ確認(デバッグ用) ###
        print ("(Width,Height)=(%d,%d)" % (bcWidth_int,bcHeight_int))

        ### 画像データ本体へJump。ほどんど不要かも。###
        offset = bfOffBitsbfOffBits_int-54
        file.read(offset)

        ######################
        ### 画像データ処理 ###
        ######################
        ### 画像処理パラメータ ###
        gain = 1.5

        ### 画像データ処理開始 ###
        dummy_size=0
        mod = (bcWidth_int*3)%4
        if (mod!=0) : dummy_size = 4-mod 
        for y in range(bcHeight_int):
            for x in range(bcWidth_int):
                R = int.from_bytes(file.read(1), "little")
                G = int.from_bytes(file.read(1), "little")
                B = int.from_bytes(file.read(1), "little")
                ### 画像処理(ゲイン) ###
                R = min(int(R*gain), 255)
                G = min(int(G*gain), 255)
                B = min(int(B*gain), 255)
                ### 処理結果を書き込む ###
                fw.write(R.to_bytes(1,"little",signed=False))
                fw.write(G.to_bytes(1,"little",signed=False))
                fw.write(B.to_bytes(1,"little",signed=False))           
            ### 画像の横ラインデータサイズを4の倍数にそろえる ###
            for i in range(dummy_size):
                tmp = int.from_bytes(file.read(1), "little")
                fw.write((255).to_bytes(1,"little",signed=False))
            
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = BMPtoArray()
    sys.exit(app.exec_())


