# PyQt 기본 위젯

## 0. 초기 설정

1. conda 가상환경 설치

2. 환경변수 설정 & 라이브러리 import

   ```python
   # conda 가상환경의 플러그인-플랫폼위치
   import os
   import sys
   from PyQt5.QtWidgets import *
   from PyQt5.QtCore import *
   
   os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\S1SECOM\Anaconda3\envs\pytoexe\Library\plugins\platforms'
   ```

## 1. Button (QPushButton)

1. QPushButton 위젯을 생성한다
2. 위젯에서 'clicked' 시그널이 발생하면 호출될 슬롯(clicked_slot)을 구현한다
3. 시그널과 슬롯을 이벤트 루프를 생성하기 전에 연결(connect) 한다

```python
def clicked_slot():
    print('clicked')
    
# PyQt에서는 QApplication 객체에서 exec_ 메서드를 호출해 이벤트 루프를 생성
app = QApplication(sys.argv)

btn = QPushButton("Push")
btn.clicked.connect(clicked_slot)
btn.show()

app.exec_()
```

![image-20210319162747728](PyQt.assets/image-20210319162747728.png)



## 2. 윈도우 만들기 (QMainWindow)

> 최상위 위젯을 의미하는 윈도우

-  QMainWindow나 QDialog 클래스를 사용해 윈도우를 생성

  1. QApplication 객체인 app을 생성한다.
  2. PushButtonWindow 라는 클래스의 객체를 생성하고 보이게 한다.
  3. exec_ 메서드를 호출해서 이벤트 루프를 생성합니다.

  ```python
  class PushButtonWindow(QMainWindow):
      def __init__(self):
          super().__init__()
          self.setupUI()
  
      def setupUI(self):
          self.setWindowTitle("PushButtonWindow")
  
          btn = QPushButton("Click me", self)
          btn.move(20, 20)	# "Click me" 버튼 위치 (좌, 상)
          btn.clicked.connect(self.btn_clicked)
  
      def btn_clicked(self):
          QMessageBox.about(self, "메시지", "clicked")
  
  if __name__ == "__main__":
      app = QApplication(sys.argv)
      window = PushButtonWindow()
      window.show()
      app.exec_()
  ```

  ![image-20210319163023599](PyQt.assets/image-20210319163023599.png)



## 3. QLabel

> 텍스트나 이미지를 출력하는 데 사용

```python
class ButtonLabelWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("ButtonLabelWindow")
        self.setGeometry(100, 100, 300, 100)
        # x축 위치, y축 위치, 윈도우의 너비, 윈도우의 높이

        self.label = QLabel("Message : ", self)
        self.label.move(20, 20)
        self.label.resize(200, 20)
        # window(혹은 widget)의 사이즈를 변경 (x축 크기, y축 크기)

        btnSave = QPushButton("저장", self)
        btnSave.move(20, 50)
        btnSave.clicked.connect(self.btnSave_clicked)

        btnCancel = QPushButton("취소", self)
        btnCancel.move(120, 50)
        btnCancel.clicked.connect(self.btnCancel_clicked)

    def btnSave_clicked(self):
        self.label.setText("저장 되었습니다")

    def btnCancel_clicked(self):
        self.label.setText("취소 되었습니다")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ButtonLabelWindow()
    window.show()
    app.exec_()
```

![image-20210319163916336](PyQt.assets/image-20210319163916336.png)

## 4. QLineEdit 

> 한 줄의 텍스트를 입력하는데 사용된다.

| 시그널          | 시그널 발생 시점                                        |
| --------------- | ------------------------------------------------------- |
| testChanged()   | QLineEdit 객체에서 텍스트가 변경될 때 발생              |
| retuenPressed() | QLineEdit 객체를 통해 사용자가 엔터 키를 눌렀을 때 발생 |

