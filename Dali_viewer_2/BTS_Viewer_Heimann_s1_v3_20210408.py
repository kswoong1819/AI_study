# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 17:58:57 2020

@author: S1SECOM
"""
import serial
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import datetime
import math
import statistics

import threading
import time
import logging
from threading import Thread

#logging.basicConfig(level=logging.DEBUG,format="%(asctime)s.%(msecs)03d[%(levelname)-8s]:%(created).6f %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
from matplotlib.widgets import CheckButtons
import csv


class ExTimer(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 
        # default delay set.. 
        self.delay = 60
        self.state = True 
        self.handler = None 
    def setDelay(self, delay): 
        self.delay = delay 
    def run(self): 
        while self.state: 
            time.sleep( self.delay ) 
            if self.handler != None: 
                self.handler() 
    def end(self): 
        self.state = False 
    def setHandler(self, handler): 
        self.handler = handler 

def timerHandler():
    bts_image = ground_state.reshape(32*32)
   # print( "(Timer)MAX_temp : %.2f, 1pix : %.2f" %(max_temp,bts_image[0]/100) )
    file_append(fy,fmo,fd,fh,fmi,fs,BTSNAME,max_temp,max_temp2,bts_image)
 

def file_init(fy,fmo,fd,fh,fmi,fs):
    global fileheader
    fn = open("%s_%04d%02d%02d_%02d%02d%02d.data"\
              % (fileheader,fy,fmo,fd,fh,fmi,fs),"w+")
    fn.write("filename,Sensorname_SensorNum_Blackbody(deg)_Dist(cm)_AmbientTemp(deg)_date\n")
    fn.write("date,time,modulename,max,center,Image\n")
    fn.close()
    print("Filename:%s_%04d%02d%02d_%02d%02d%02d.data"\
              % (fileheader,fy,fmo,fd,fh,fmi,fs))
    
def file_append(fy,fmo,fd,fh,fmi,fs,BTSNAME,bts_max,bts_center,bts_image):
    global fileheader
    #logging.info('filewrite_start')
    
    #with open("%s_report_%d%d%d%d%d%d.data"\
    ##          % (fileheader,fy,fmo,fd,fh,fmi,fs),"a+", encoding='utf-8') as f:
    #    writer = csv.writer(f, delimiter=',')
    #    writer.writerow("%d-%d-%d,%d:%d:%d,%s,%.2f,%.2f,%.2f"\
    #         %(datetime.datetime.now().year,datetime.datetime.now().month ,datetime.datetime.now().day,\
    #            datetime.datetime.now().hour,datetime.datetime.now().minute ,datetime.datetime.now().second,\
    #                BTSNAME ,bts_max,bts_max2,internal_temp))
    #    writer.writerow(bts_image/100)
    
    fn = open("%s_%04d%02d%02d_%02d%02d%02d.data"\
              % (fileheader,fy,fmo,fd,fh,fmi,fs),"a+")
    fn.write("%d-%d-%d,%d:%d:%d,%s,%.2f,%.2f,"\
             %(datetime.datetime.now().year,datetime.datetime.now().month ,datetime.datetime.now().day,\
                datetime.datetime.now().hour,datetime.datetime.now().minute ,datetime.datetime.now().second,\
                    BTSNAME ,bts_max,bts_center))
    #for i in range(120*160):
    #    fn.write(",%.2f" %(bts_image[i]/100))
    #fn.write(np.array2string(bts_image[0:120*160]/100,separator=','))
    fn.write(','.join(map(str,bts_image[0:32*32])))
        
    fn.write("\n")
    fn.close()
    #logging.info('filewrite_end')
    
def polynomial_regression_pow3(indata):
    
    #indata = indata - (ref_humantemp - 34)
    ret = 0.0021*math.pow(indata,3) - 0.1538*math.pow(indata,2)+3.8196*indata + 4.1589
    #print("ret =%.2f"%ret)
    if ret > 34 and ret < 42:
        #human ref update
        ref_humantemp = ref_humantemp + (1/10) * (indata - ref_humantemp)
        
        ####human regression
        indata = indata - (ref_humantemp - 34)
        
        #print("indata=%.2f, ref=%.2f"%(indata,ref_humantemp))
        ###polynomial regression
        ret = 0.0021*math.pow(indata,3) - 0.1538*math.pow(indata,2)+3.8196*indata + 4.1589
    
    return ret

def polynomial_regression_pow6(indata, internal_t):
    global ref_humantemp
    global ref_environment
    global regression_cnt
    global regression_flag
    
    global ground_state_show
    global refImg
    global backgroundImg

    global im2Img
    global im3Img
    global im4Img
    
    global humanDelta
    global Delta
    global environmentDelta
    currentImg = ground_state_show
    
    if regression_cnt == 0 and regression_flag == 0:
        
        # Init Background
        refImg = ground_state_show
        backgroundImg = ground_state_show
        im2Img = ground_state_show
        im3Img = ground_state_show
        im4Img = ground_state_show
        regression_flag = 1
        ref_environment = 0
        print('regression_flag done')
    elif regression_cnt !=0 and regression_flag == 0:
        regression_cnt = regression_cnt-1
    else:
        backgroundImg = backgroundImg + (1/1000) *(currentImg - backgroundImg)
        ######
        #
        #backgroundImg = currentImg - backgroundImg
        
        
    ##init
        
    if regression_flag == 0:
      #  print("INIT ing, %d"%regression_cnt)
        ###polynomial regression
        #if(indata <40 and indata >30):
         #   ret = -0.00002473677282743840*math.pow(indata,6) + 0.00452498105771539000*math.pow(indata,5)\
        #        - 0.34295206746532400000*math.pow(indata,4) + 13.79168083481320000000*math.pow(indata,3)\
        #        - 310.52369338559900000000*math.pow(indata,2) + 3713.26487080404000000000*indata - 18398.25954399820000000000
        #else:
        ret = indata
        
        if ret >30 and ret <42:
         #   print("internal=%.2f, before=%.2f"%(internal_t,ret))
            ref_humantemp = ref_humantemp + (1/3) * (ret - ref_humantemp)
        #    print("ref=%.2f"%(ref_humantemp))
            
        ret = ret - (ref_humantemp - 36.5)
        
        #print("Error")
    else:
        #indata = indata - (ref_humantemp - 32.3)
        ###polynomial regression
        #if(indata <40 and indata >30):
        #    poly_ret = -0.00002473677282743840*math.pow(indata,6) + 0.00452498105771539000*math.pow(indata,5)\
        #        - 0.34295206746532400000*math.pow(indata,4) + 13.79168083481320000000*math.pow(indata,3)\
        #        - 310.52369338559900000000*math.pow(indata,2) + 3713.26487080404000000000*indata - 18398.25954399820000000000
            #ret = 0.0000548658768195764*math.pow(indata,6)-0.0111338290044785*math.pow(indata,5)\
            #    + 0.939275847920264*math.pow(indata,4)-42.1505844218716*math.pow(indata,3)\
            #        +1060.89850554761*math.pow(indata,2)-14196.199974408*indata+78920.5830976677
        #else:
        poly_ret = indata
  
          ####human regression
        
        
        
        
        humanDelta = 36.5 - ref_humantemp
        environmentDelta = ref_environment
        
        humanDeltaAlpha = 1
        #print(np.abs(environmentDelta))
        Delta = humanDelta * humanDeltaAlpha + environmentDelta * (1-humanDeltaAlpha)
        #print('Delta: %.2f'%Delta,'h:%.2f'%humanDelta,' e:%.2f'%environmentDelta)
        ret = poly_ret + Delta#- (ref_humantemp - 36.5)
        
        #print('ret:%.2f,P_ret:%.2f,Delta%.2f'%(ret,poly_ret,Delta))
        if internal_t < 30:
            if ret >30 and ret <41:
                #print("internal=%.2f, before=%.2f"%(internal_t,ret))
                ref_humantemp = ref_humantemp + (1/3) * (poly_ret - ref_humantemp)
                #print("ref=%.2f"%(ref_humantemp))
                
        elif ret > 35.5 and ret < 37.3:
            #human ref update
            ref_humantemp = ref_humantemp + (1/5) * (poly_ret - ref_humantemp)
            #print("poly_ret=%.2f, ref=%.2f"%(poly_ret,ref_humantemp))
        else:
            ref_humantemp = ref_humantemp + (1/10000) * (poly_ret - ref_humantemp)
            #print("HIGH poly_ret=%.2f, ref=%.2f"%(poly_ret,ref_humantemp))
        
        
        im2Img = backgroundImg
        im3Img = currentImg - backgroundImg
        im3Img = np.abs(im3Img)
        refdeltaimg = refImg - backgroundImg
        
                
        #im3Img = im3Img + np.abs(refdeltaimg)
        

        
        #print(im3Img.max())
        
        #im4Img = im3Img>1 
        im4ImgTemp = np.where(im3Img>1,1,0)
        
        arrayidx = 0
        deltacntarray = np.zeros(6*8)
        deltaarray = np.zeros(6*8)
        for y in range(0,6):#20*6 = 120
            for x in range(0,8):#20*8 = 160
                deltacnt = 0
                deltasum = 0
                deltasumcnt = 0
                for dy in range(0,20):
                    for dx in range(0,20):
                        #print('    y:',y*20 + dy,'x:',x*20+dx)
                        
                        if im3Img[y*20 + dy][x*20+dx]<1: ## currentImg와 backgroundImg 차분값(움직임 확인) 
                            # 움직임만 없으면 모든 편차 다 구하기
                            deltasum = deltasum + refdeltaimg[y*20 + dy][x*20+dx]# 기준(refImg)와 backgroundImg 편차
                            deltasumcnt = deltasumcnt+1
                            #print(np.abs(refdeltaimg))
                            
                            if np.abs(refdeltaimg[y*20 + dy][x*20+dx]) < np.abs(environmentDelta):
                                #움직임이 없으면서 기준Img보다 적게 변한 pixel 찾기
                                deltacnt = deltacnt+1
                        
                if(deltasumcnt > 0):
                    deltasum = deltasum/(deltasumcnt)
                
                deltacntarray[arrayidx] = deltacnt
                deltaarray[arrayidx] = deltasum
                arrayidx = arrayidx+1
        
        deltacntarrayMaxIdx = deltacntarray.argmax()
        
        
        y = int(deltacntarrayMaxIdx/8)
        x = int(deltacntarrayMaxIdx - y*8)
        
        #print('max:',deltacntarray.max(),'MinIdx:',deltacntarrayMaxIdx,'min:',deltacntarray.max(),'/delta:%.2f'%deltaarray[deltacntarrayMaxIdx])
        for dy in range(0,20):
            for dx in range(0,20):
                im4ImgTemp[y*20 + dy][x*20+dx] = 10
        ref_environment = deltaarray[deltacntarrayMaxIdx]
        
        im4Img = im4ImgTemp
    return ret

def findPort():
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
            if port[1].startswith("Sili"):
                ebb_port = port[0]  # Success; EBB found by name match.
                break  # stop searching-- we are done.
        if ebb_port is None:
            for port in com_ports_list:
                if port[2].startswith("Silicon"):
                    ebb_port = port[0]  # Success; EBB found by VID/PID match.
                    break  # stop searching-- we are done.
        return ebb_port 
    
def serial_init(*args):
    #ser.close()
    current_port = findPort()
    if 1:
        print('AutoPort:', current_port);
        #ser = serial.Serial(port=current_port,baudrate=115200, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
        ser = serial.Serial(port=current_port,baudrate=500000, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
       # ser = serial.Serial(port=current_port,baudrate=256000, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
    else:
#        ser = serial.Serial(port='COM9',baudrate=115200, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
        ser = serial.Serial(port='COM9',baudrate=256000, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
        print('HardCoding Port:COM9');
    
    ser.set_buffer_size(rx_size = 2560000, tx_size = 2560000)
    if 0:
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
    else:
        packet = bytearray()
        packet.append(0x53)#STX1:S
        packet.append(0xf1)#STX2
        packet.append(0x09)#len
        packet.append(0x00)#len
        packet.append(0x04)#열화상
        packet.append(0x53)#S
        packet.append(0x45)#E
        packet.append(0x4e)#N
        packet.append(0x44)#D
        packet.append(0x5f)#_
        packet.append(0x5f)#_
        packet.append(0x4f)#O
        packet.append(0x4e)#N
        packet.append(0x89)#CHECKSUM
        packet.append(0x45)#ETX:E
        
        
        ser.write(packet)
    
    
    return ser
    



def update_fig(*args):
    #global backgroundImg
    #simulate(ground_state,ser)#, 1000, 1.0)
#    time_text.set_text('S1_MAX[before:%.2f,after:%.2f], IN_T[%.2f]' % (max_temp, max_temp2,internal_temp))
    
    global file_save_flag
    im.set_data(ground_state_show)
    im.set_clim(ground_state_show.min(),ground_state_show.max())
    scat.set_offsets([max_x,max_y])
    
    im2.set_data(im2Img)
    im2.set_clim(im2Img.min(),im2Img.max())
        
    if(file_save_flag == 1):
        time_text.set_text('MAX:%.2f,CENTER:%.2f (Saving)' % (ground_state_show.max(),ground_state[16,16]))
    else:
        time_text.set_text('MAX:%.2f,CENTER:%.2f' % (ground_state_show.max(),ground_state[16,16]))
    
    #print(ground_state.max())
    #im.colorbar()
    plt.autoscale(enable=True)
    if regression_flag == 1:
        #time_text.set_text('S1_MAX[before:%.2f,after:%.2f], IN_T[%.2f]' % (max_temp, max_temp2,internal_temp))
        time_text.set_text('before:%.2f,after:%.2f,hD:%.2f,eD:%.2f,D:%.2f' % (ground_state_show.max(), max_temp2,humanDelta,environmentDelta, Delta))
        
        im2.set_data(im2Img)
        im2.set_clim(im2Img.min(),im2Img.max())
        
        
        #print('max',im4Img.max(),'min',im4Img.min())
    
    return im

def threaded_function(arg):
    global file_save_flag
    global start_flag
    global stop_flag
    global ground_state_show
    global framecnt
    global save_cnt
    framecnt = 100
    file_save_flag = 0
    start_flag = 0
    stop_flag = 0
    save_cnt = 50
    while(1):
        if(start_flag == 1):
            start_flag = 0
            file_save_flag = 1
            
            BTSNAME = 'HEI01'
            fy = datetime.datetime.now().year
            fmo = datetime.datetime.now().month
            fd = datetime.datetime.now().day
            fh = datetime.datetime.now().hour
            fmi = datetime.datetime.now().minute
            fs = datetime.datetime.now().second
            file_init(fy,fmo,fd,fh,fmi,fs)
            
            save_cnt = 50
            
        if (save_cnt == 0):
            print('save stop')
            save_cnt = 50
            stop_flag = 0
            file_save_flag = 0
        if(stop_flag == 1):
            #print('save stop')
            stop_flag = 0
            file_save_flag = 0
            
            
        simulate(ser)
#        print( "(Timer)MAX_temp : %.2f, 1pix : %.2f" %(max_temp,bts_image[0]/100) )
        if(file_save_flag == 1):
            if(check_active):
                save_cnt = save_cnt -1
            file_append(fy,fmo,fd,fh,fmi,fs,BTSNAME,max_temp,max_temp2,ground_state_show.reshape(32*32))


def submit1(text):
    #ydata = eval(text)
    global fileheader
    global fileheader1
    global fileheader2
    global fileheader3
    global fileheader4
    fileheader1 = text
    fileheader = text+'_'+fileheader2+'_'+fileheader3+'_'+fileheader4
    print('change(fileheader1):',text);
    print(fileheader)
def submit2(text):
    #ydata = eval(text)
    global fileheader
    global fileheader1
    global fileheader2
    global fileheader3
    global fileheader4
    print('change(fileheader2):',text);
    fileheader2 = text
    fileheader = fileheader1+'_'+text+'_'+fileheader3+'_'+fileheader4
    print(fileheader)
def submit3(text):
    #ydata = eval(text)
    global fileheader
    global fileheader1
    global fileheader2
    global fileheader3
    global fileheader4
    fileheader3 = text
    print('change(fileheader3):',text);
    fileheader = fileheader1+'_'+fileheader2+'_'+text+'_'+fileheader4
    print(fileheader)
def submit4(text):
    #ydata = eval(text)
    global fileheader
    global fileheader1
    global fileheader2
    global fileheader3
    global fileheader4
    fileheader4 = text
    print('change(fileheader4):',text);
    fileheader = fileheader1+'_'+fileheader2+'_'+fileheader3+'_'+text
    print(fileheader)
    
def CheckBox_clicked(click):
    global check_active
    
    check_active = not check_active
    
    if(check_active):
        packet = bytearray()
        packet.append(0x53)#STX1:S
        packet.append(0xf1)#STX2
        packet.append(0x09)#len
        packet.append(0x00)#len
        packet.append(0x04)#열화상
        packet.append(0x53)#S
        packet.append(0x45)#E
        packet.append(0x4e)#N
        packet.append(0x44)#D
        packet.append(0x5f)#_
        packet.append(0x5f)#_
        packet.append(0x4f)#O
        packet.append(0x4e)#N
        packet.append(0x89)#CHECKSUM
        packet.append(0x45)#ETX:E
        
        ser.write(packet)
    else:
        packet = bytearray()
        packet.append(0x53)#STX1:S
        packet.append(0xf1)#STX2
        packet.append(0x09)#len
        packet.append(0x00)#len
        packet.append(0x04)#열화상
        packet.append(0x53)#S
        packet.append(0x45)#E
        packet.append(0x4e)#N
        packet.append(0x44)#D
        packet.append(0x5f)#_
        packet.append(0x4f)#O
        packet.append(0x46)#F
        packet.append(0x46)#F
        packet.append(0x68)#CHECKSUM
        packet.append(0x45)#ETX:E
        
        ser.write(packet)
    print(check_active)
    
    
def main():
    #data = bytearray([0xAA, 0x55, 0x00, 0x00, 0x00, 0x01, 0x4F, 0x7E, 0x00, 0x00, 0x00, 0x0D, 0x0A])
    #ser.write(b'\0xaa\0x55\0x00\0x00\0x00\0x01\0x4f\0x7e\0x00\0x00\0x00\0x0d\0x0a')
    #ser.write(b'\0xaa\0x55\0x00\0x00\0x00\0x01\0x4f\0x7e\0xff\0x1e\0xf0\0x0d\0x0a')
    #ser.write(b'\0xAA\0x55\0x00\0x00\0x00\0x01\0x4F\0x7E\0xFF\0x1E\0xF0\0x0D\0x0A')
    global ser
    global time_text
    global visit
    global im
    global im2
    global im3
    global im4
    
    global scat
    global scat2
    global ground_state
    global fn
    global BTSNAME
    global fy,fmo,fd,fh,fmi,fs,bts_max,bts_image
    global max_temp, max_temp2
    global internal_temp
    global max_x, max_y
    global ref_humantemp
    global regression_cnt
    global regression_flag
    global button
    
    global start_flag
    global stop_flag
    global ground_state_show
    global fileheader
    global fileheader1
    global fileheader2
    global fileheader3
    global fileheader4
    global check_active
    
    global backgroundImg
    global im2Img
    global im3Img
    global im4Img
    start_flag = 0
    stop_flag = 0
    regression_cnt = 30;
    regression_flag = 0;
    
    ref_humantemp = 36.5
    max_temp = 30
    internal_temp = 30
    max_temp2 = 35
    max_x = 60
    max_y = 60
    
    bts_max = 30
    bts_image = 10
    BTSNAME = 'HEI'
    fy = datetime.datetime.now().year
    fmo = datetime.datetime.now().month
    fd = datetime.datetime.now().day
    fh = datetime.datetime.now().hour
    fmi = datetime.datetime.now().minute
    fs = datetime.datetime.now().second
    ground_state = np.random.randn(32,32)
    ground_state_show = ground_state
    im2Img = ground_state_show;

    initial_text1 = "HEI01"# Heimann_Sensolution
    initial_text2 = "30"
    initial_text3 = "50"
    initial_text4 = "25"

    fileheader1 =initial_text1
    fileheader2 =initial_text2
    fileheader3 =initial_text3
    fileheader4 =initial_text4
    initial_text =initial_text1+'_'+initial_text2+'_'+initial_text3+'_'+initial_text4
    fileheader = initial_text
    #print(fileheader)
   
    visit = np.zeros(120)
    

    ser = None
    ser = serial_init(ser)
    fig = plt.figure()

    time_text = fig.text(0.03, 0.9, 'MAX = 0', fontsize=18)#, transform=fig.transAxes)
    
    

    
    ax2 = fig.add_subplot(1, 2, 2)
    plt.autoscale(enable=True)

    x = [16]
    y = [16]
    s = [200]
    scat2 = plt.scatter(x,y,s=s,marker='x',facecolors='red',linewidth=5)#,linestyle=':')
    #im = plt.imshow(ground_state,interpolation='gaussian', cmap = 'jet',animated = True)
    im2 = ax2.imshow(ground_state_show,interpolation='gaussian',cmap = 'jet',animated = True)
    
    #scat = plt.scatter(x,y,facecolors='none',s=s,linewidth=5,edgecolors='white')#,linestyle='--')
    ax1 = fig.add_subplot(1, 2, 1)
    plt.autoscale(enable=True)
    
    
    s = [1000]
    scat = plt.scatter(x,y,s=s,marker='x',facecolors='white',linewidth=5)#,linestyle=':')
    
    im = ax1.imshow(ground_state_show,cmap = 'jet',animated = True)
    
    
    #plt.colorbar()
    #plt.clim(40000, 70000)
    plt.clim(2900, 3100)
   
    ###
    button_axcut={}
    button={}

    button_axcut['FileSave'] = plt.axes([0.7,0, 0.1, 0.05])
    button['FileSave'] = Button(button_axcut['FileSave'] ,'FileSave', color='white')

    button_axcut['Stop'] = plt.axes([0.81,0, 0.07, 0.05])
    button['Stop'] = Button(button_axcut['Stop'] ,'Stop', color='white')

    button['FileSave'].on_clicked(Start_clicked)
    button['Stop'].on_clicked(Stop_clicked)
    
    
    axbox1 = plt.axes([0.1, 0.0, 0.13, 0.05])
    text_box1 = TextBox(axbox1, 'Sensor', initial=initial_text1)
    text_box1.on_submit(submit1)
    
    axbox2 = plt.axes([0.33, 0.0, 0.05, 0.05])
    text_box2 = TextBox(axbox2, 'BT(deg)', initial=initial_text2)
    text_box2.on_submit(submit2)
    
    axbox3 = plt.axes([0.48, 0.0, 0.05, 0.05])
    text_box3 = TextBox(axbox3, 'Dist(cm)', initial=initial_text3)
    text_box3.on_submit(submit3)

    axbox4 = plt.axes([0.63, 0.0, 0.05, 0.05])
    text_box4 = TextBox(axbox4, 'AT(deg)', initial=initial_text4)
    text_box4.on_submit(submit4)
    #######열원체 온도. 환경온도 ? 추가 필요
    
    check_active = 1    
    checklabels = [' ']
    checkvisibility = [True]

    axcheckbox = plt.axes([0.9, 0.0, 0.2, 0.2])
    Check_Box = CheckButtons(axcheckbox, checklabels,checkvisibility)
    Check_Box.on_clicked(CheckBox_clicked)
###
    ani = animation.FuncAnimation(fig, update_fig, interval = 200)

    thread = Thread(target = threaded_function, args = (10, ))
    thread.start()
    

    plt.show()
    
def simulate(*args):
    global max_x
    global max_y
    global max_temp,max_temp2
    global ground_state
    global ground_state_show
    global internal_temp
    global framecnt
    global im2Img
    
    
    #print("start")
    cnt = 0
    ##### Buffer reset####
    #print('cnt:',cnt)
    subcnt = 0
    while(1):
            stx1 = ser.read(1).hex()
            while(len(stx1) < 1):
                stx1+=ser.read(1-len(stx1)).hex()
            
            #print("stx1 receive")
            if(stx1 == '53'):#'S'   0x53
                stx2 = ser.read(1).hex()
                while(len(stx2) < 1):
                    stx2+=ser.read(1-len(stx2)).hex()
                    
                if(stx2=='f3'):# 대소문자 차이 있음!
                    if( subcnt > 0 and subcnt < 10):
                        logging.info('subcnt=%d',subcnt)
                    elif(subcnt>0):
                        print('subcnt=',subcnt)
                    break;
                else:
                    #subcnt = subcnt+1
                    if(len(stx2) > 0):
                       print('stx2:',stx2)
            else:
                subcnt = subcnt+1
#                if(len(stx1) > 0):
                   #print('stx1 error stx1:',stx1)
                continue;
            
    datatype = ser.read(1).hex()
    while(len(datatype) < 1):
        datatype+=ser.read(1-len(datatype)).hex()
                
    rcv_data=ser.read(32*32*2)
    while(len(rcv_data)<32*32*2):
        rcv_data+=ser.read(32*32*2-len(rcv_data))
        
    filemax = ser.read(2).hex()
    while(len(datatype) < 2):
        filemax+=ser.read(1-len(filemax)).hex()
        
    filemax_x = ser.read(1).hex()
    while(len(filemax_x) < 1):
        filemax_x+=ser.read(1-len(filemax_x)).hex()
    filemax_y = ser.read(1).hex()
    while(len(filemax_y) < 1):
        filemax_y+=ser.read(1-len(filemax_y)).hex()
        #################################3
   
        #########################
#            linebuffer= np.frombuffer(rcv_data,">u2")
    
    linebuffer= np.frombuffer(rcv_data,"<u2")
    linebuffer = linebuffer/10 - 273.15
    
        
    ground_state=linebuffer.reshape(32,32);
    ground_state_show = ground_state;
    im2Img = ground_state_show;
  #  print('rcv_data:',ground_state[1,1]);
                

    my,mx = np.where(ground_state_show == ground_state_show.max())
    
    max_x = mx[0]
    max_y = my[0]
  
    max_temp = ground_state_show.max();
    max_temp2 = ground_state_show[16,16];
    framecnt = framecnt -1
    #print(framecnt)
    if(framecnt==0):
        framecnt = 100
        tmp = ser.read(10000).hex()
        while(len(tmp)>0):
            tmp = ser.read(10000).hex()
        
        print('Buffer reset!!')
        
            
        #print('crc2', crc2, 'etx',etx)
                
#    while(1):
#        stx = ser.read(10000).hex()
#        if(len(stx) == 0):
#            break;
        
def Start_clicked(event):
    global start_flag
    start_flag = 1
    print('FilesaveStart!!')
    button['FileSave'].ax.set_facecolor('green')
    button['Stop'].ax.set_facecolor('white')
    #file_init(fy,fmo,fd,fh,fmi,fs)
    #th = ExTimer() 
    #th.setHandler(timerHandler) 
    #th.setDelay(1) 
    #th.start()
    #th.cancel()
def Stop_clicked(event):
    global stop_flag
    stop_flag = 1
    button['FileSave'].ax.set_facecolor('white')
    button['Stop'].ax.set_facecolor('green')
    print('FilesaveStop!!')
    

if __name__ == "__main__":
    main()


#print(a)
#print(b)
#print(c)

#ser.close()