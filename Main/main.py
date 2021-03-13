from MainWindows import *

if __name__ == '__main__':

    print("BMPファイルからマイコン表示用の配列にデータを変換する")
    app = QApplication(sys.argv)
    ew = ExampleWidget()    
    sys.exit(app.exec_())



