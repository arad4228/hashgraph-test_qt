import PyQt5
import os, sys
from mainWindow import *

# QPA 관련 환경 설정을 위한 필수 명령어
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'Qt5','plugins','platforms','QtWebEngineProcess')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Main_WindowClass()
    myWindow.show()
    app.exec_()