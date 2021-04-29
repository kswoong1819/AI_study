import sys, os, time
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\S1SECOM\Anaconda3\envs\pytoexe\Library\plugins\platforms'
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5 import uic
import pyqtgraph as pg

import serial
import logging
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
import numpy as np

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
path = r'D:\AI_study\Dali_viewer_2\dali_viewer.ui'
form_class = uic.loadUiType(path)[0]

ground_state = np.random.randn(120,160)
ground_state_show = ground_state
ground_state_crop = ground_state_show
im2Img = ground_state_show

start_flag = 0
stop_flag = 0
regression_cnt = 30
regression_flag = 0

ref_humantemp = 36.5
max_temp = 30
internal_temp = 30
center_temp = 35
max_x = 60
max_y = 60

max_x_ = 80
max_y_ = 60

bts_max = 30
bts_image = 10

ser = None

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        global ser
        global ground_state
        global und_state_show
        global ground_state_crop
        global im2Img

        global start_flag
        global stop_flag
        global regression_cnt
        global regression_flag

        global ref_humantemp
        global max_temp
        global internal_temp
        global center_temp 
        global max_x
        global max_y

        global max_x_
        global max_y_

        global bts_max    
        global bts_image

        super().__init__()
        self.setupUi(self)
        self.thread = QtCore.QThread()
        self.thread.start()
        self.plotgraph = PlotGraph()
        self.plotgraph.moveToThread(self.thread)

        self.start_btn.clicked.connect(self.plotgraph.plot_start)
        self.stop_btn.clicked.connect(self.plotgraph.plot_stop)

        self.horizontal_slider.setRange(0,160)
        self.horizontal_slider.setValue(80)
        self.horizontal_slider.valueChanged.connect(self.test)

        self.vertical_slider.setRange(0,120)
        self.vertical_slider.setValue(60)
        self.vertical_slider.valueChanged.connect(self.test2)

        self.image()
        self.text_insert()

        # ser = self.serial_init(ser)

    def test(self, v):
        self.plot_widget.canvas.ax.set_xlim(v-80, v+80)
        self.plot_widget.canvas.draw()

    def test2(self, v):
        self.plot_widget.canvas.set_ylim(v-60, v+60)
        self.plot_widget.canvas.draw()

    def image(self):
        global im
        x = [80]
        y = [60]
        s = 1000

        self.plot_widget.canvas.ax.set_xlim(50, 100)
        
        im = self.plot_widget.canvas.ax.imshow(ground_state_show, cmap = 'jet', animated = True)
        self.plot_widget.canvas.ax.scatter(x, y, marker='x', color='r', s=s, linewidth=5)
        self.plot_widget.canvas.ax.scatter(x, y, marker='x', color='w', s=s, linewidth=5)

        # ani = animation.FuncAnimation(self.plot_widget, self.update_fig, interval = 200)
        # self.plot_widget.canvas.scale(1.5)
        self.plot_widget.canvas.draw()

        # self.show()

    def text_insert(self):
        self.main_text.setFontPointSize(18)
        self.main_text.setFontWeight(QFont.Bold)
        # lexer.setColor(QColor("#ADD4FF"), 2)
        self.serial_num.setText("시리얼 포트 : " + str(ser))
        self.max_temp.setText("최고온도 : " + str(max_temp) + " ( x : " + str(max_x) + ", y : " + str(max_y) + " )")
        self.min_temp.setText("bb : " + " ( x : " + str(max_x_) + ", y : " + str(max_y_) + " )")
        self.any_temp.setText("aa : " + str(ser))
        

    def update_fig(self, *args):
        global ground_state_crop
        global file_save_flag
        
        im.set_data(ground_state_show)
        im.set_clim(ground_state_show.min(),ground_state_show.max())
        # scat.set_offsets([max_x_,max_y_])

        # if(file_save_flag == 1):
        #     time_text.set_text('Module(M:%.2f,C:%.2f), Image(M:%.2f,C:%.2f) (Saving)' % (max_temp,center_temp,ground_state_crop.max(),ground_state[60,80]))
        # else:
        #     time_text.set_text('Module(M:%.2f,C:%.2f), Image(M:%.2f,C:%.2f)' % (max_temp,center_temp,ground_state_crop.max(),ground_state[60,80]))
        
        return im


    def serial_init(self, *args):
        #ser.close()
        current_port = self.findPort()
        if 1:
            print('AutoPort:', current_port);
            ser = serial.Serial(port=current_port,baudrate=3000000, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
        else:
            ser = serial.Serial(port='COM9',baudrate=3000000, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
            print('HardCoding Port:COM9');
        
        ser.set_buffer_size(rx_size = 2560000, tx_size = 2560000)
        packet = bytearray()
        packet.append(0xaa)
        packet.append(0x55)
        packet.append(0x00)
        packet.append(0x00) 
        packet.append(0x00)
        packet.append(0x01)
        packet.append(0x4f)
        packet.append(0x7e)
        packet.append(0x00)
        packet.append(0x00)
        packet.append(0x00)
        packet.append(0x0d)
        packet.append(0x0a)
        ser.write(packet)
        
        packet2 = bytearray()
        packet2.append(0xaa)
        packet2.append(0x55)
        packet2.append(0x00)
        packet2.append(0x09)
        packet2.append(0x00)
        packet2.append(0x01)
        packet2.append(0xd1)
        packet2.append(0xef)
        packet2.append(0x00)
        packet2.append(0x00)
        packet2.append(0x00)
        packet2.append(0x0d)
        packet2.append(0x0a)
        ser.write(packet2)
        
        return ser

    def findPort(self):
        # Find first available EiBotBoard by searching USB ports.
        # Return serial port object.
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            return None
        if comports:
            com_ports_list = list(comports())
            ebb_port = None
            for port in com_ports_list:
                if port[1].startswith("USB"):
                    ebb_port = port[0]  # Success; EBB found by name match.
                    break  # stop searching-- we are done.
            if ebb_port is None:
                for port in com_ports_list:
                    if port[2].startswith("USB VID:PID=04D8:FD92"):
                        ebb_port = port[0]  # Success; EBB found by VID/PID match.
                        break  # stop searching-- we are done.
            return ebb_port 
    

class PlotGraph(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.stop_flag = False

    def plot_start(self):
        print("start")
        self.simulate(ser)
        # while True:
        #     loop = QtCore.QEventLoop()
        #     QtCore.QTimer.singleShot(10, loop.quit) # 5000 ms
        #     loop.exec_()
        if self.stop_flag:
            self.stop_flag = False
            # break

    def plot_stop(self):
        print("end")
        self.stop_flag = True

    def simulate(self, *args):
        global max_x
        global max_y
        global max_temp, center_temp
        global ground_state
        global ground_state_show
        global ground_state_crop
        global internal_temp
        global max_x_
        global max_y_
        framecnt = 100
        cnt = 0
        ##### Buffer reset####
        while(cnt<120):
            if self.stop_flag:
                break
            subcnt = 0
            while(1):
                stx1 = ser.read(1).hex()      
                while(len(stx1) < 1):
                    stx1+=ser.read(1-len(stx1)).hex()

                if(stx1 == 'aa'):    
                    stx2 = ser.read(1).hex()
                    while(len(stx2) < 1):
                        stx2+=ser.read(1-len(stx2)).hex()
                        
                    if(stx2=='55'):
                        if( subcnt > 0 and subcnt < 10):
                            logging.info('subcnt=%d',subcnt)
                        elif(subcnt>0):
                            print('subcnt=',subcnt)
                        break
                    else:
                        if(len(stx2) > 0):
                            print('stx2:',stx2)
                else:
                    subcnt = subcnt+1
                    continue
            
            status = ser.read(1).hex()
            while(len(status) < 1):
                status+=ser.read(1-len(status)).hex()
                
            cmd = ser.read(1).hex()
            while(len(cmd) < 1):
                cmd+=ser.read(1-len(cmd)).hex()
                
            # if(cmd != '25' and cmd != '0d' and cmd != '0e' and cmd != '1f'):
            #     print('cmd',cmd)
                
            if (cmd != '25' and cmd != '24'):
                if(cmd == '0d'):
                    datalen = ser.read(2).hex()
                    while(len(datalen)<2):
                        datalen+=ser.read(2-len(datalen)).hex()
                        
                    crc1 = ser.read(2).hex()
                    while(len(crc1)<2):
                        crc1+=ser.read(2-len(crc1)).hex()
                    
                    tmp = ser.read(2).hex()
                    while(len(tmp)<2):
                        tmp+=ser.read(2-len(tmp)).hex()
                        
                    internal_temp = int('0x' + tmp[0:2]+tmp[2:4],0)
                    internal_temp = 190.65 - 0.02164 * internal_temp
                    
                    tmp = ser.read(6).hex()
                    while(len(tmp)<6):
                        tmp+=ser.read(6-len(tmp)).hex()

                    tmp = ser.read(4).hex()
                    while(len(tmp)<4):
                        tmp+=ser.read(4-len(tmp)).hex()
                        
                    crc2 = ser.read(2).hex()
                    while(len(crc2)<2):
                        crc2+=ser.read(2-len(crc2)).hex()

                    etx = ser.read(2).hex()
                    while(len(etx)<2):
                        etx+=ser.read(2-len(etx)).hex()
                        
                    ground_state_show = ground_state
                    ground_state_crop = ground_state[40:80,60:100] #세로120, 가로160
                    max_x_ = max_x
                    max_y_ = max_y
                    
                    max_y_ = np.argmax(ground_state_crop) / 40 + 40
                    max_x_ = np.argmax(ground_state_crop) % 40 + 60
                    #print('x:',max_x_, 'y:', max_y_)
                    ## 임시 BlackBody 모델이 0x0000 들어와서 주석처리함
                    #if(etx !='0d0a'):
                    #print('0x0d : datalen',datalen,' crc2', crc2, 'etx',etx)
                    continue
                    
                elif(cmd == '0e'):
                    datalen = ser.read(2).hex()
                    while(len(datalen)<2):
                        datalen+=ser.read(2-len(datalen)).hex()
                        
                    crc1 = ser.read(2).hex()
                    while(len(crc1)<2):
                        crc1+=ser.read(2-len(crc1)).hex()
                
                    max_x = ser.read(1).hex()
                    while(len(max_x)<1):
                        max_x+=ser.read(1-len(max_x)).hex()
                        print(max_x)
                    max_x = int('0x'+max_x,0)
                    max_y = int('0x'+ser.read(1).hex(),0)
                    
                    tmp = ser.read(2).hex()
                    max_temp = int('0x' + tmp[0:2]+tmp[2:4],0)

                    center_x = int('0x'+ser.read(1).hex(),0)
                    center_y = int('0x'+ser.read(1).hex(),0)
                    tmp = ser.read(2).hex()
                    center_temp = int('0x' + tmp[0:2]+tmp[2:4],0)
                    
                    min_x = int('0x'+ser.read(1).hex(),0)
                    min_y = int('0x'+ser.read(1).hex(),0)
                    tmp = ser.read(2).hex()
                    min_temp = int('0x' + tmp[0:2]+tmp[2:4],0)
                    
                    any_x = int('0x'+ser.read(1).hex(),0)
                    any_y = int('0x'+ser.read(1).hex(),0)
                    tmp = ser.read(2).hex()
                    any_temp = int('0x' + tmp[0:2]+tmp[2:4],0)
                    
                    max_temp = (max_temp/10) - 100
                    center_temp = (center_temp/10) - 100
                    
                    crc2 = ser.read(2).hex()
                    while(len(crc2)<2):
                        crc2+=ser.read(2-len(crc2)).hex()
                    etx = ser.read(2).hex()
                    while(len(etx)<2):
                        etx+=ser.read(2-len(etx)).hex()
                    if(etx !='0d0a'):
                        print('0x0e : crc2', crc2, 'etx',etx)
                    continue
                elif(cmd == '1f'):
                    datalen = ser.read(2).hex()
                    while(len(datalen)<2):
                        datalen+=ser.read(2-len(datalen)).hex()
                    crc1 = ser.read(2).hex()
                    while(len(crc1)<2):
                        crc1+=ser.read(2-len(crc1)).hex()    
                    status = ser.read(1).hex()
                    while(len(status) < 1):
                        status+=ser.read(1-len(status)).hex()

                    crc2 = ser.read(2).hex()
                    while(len(crc2)<2):
                        crc2+=ser.read(2-len(crc2)).hex()
                    etx = ser.read(2).hex()
                    while(len(etx)<2):
                        etx+=ser.read(2-len(etx)).hex()
                                
                    while(etx != '0d0a'):
                        etx = ser.read(2).hex()
                        while(len(etx)<2):
                            etx+=ser.read(2-len(etx)).hex()
                    if(etx !='0d0a'):
                        print('cmd(1f) error etx',datalen,':', etx)     
                    continue
                else:
                    print('cmd error!:',cmd)
                    etx = ser.read(2).hex()
                    while(len(etx)<2):
                        etx+=ser.read(2-len(etx)).hex()
                                
                    while(etx != '0d0a'):
                        etx = ser.read(2).hex()
                        while(len(etx)<2):
                            etx+=ser.read(2-len(etx)).hex()
                    print('cmd error etx',etx)     
                    continue
                continue
            
            datalen = ser.read(2).hex()
            while(len(datalen)<2):
                datalen+=ser.read(2-len(datalen)).hex()
                
            crc1 = ser.read(2).hex()
            while(len(crc1)<2):
                crc1+=ser.read(2-len(crc1)).hex()
            
            linenum = ser.read(1).hex()
            while(len(linenum) < 1):
                linenum+=ser.read(1-len(linenum)).hex()
            lineidx = int('0x'+linenum,0)
            
            if(lineidx < 120 and lineidx >= 0):
                cnt = cnt +1
                rcv_data=ser.read(320)
                while(len(rcv_data)<320):
                    rcv_data+=ser.read(320-len(rcv_data))
                linebuffer= np.frombuffer(rcv_data,">u2")
                linebuffer = linebuffer/10 -273
            else:
                print('cmd', cmd, 'linidx',lineidx)
                
            crc2 = ser.read(2).hex()
            while(len(crc2)<2):
                crc2+=ser.read(2-len(crc2)).hex()
            
            etxerrorflag = 0
            while(1):
                etx1 = ser.read(1).hex()
                while(len(etx1) < 1):
                    etxerrorflag = 1
                    etx1+=ser.read(1-len(etx1)).hex()
                
                if(etx1 == '0d'):
                    etx2 = ser.read(1).hex()
                    while(len(etx2) < 1):
                        etxerrorflag = 1
                        etx2+=ser.read(1-len(etx2)).hex()
                        
                    if(etx2=='0a'):
                        if(etxerrorflag == 0):
                            ground_state[lineidx]=linebuffer
                        break
                    else:
                        etxerrorflag = 1
                        print('0x24 25 error etx2',etx1,',',etx2)
                else:
                    etxerrorflag= 1
        
        framecnt = framecnt - 1
        if(framecnt==0):
            framecnt = 100
            tmp = ser.read(10000).hex()
            while(len(tmp)>0):
                tmp = ser.read(10000).hex()
            print('Buffer reset!!')


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()