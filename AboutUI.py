from PyQt4.QtGui import *
from PyQt4 import uic

class AboutWindow(QMainWindow):
    """MainWindow inherits QMainWindow"""

    def __init__(self, parent=None):
        ( AboutWindow, QMainWindow ) = uic.loadUiType('AboutUI.ui')
        QMainWindow.__init__(self, parent)
        self.ui = AboutWindow()
        self.ui.setupUi(self)

    def __del__(self):
        self.ui = None