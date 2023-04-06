import sys
import os
import PyQt5
from PyQt5.QtWidgets import *

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'Qt5','plugins','platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

app = QApplication(sys.argv)

win = QWidget()
win.show()

app.exec_()