```python
class CLineEditWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("ButtonLabelWindow")
        self.setGeometry(100,100,300,100)

        self.label = QLabel("이름 : ", self)
        self.label.move(20,20)
        self.label.resize(150,20)

        self.lineEdit = QLineEdit("", self)
        self.lineEdit.move(60,20)
        self.lineEdit.resize(200,20)
        self.lineEdit.textChanged.connect(self.lineEdit_textChanged)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        
        btnSave = QPushButton("저장", self)
        btnSave.move(10, 50)
        btnSave.clicked.connect(self.btnSave_clicked)

        btnClear = QPushButton("초기화", self)
        btnClear.move(100, 50)
        btnClear.clicked.connect(self.btnClear_clicked)

        btnQuit = QPushButton("닫기", self)
        btnQuit.move(190, 50)
        btnQuit.clicked.connect(self.btnQuit_clicked)
        #btnQuit.clicked.connect(QCoreApplication.instance().quit)  

    def btnSave_clicked(self):
        print(self.lineEdit.text())
        msg = "저장하시겠습니까?"
        msg += "\n이름 : " + self.lineEdit.text()
        buttonReply = QMessageBox.question(self, '저장', msg,
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                           #QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
            # 저장을 한다
            QMessageBox.about(self, "저장", "저장 되었습니다")
            self.statusBar.showMessage("저장 되었습니다")
        if buttonReply == QMessageBox.No:
            print('No clicked.')
        if buttonReply == QMessageBox.Cancel:
            print('Cancel')
            
    def btnClear_clicked(self):
        # 화면을 초기화 한다
        self.lineEdit.clear()

    def  btnQuit_clicked(self):
        # 프로그램을 종료한다
        sys.exit()

    def  lineEdit_textChanged(self):
        pass
        #self.statusBar.showMessage(self.lineEdit.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CLineEditWindow()
    window.show()
    app.exec_()
```

![image-20210322132650252](PyQt.assets/image-20210322132650252.png)

## 5. QRadioButton

> 사용자로부터 여러 가지 옵션 중 하나를 입력 받을 때 주로 사용

```python
class RadioButtonWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("PushButtonWindow")

        self.radio1 = QRadioButton("항목1", self)
        self.radio1.move(20, 20)
        self.radio1.setChecked(True)
        self.radio1.clicked.connect(self.radioButton_clicked)

        self.radio2 = QRadioButton("항목2", self)
        self.radio2.move(20, 40)
        self.radio2.clicked.connect(self.radioButton_clicked)

        self.radio3 = QRadioButton("항목3", self)
        self.radio3.move(20, 60)
        self.radio3.clicked.connect(self.radioButton_clicked)
        
        # self.statusBar = QStatusBar(self)
        # self.setStatusBar(self.statusBar)

    def radioButton_clicked(self):
        msg = ""
        if self.radio1.isChecked():
            msg = "항목1"
        elif self.radio2.isChecked():
            msg = "항목2"
        else:
            msg = "항목3"
            
        # self.statusBar.showMessage("선택된 항목 : " + msg)
        QMessageBox.about(self, "선택된 항목", msg+ " 선택됨 ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RadioButtonWindow()
    window.show()
    app.exec_()
```

![image-20210322133345874](PyQt.assets/image-20210322133345874.png)![image-20210322133429449](PyQt.assets/image-20210322133429449.png)

## 6. QGroupBox 

> 제목이 있는 네모 박스를 만듭니다.

```python
class GroupBoxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("PushButtonWindow")

        # QGoupBox 먼저 만들고 그룹박스내 위젯들(예: QRadioButton)을 추가
        groupBox = QGroupBox("항목 그룹", self)
        groupBox.move(10, 10)
        groupBox.resize(150, 80)

        self.radio1 = QRadioButton("항목1", self)
        self.radio1.move(20, 20)
        self.radio1.setChecked(True)	# default check
        self.radio1.clicked.connect(self.radioButton_clicked)

        self.radio2 = QRadioButton("항목2", self)
        self.radio2.move(20, 40)
        self.radio2.clicked.connect(self.radioButton_clicked)

        self.radio3 = QRadioButton("항목3", self)
        self.radio3.move(20, 60)
        self.radio3.clicked.connect(self.radioButton_clicked)

    def radioButton_clicked(self):
        msg = ""
        if self.radio1.isChecked():
            msg = "항목1"
        elif self.radio2.isChecked():
            msg = "항목2"
        else:
            msg = "항목3"
            
        QMessageBox.about(self, "선택된 항목", msg+ " 선택됨 ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GroupBoxWindow()
    window.show()
    app.exec_()
```

