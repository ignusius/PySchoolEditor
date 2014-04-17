#!/usr/bin/python3

__author__ = "Komarov Alexander"
__version__ = "0.1"
__license__ = "GPL"
__email__ = "ignusius@gmail.com"


"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import  os
import codecs
# import PyQt4 QtCore and QtGui modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4 import Qsci
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerPython
import webbrowser
from AboutUI import AboutWindow

( Ui_MainWindow, QMainWindow ) = uic.loadUiType('MainUI.ui')


class MainWindow(QMainWindow):
    """MainWindow inherits QMainWindow"""

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.editor = self.ui.editor
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.editor.setFont(font)
        self.editor.setMarginsFont(font)
        self.editor.setMarginsFont(font)
        self.lexer = QsciLexerPython()
        self.lexer.setDefaultFont(font)
        self.api = Qsci.QsciAPIs(self.lexer)
        self.editor.setLexer(self.lexer)
        self.editor.setAutoCompletionThreshold(1)
        self.editor.setMarginLineNumbers(1,True)
        self.editor.setMarginWidth(1,"0000")
        self.editor.setIndentationWidth(4)
        self.editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.editor.setCaretLineBackgroundColor(QColor("#fbf6f6"))
        self.editor.setAutoCompletionSource(self.editor.AcsAPIs)
        self.editor.setAutoIndent(True)
        self.editor.setUtf8(True)
        self.ui.find_bar.hide()

        self.filename=""

    def __del__(self):
        self.ui = None

    def new(self):
        if self.filename !="":
            self.save()
            self.open()

    def open(self):
        try:
            self.filename = QFileDialog.getOpenFileName(self, 'Открыть файл', '', ".py(*py)")
            self.editor.setText(codecs.open(self.filename,'r',"utf-8").read())
            self.setWindowTitle('PySchoolEdit - ['+self.filename+']')
        except(FileNotFoundError):
            pass

    def save(self):
        if self.filename == "":
            self.filename = QFileDialog.getSaveFileName(self, 'Сохранить файл', '', ".py(*.py)")
            with codecs.open(self.filename,"w","utf-8") as f:
                f.write(self.editor.text())
            self.ui.statusBar.showMessage("Сохранено")
            self.setWindowTitle('PySchoolEdit - ['+self.filename+']')
        else:
            with codecs.open(self.filename,"w","utf-8") as f:
                f.write(self.editor.text())
        self.ui.statusBar.showMessage("Сохранено")

    def save_as(self):
        self.filename = QFileDialog.getSaveFileName(self, u'Сохранить файл', '', ".py(*.py)")
        with codecs.open(self.filename,"w","utf-8") as f:
                f.write(self.editor.text())
        self.ui.statusBar.showMessage("Сохранено")
        self.setWindowTitle('PySchoolEdit - ['+self.filename+']')

    def run(self):

        self.save()
        if sys.platform=='linux':
            filename=self.filename.replace(r" ","\ ")

            os.system('xterm -geometry 50x15 -fa \'terminal\' -e bash -c  \'python3 '+filename+' \
; read -p "Для продолжения нажмите любую клавишу . . ."\'')
        if sys.platform=='win32':
            os.system('C:\Python33\python "'+self.filename+'"& pause')
    def find_bar_show(self,status):
        if status==True:
            self.ui.find_bar.show()
        else:
            self.ui.find_bar.hide()

    def find_text(self):
        if self.ui.case_cmbox.checkState()==0:
            status=False
        else:
            status=True
        self.editor.findFirst(self.ui.find_field.text(),True,status,True,True,True)


    def app_quit(self):
        QApplication.quit()

    def app_site(self):
        webbrowser.open_new("http://python-rutour.rhcloud.com/")

    def app_about(self):
        self.about_window = AboutWindow(self)
        self.about_window.show()

    def text_changed(self):
        self.ui.statusBar.showMessage("Текст изменён")
#-----------------------------------------------------#
if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('PySchoolEdit')

    # create widget
    w = MainWindow()
    w.setWindowTitle('PySchoolEdit')
    w.show()

    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())
