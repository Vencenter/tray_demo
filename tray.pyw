# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets as  QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import *
import os,datetime
import sys
import sip
import _thread
import subprocess
from multiprocessing import Process
from shutdown import LoginDialog
import numpy as np
#from pic import src
import pythoncom
from win32com.shell import shell
import locale
import win32timezone
import random
import win32api
root = os.path.dirname(__file__)


print (root)
os.chdir(root)
speed = 360

class circle_label(QtGui.QLabel):
    def __init__(self,parent=None):
        QtGui.QLabel.__init__(self, parent)
        self._parent =  parent

        self.time_num=0
   
        
        self.setWindowTitle("Tray!")
        self.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground);
        self.setWindowOpacity(1)
        self._time=QtCore.QTimer()
        self._time.start(10)  
        self.pic=QPixmap('pic/circle.png')
        self.setPixmap(self.pic)
        self.setMask(self.pic.mask())
        self.setAlignment(QtCore.Qt.AlignCenter)
        self._time.timeout.connect(self.change_position)

    def mousePressEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.dragPosition=event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
        if event.button()==QtCore.Qt.RightButton:
            pass
    def mouseMoveEvent(self,event):
        if event.buttons()& QtCore.Qt.LeftButton:
            self.move(event.globalPos()-self.dragPosition)
            event.accept()
    def change_position(self):
        r = self._parent.height()/1.2
        a =  (self._parent.pos().x()+ self._parent.width()/2)
        b =  (self._parent.pos().y() +self._parent.height()/2.5)

        pos_data= ((speed-self.time_num)/speed)*2*np.pi
        self.time_num+=1

        if self.time_num>=speed:
            self.time_num=0
        
        x = a + r * np.cos(pos_data)
        y = b + r * np.sin(pos_data)
        self.move(x,y)

class custdom_label(QtGui.QLabel):
    def __init__(self,text="",parent=None):
        QtGui.QLabel.__init__(self, parent)

        self.setWindowTitle("Tray!")
        self.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground);
        self.setWindowOpacity(1)
      
    
        self.setAlignment(QtCore.Qt.AlignCenter)
        font = QFont()
        color = "color:white"
        self.setStyleSheet(color)
        #font.setFamily("Arial") 
        font.setPointSize(28)   
        self.setFont(font)
        self.setText(text)
    
        self.resize(1920,300)
        self.show()
    def mousePressEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.dragPosition=event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
        if event.button()==QtCore.Qt.RightButton:
            pass
    def mouseMoveEvent(self,event):
        if event.buttons()& QtCore.Qt.LeftButton:
            self.move(event.globalPos()-self.dragPosition)
            event.accept()

  
