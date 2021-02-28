from MainWindows import *
"""
import * = まとめてimport
from 
"""

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ew = ExampleWidget()    
    sys.exit(app.exec_())