import sys, os, time
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\S1SECOM\Anaconda3\envs\pytoexe\Library\plugins\platforms'
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
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
        self.thread = QtCore.QThread()
        self.thread.start()
        self.autosave = Autosave()
        self.autosave.moveToThread(self.thread)

        # table & log 설정
        self.setTable()
        self.log_data()

        # 버튼에 기능을 연결하는 코드
        self.start_btn.clicked.connect(self.plot_data)
        self.stop_btn.clicked.connect(self.plot_data2)
        self.store_btn.clicked.connect(self.storeFunction)
        self.reset_btn.clicked.connect(self.resetFunction)
        self.autosave_btn.clicked.connect(self.autosaveFunction)
        self.reload_btn.clicked.connect(self.insertData)
        self.delete_btn.clicked.connect(self.deleteFunction)

        # spinbox 값이 바뀔때 마다 함수 실행
        global second
        self.spinBox.valueChanged.connect(self.spinBoxChanged)
        second = self.spinBox.value()

    def setTable(self):
        # table 가로 갯수
        self.file_table.setColumnCount(1)
        # table 세로 갯수
        # self.file_table.setRowCount(3)
        
        # table 헤더 라벨
        self.file_table.setHorizontalHeaderLabels(['파일명'])
        # self.file_table.setVerticalHeaderLabels(['1','2','3'])

        # setSectionResizeMode - 테이블 크기에 맞추어 늘려줌
        # 가로 헤더 사이즈 조정
        self.file_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 세로 헤더 사이즈 조정
        # self.file_table.verticalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        # 테이블의 셀 병합하기 - (1, 0) 셀을 기준으로 Row는 1칸, Column은 2칸을 병합
        # self.file_table.setSpan(1,0, 1,2)
        
        self.file_table.cellDoubleClicked.connect(self.view_data)

        # 테이블 수정 금지
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 데이터 입력
        self.insertData()

    def insertData(self):
        path = "./tmptext"
        file_list = os.listdir(path)
        file_list_txt = [file for file in file_list if file.endswith(".txt")]

        self.file_table.setRowCount(len(file_list_txt))

        for i, file_name in enumerate(file_list_txt):
            # 테이블 아이템 입력
            self.file_table.setItem(i, 0, QTableWidgetItem(""))
            # 테이블 값 입력
            self.file_table.item(i, 0).setText(file_name)

        # 테이블 각 셀의 스타일 세팅
        # 셀의 백그라운드 설정
        #self.file_table.item(0, 0).setBackground(QtGui.QColor("#FF0000"))
        # 셀안의 텍스트의 정렬 설정
        #self.file_table.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        # 셀안의 텍스트 폰트 설정
        #font = QtGui.QFont("맑은 고딕", 16, QtGui.QFont.Normal)
        #self.file_table.item(0, 0).setFont(font)
        # 테이블 값 입력
        # self.file_table.item(0, 0).setText("홍길동")

    def view_data(self) :
        global txt
        row = self.file_table.currentRow()
        cur = self.file_table.currentColumn()
        item = self.file_table.item(row, cur)
        txt = item.text()

        # msg = QMessageBox.information(self, "내용", txt)
        dlg = LogDialog()
        dlg.exec_()

    def plot_data(self):
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load("./1617527254289.jpg")
        self.qPixmapFileVar = self.qPixmapFileVar.scaled(360, 200)
        self.widget_image.setPixmap(self.qPixmapFileVar)

        x=range(0, 20, 2)
        y=range(0, 10)
        self.widget_graph.canvas.ax.plot(x, y)
        self.widget_graph.canvas.draw()

    def log_data(self):
        global result
        result = ['people', 'cat', 'dog']
        model = QStandardItemModel()
        for r in result:
            model.appendRow(QStandardItem(r))
        self.log_view.setModel(model)
        # log내용 수정 금지
        self.log_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def plot_data2(self):
        print("delete")
        self.widget_graph.canvas.ax.clear()

    def storeFunction(self):
        now_time = time.strftime('%y_%m_%d_%H_%M_%S', time.localtime(time.time()))
        f = open("./tmptext/" + now_time + ".txt", 'w')
        for data in result:
            f.write(data + "\n")
        f.close()
        self.insertData()

    def deleteFunction(self):
        row = self.file_table.currentRow()
        cur = self.file_table.currentColumn()
        item = self.file_table.item(row, cur)
        txt = item.text()
        os.remove('./tmptext/' + txt)
        self.insertData()

    def resetFunction(self):
        print("reset")
        result = []
        self.log_data()

    def spinBoxChanged(self):
        global second
        second = self.spinBox.value()

    def autosaveFunction(self):
        sender_obj = self.sender()
        if sender_obj.text() == "자동저장":
            sender_obj.setText("자동저장 취소")
            self.spinBox.setReadOnly(True)
            self.autosave.save_start(second)
            self.insertData()
        else:
            sender_obj.setText("자동저장")
            self.spinBox.setReadOnly(False)
            self.autosave.save_stop()


class Autosave(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.stop_flag = False

    def save_start(self, s):
        while True:
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(s * 100, loop.quit) # 5000 ms
            loop.exec_()

            now_time = time.strftime('%y_%m_%d_%H_%M_%S', time.localtime(time.time()))
            f = open("./tmptext/" + now_time + ".txt", 'w')
            for data in result:
                f.write(data + "\n")
            f.close()

            if self.stop_flag:
                self.stop_flag = False
                break

    def save_stop(self):
        self.stop_flag = True

class LogDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialogUI()

    def dialogUI(self):

        f = open('./tmptext/' + txt, 'r')
        lines = f.readlines()
        f.close()
        listview = QListView(self)
        model = QStandardItemModel()
        for l in lines:
            model.appendRow(QStandardItem(l))
        listview.setModel(model)
        # log내용 수정 금지
        listview.setEditTriggers(QAbstractItemView.NoEditTriggers)

        listview.scrollToBottom()
        listview.resize(280,180)
        listview.move(20,10)
        self.setFixedSize(320,200)
        self.show()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()