import sys, os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\S1SECOM\Anaconda3\envs\pytoexe\Library\plugins\platforms'
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

import matplotlib.pyplot as plt
import numpy as np

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
path = r'D:\aa\pythonToexe\pjt\pjt.ui'
form_class = uic.loadUiType(path)[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.initData()

        #버튼에 기능을 연결하는 코드
        self.start_btn.clicked.connect(self.plot_data)
        self.stop_btn.clicked.connect(self.plot_data2)
        self.store_btn.clicked.connect(self.storeFunction)
        self.reset_btn.clicked.connect(self.resetFunction)
        self.autosave_btn.clicked.connect(self.autosaveFunction)

    def initData(self):
        print("init")
        self.sampleData = {
            'Python': ['Fluent Python', 'Python Programming', 'Learning Python'],
            'go' : 'The Go Programming Language',
            'C#' : ['Inside C#', 'C# In Depth'],
            'C' : 'The C Programming Language'
        }

    def plot_data(self):
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load("./1617527254289.jpg")
        # self.qPixmapFileVar = self.qPixmapFileVar.scaled(360, 200)
        self.widget_image.setPixmap(self.qPixmapFileVar)

        x=range(0, 20, 2)
        y=range(0, 10)
        self.widget_graph.canvas.ax.plot(x, y)
        self.widget_graph.canvas.draw()

    def plot_data2(self):
        print("delete")
        self.widget_graph.canvas.ax.clear()

    def storeFunction(self) :
        print("store")

    def resetFunction(self) :
        print("reset")

    def autosaveFunction(self) :
        print("autosave")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()