class Tray_(QtGui.QLabel):
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)
        self._pic_vaule = 1
        self.zoomscale=1
        self.contorl=1
        self.contorl_=1
        self._change_pic=1
        self.change_switch = 0
        self.move_value=0
        
        self.setWindowTitle("Tray!")
        self.setAcceptDrops(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground);
        self.setWindowOpacity(1)
        self._time=QtCore.QTimer()
        
        self._image=QtGui.QLabel()
        self._pic =QPixmap('pic/pic1.png')
        self._image.setPixmap(self._pic)
        self._image.setMask(self._pic.mask())
        #self._image.setMask(self._pic.mask())
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self._image)
        self.setLayout(self.layout)  
        

        self._time.timeout.connect(self.shut_down)
        self._image.setScaledContents(True)        
        self._image.setAlignment(QtCore.Qt.AlignCenter)
        self.dragPosition=None
        self.createContextMenu() 
        
        self._time.start(600000)

        
        self.resize(100,100)
        self.show()
         
    def createContextMenu(self):  
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  
        self.customContextMenuRequested.connect(self.showContextMenu)  
        self.contextMenu = QtGui.QMenu(self)  
        self.actionA = self.contextMenu.addAction(u'执行exe')
        self.actionW = self.contextMenu.addAction(u'web')
        self.actionN = self.contextMenu.addAction(u'vpn')
        self.jupyterlab= self.contextMenu.addAction(u'jupyterlab')  
        self.BlackBird= self.contextMenu.addAction(u'BlackBird')  
        self.actionB = self.contextMenu.addAction(u'关机') 
        self.actionS = self.contextMenu.addAction(u'Timer')        
        self.actionC = self.contextMenu.addAction(u'关闭') 
        self.actionH = self.contextMenu.addAction(u'环绕') 
        self.actionRoot = self.contextMenu.addAction(u'root')          
        self.actionA.triggered.connect(self.action_add)  
        self.actionB.triggered.connect(self.action_del)  
        self.actionC.triggered.connect(self.action_close)
        self.actionN.triggered.connect(self.action_vpn)
        self.actionW.triggered.connect(self.action_web)
        self.actionH.triggered.connect(self.circle_round)
        self.jupyterlab.triggered.connect(self.jupyter)
        self.BlackBird.triggered.connect(self.blackBird)
        self.actionS.triggered.connect(self.close_timer)
        self.actionRoot.triggered.connect(self.action_root)
    def circle_round(self):
        if self.contorl_==1:
            self.contorl_=0
            self.app = circle_label(self)
            self.app.show()
        else:
            self.contorl_=1
            if self.app!=None:
                self.app.close()
        
    def action_root(self):
        root = "D:\\software\\Python3.7\\Lib\\site-packages"
        #os.startfile(root)
        if not os.path.exists(root):
            return
        else:
            win32api.ShellExecute(None, "open", "explorer.exe",  "/select, "+root+"\\tensorflow",None, 1);
    def close_timer(self):
        
        if self.change_switch == 1:
            self._time.start(60000)
            self.change_switch = 0
        else:
            self._time.start(200)
            self.change_switch = 1
    def shut_down(self):
        current_time = str(datetime.datetime.strftime(datetime.datetime.now(),'%H:%M:%S'))
        compare_time = "23:10:00"
        next_time = "23:11:00"
        
        
        if self.change_switch == 1:
            r = 400  
            a=800
            b=300
           
            current_minutes = int(datetime.datetime.strftime(datetime.datetime.now(),'%M'))
            pos_data= (current_minutes/60)*2*np.pi
            x = a + r * np.cos(pos_data)
            y = b + r * np.sin(pos_data)
            self.move(x,y)
        if current_time>compare_time and current_time < next_time and self.change_switch == 0:   
            cmd="shutdown -s -t 30"
            self.change_switch == 0
            subprocess.Popen(cmd, shell=True)

    def change_pic(self):
        if self._pic_vaule <5:
            self._pic_vaule+=1
            file_pic = 'pic/pic'+str(self._pic_vaule)+'.png'
        else:
            self._pic_vaule  = 1
            file_pic = 'pic/pic'+str(self._pic_vaule)+'.png'
        
           
        #self.layout.removeWidget(self._image)
        
        self._image.deleteLater()
        sip.delete(self.layout)
        
        self._image=QtGui.QLabel()
        self._pic = QPixmap(file_pic)
        self._image.setPixmap(self._pic)
        self._image.setMask(self._pic.mask())
        self._image.setMask(self._pic.mask())
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self._image)
        self.setLayout(self.layout)  
        
    def showContextMenu(self, pos):  
        self.contextMenu.move(self.pos() + pos)  
        self.contextMenu.show()  
    def jupyter(self):
        cmd = u"jupyter notebook"
        subprocess.Popen(cmd, shell=True)
    def blackBird(self):
        root = "D:/local_software/software/BlackBird-Player/playlist/qita"
        if not os.path.exists(root):
            QtGui.QMessageBox.information(self,u"提示", u"您的电脑未配置环境！")
            return
        else:
            os.chdir(root)
        cmd = "python2 update.py"
        subprocess.Popen(cmd, shell=True)
    def action_vpn(self):
        root = "./ChromeGo"
        if not os.path.exists(root):
            QtGui.QMessageBox.information(self,u"提示", u"您的电脑未配置环境！")
            return
        cmd = u"call \"./ChromeGo/7.SSR翻墙.cmd\""
        subprocess.Popen(cmd, shell=True)
    def action_web(self):
        root = "D:/other/website"
        if not os.path.exists(root):
            QtGui.QMessageBox.information(self,u"提示", u"您的电脑未配置环境！")
            return
        else:
            os.chdir(root)
        cmd = u"python2 D:/other/website/run.py"
        subprocess.Popen(cmd, shell=True)
    def action_add(self):
        root="D:/software/player"
        if not os.path.exists(root):
            QtGui.QMessageBox.information(self,u"提示", u"您的电脑未配置环境！")
            return
        else:
            os.chdir(root)
        cmd = "start h-player.exe"
        subprocess.Popen(cmd, shell=True)
    def action_del(self):
        if self.contorl == True:
            dialog = LoginDialog(self)
            dialog.show()
            self.contorl=0
        else:
            cmd="shutdown -a"
            self.contorl=1
            subprocess.Popen(cmd, shell=True)
    def action_close(self):
        if self.contorl_==0:
            self.app.close()
        self.close()
    def play_audio(self,file,txt):
        from playsound import playsound
        text_label = custdom_label(txt,self)
        playsound(file)
        text_label.close()
    def mouseDoubleClickEvent(self, event):
        if event.buttons () == QtCore.Qt.LeftButton: 
            #self.change_pic()
            x = ( event.pos().x()) 
            y = ( event.pos().y()) 
            print (x,y)
            if ((x>=205 and x<=260) and (y>=38 and y<=80)):  
                self.change_pic()
            else:
                root = os.listdir("wav_jp/")
                if root != []:
                    file = "wav_jp/"+random.choice(root)
                else:
                    root = os.listdir("wav_en/")
                    file = "wav_en/"+random.choice(root)
                with open("txt/data.txt","r",encoding = "shift-jis") as f:
                    data = f.readlines()
                
                txt = random.choice(data)
                _thread.start_new_thread( self.play_audio, (file,txt, ) )
         
                
                
         
    def mousePressEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.dragPosition=event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
        if event.button()==QtCore.Qt.RightButton:
            pass
    def mouseMoveEvent(self,event):
        if event.buttons()& QtCore.Qt.LeftButton:
            self.move(event.globalPos()-self.dragPosition)
            event.accept()    
    def func(self,cmd):
        subprocess.Popen(cmd, shell=True)
    def login(self,path):

        if not os.path.exists("D:/software/python2.7"):
            gettime= ("\""+ path +"\"")
            cmd=r"python "+(gettime)
            subprocess.Popen(cmd, shell=True)
        else:
            gettime= ("\""+ path +"\"")
            try:
                cmd=r"python2 "+(gettime)
                subprocess.Popen(cmd, shell=True)
            except Exception as e:
                print (e)
    def dragEnterEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()
    def dragMoveEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()
    def dropEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                filepath = str(urls[0].path())[1:]
                if "." not in filepath:
                    QtGui.QMessageBox.information(self,u"提示", u"不是文件！")
                elif (filepath.split(".")[-1]=="py" or filepath.split(".")[-1]=="pyw"):
                    self.login(filepath )
                elif filepath.split(".")[-1]=="lnk":
                    file_path=self.getShortcutRealPath(filepath)
                    print (file_path)
                    if (file_path.split(".")[-1]=="py" or file_path.split(".")[-1]=="pyw"):
                        self.login(file_path )
                    else:
                        QtGui.QMessageBox.information(self,u"提示", u"文件不符合要求！")
                else:
                    QtGui.QMessageBox.information(self,u"提示", u"文件不符合要求！")            
    def getShortcutRealPath(self,filePath):
        
        pythoncom.CoInitialize()
        shortcut = pythoncom.CoCreateInstance(
                        shell.CLSID_ShellLink, None,
                        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
        shortcut.QueryInterface(pythoncom.IID_IPersistFile).Load(filePath)
        fileRealPath = shortcut.GetPath(shell.SLGP_UNCPRIORITY)[0]
        fileRealPath = fileRealPath
        print (fileRealPath)
        return fileRealPath
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    dialog = Tray_()
    dialog.show()
    sys.exit(app.exec_())
    