![image-20210322133559192](PyQt.assets/image-20210322133559192.png)

## 7. QCheckBox 

> 하나의 옵션만을 선택하는 QRadioButton와는 달리 여러 옵션을 동시에 선택할 수 있다.

```python
class CheckBoxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("체크박스 예제")

        self.checkBox1 = QCheckBox("항목1", self)
        self.checkBox1.move(20, 20)
        self.checkBox1.setChecked(True)
        self.checkBox1.clicked.connect(self.checkBoxStateChanged)

        self.checkBox2 = QCheckBox("항목2", self)
        self.checkBox2.move(20, 40)
        self.checkBox2.clicked.connect(self.checkBoxStateChanged)

        self.checkBox3 = QCheckBox("항목3", self)
        self.checkBox3.move(20, 60)
        self.checkBox3.clicked.connect(self.checkBoxStateChanged)

    def checkBoxStateChanged(self):
        msg = ""
        if self.checkBox1.isChecked():
            msg += "항목1 "
        if self.checkBox2.isChecked():
            msg += "항목2 "
        if self.checkBox3.isChecked():
            msg += "항목3"
            
        QMessageBox.about(self, "선택된 항목", msg+ " 선택됨 ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckBoxWindow()
    window.show()
    app.exec_()
```

![image-20210322143552480](PyQt.assets/image-20210322143552480.png)

## 8. QSpinBox 

> 값을 증가/감소시키는 데 사용하는 화살표와 값이 출력되는 부분, 입력 창에 직접 값을 입력도 가능

```python
class SpinBoxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("스핀박스  예제")

        label = QLabel("수량: ", self)
        label.move(10, 20)
        
        self.spinBox = QSpinBox(self)
        self.spinBox.move(40, 20)
        self.spinBox.resize(60, 20)
        self.spinBox.valueChanged.connect(self.spinBoxValueChanged)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def spinBoxValueChanged(self):
        val = self.spinBox.value()
        print(val)
        msg = "선택된 값: %s" %val
        print(msg)
        self.statusBar.showMessage(msg)
        # QMessageBox.about(self, "선택된 값", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpinBoxWindow()
    window.show()
    app.exec_()
```

![image-20210322144025797](PyQt.assets/image-20210322144025797.png)

## 9. QTableWidget

> 행과 열로 구성된 2차원 포맷 형태의 데이터를 사용하여 테이블 형태로 표시

```python
class TableWidgetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("TableWidget  예제")

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(400, 300)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(3)
        # setEditTriggers 아이템 항목을 수정할 수 없도록 설정
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        students = {
            'no': ['2018001', '2018002', '2018003'],
            'name': ['홍길동', '이순신', '김성철'],
            'group': ['1학년', '2학년', '3학년']
        }
        column_idx_lookup = {'no': 0, 'name': 1, 'group': 2}
        
        column_headers = ['학번', '이름', '학년']
        # column에 대한 라벨을 설정
        # row 방향에 대한 라벨을 설정할 때는 setVerticalHeaderLabels
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        for k, v in students.items():
            col = column_idx_lookup[k]
            print(k,v,col)
            for row, val in enumerate(v):
                item = QTableWidgetItem(val)
                if col == 2:
                    # setTextAlignment 메서드를 사용해 우측 정렬
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

                self.tableWidget.setItem(row, col, item)
		
        # 행과 열 크기를 각 위치에 저장된 아이템 길이에 맞춰 자동 조정
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableWidgetWindow()
    window.show()
    app.exec_()
```

![image-20210322144159878](PyQt.assets/image-20210322144209420.png)![image-20210322144221409](PyQt.assets/image-20210322144221409.png)