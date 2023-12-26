from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QMovie 
import os
import time
import sys
import yaml
import mediapipe as mp
import cv2
import numpy as np
import threading    
from multiprocessing import Process
from multiprocessing import Pool
from serial_coms import CHSerial
from num2words import num2words

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 1920)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 1920))
        MainWindow.setMaximumSize(QtCore.QSize(1080, 1920))
        self.config = config
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1080, 1920))
        self.label.setMinimumSize(QtCore.QSize(1080, 1920))
        self.label.setMaximumSize(QtCore.QSize(1080, 1920))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths['start_screen'])))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 1370, 581, 161))
        self.pushButton.setText("")
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(490, 1530, 101, 111))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths['zero'])))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_2.hide()
        self.movie = QMovie(os.path.join(os.getcwd(), self.config.paths['loading_gif'])) 
        self.label_2.setMovie(self.movie)
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(410, 780, 340, 400))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths['zero'])))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_3.hide()
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(310, 780, 340, 400))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths['zero'])))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_4.hide()
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(490, 780, 340, 400))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths['zero'])))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_5.hide()
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.dualN = False
        self.dispenser_state = False
        self.tout = False
        self.prepare_screen = True
        self.connect_dispenser()
        self.testCamera(self.config.camera_id)
        self.remainingTime = self.config.animation_timeout
        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.updateTimer)
        self.pushButton.clicked.connect(self.startClicked)
    
    def startAnimOps(self):
        self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths['prepare_screen'])))
        self.label_2.show()
        self.remainingTime = self.config.animation_timeout * 1000
        print("Total animation time:", self.remainingTime)
        self.timer.start(100)
        self.movie.start()
    
    def startClicked(self):
        print('initiating start ops')
        if self.config.dispenser:
            try: 
                if self.dispenser.poll_data(True) == 0:
                    self.startAnimOps()
                    t2 = threading.Thread(target=self.squat_ops)
                    t2.start()
                else:
                    print('No coins')
                    self.warning('Out of Coins!', 'd')
            except:
                print("Dispenser is not connected to your machine")
                self.warning('Dispenser is not connected to your machine!', 'd')
                # self.go_back()
        else:
            print("testing without dispenser")
            if self.config.camera:
                if self.testCamera(self.config.camera_id):
                    self.startAnimOps()
                    t2 = threading.Thread(target=self.squat_ops)
                    t2.start()
            else:
                print("testing without camera")
                self.startAnimOps()
                t2 = threading.Thread(target=self.squat_ops)
                t2.start()
                
    def updateTimer(self):
        self.remainingTime -= 100
        if (self.remainingTime < (self.config.animation_timeout*1000 // 2) and self.remainingTime > 0):
            if self.prepare_screen:
                print(f"{self.remainingTime / 1000:.2f} seconds passed and going to get_ready_screen")
                self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths['get_ready_screen'])))
                print('get_ready_screen')
                self.prepare_screen = False
        if self.remainingTime < 0:
            self.movie.stop()
            self.timer.stop()
            print("Animation stopped after {} seconds".format(self.config.animation_timeout))
            self.prepare_screen = True
            self.label_2.hide()
            self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths['blank_screen'])))
            self.label_3.show()
            return True
    
    def squat_ops(self):
        time.sleep(self.config.animation_timeout)
        print("starting squating now")
        if self.detect_squat(self.config.squat_number):
            self.label_3.hide()
            self.label_4.hide()
            self.label_5.hide()
            self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(),self.config.paths['finish_screen'])))
            time.sleep(2)
            self.go_back()
        else:
            print('squat timeout')
            self.tout =  True
            self.go_back()
    
    def load_config(self, file_path):
        with open(file_path) as config_file:
            config_data = yaml.safe_load(config_file)
            return ConfigData(**config_data)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def connect_dispenser(self):
        if self.config.dispenser:
            try:
                os.system("sudo chmod a+rw /dev/ttyUSB0")
                self.dispenser = CHSerial(port='/dev/ttyUSB0')
                self.dispenser_state = self.dispenser.poll_data(True) 
                if self.dispenser_state == 0:
                    print('dispenser connected successfully! and working properly')
                elif self.dispenser_state == 1:
                    print('dispenser connected successfully! but out of coins')
                    self.warning('OUT OF COINS!', 'd')
                elif self.dispenser_state == 2:
                    print("AN ERROR HAS OCCURED ON THE DISPENSER SIDE!")
                    self.warning('dispenser not working properly', 'd')                
            except:
                self.warning('Dispenser not connected to your machine', 'd')
                print('dispenser not connected with the machine')
                self.dispenser_state = False

    def testCamera(self, source):
        if self.config.camera:
            print('Trying to connect to camera_id: ', source)
            cap = cv2.VideoCapture(source) 
            if cap is None or not cap.isOpened():
                print('Warning: unable to open video source from webcam: ', source)
                self.warning('Camera not working!', 'c')
                return False
            else:
                print('Webcam {} works!'.format(source))
                cap.release()
                return True
    
    def go_back(self):
        print("go back pressed: returning to home screen")
        self.stopOps = True
        self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(),self.config.paths['start_screen'])))
        self.state = 'start'
        self.label_3.hide()
        if self.dualN:
            print("here")
            self.label_4.hide()
            self.label_5.hide()  
        self.dualN = False          

    def detect_squat(self, squat_n=5):
        self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(),self.config.paths['blank_screen'])))
        self.label_3.show()
        self.label_3.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths['zero'])))
        success = False
        def findAngle(a, b, c, minVis=0.8):
            
            if a.visibility > minVis and b.visibility > minVis and c.visibility > minVis:
                bc = np.array([c.x - b.x, c.y - b.y, c.z - b.z])
                ba = np.array([a.x - b.x, a.y - b.y, a.z - b.z])

                angle = np.arccos((np.dot(ba, bc)) / (np.linalg.norm(ba)
                                                    * np.linalg.norm(bc))) * (180 / np.pi)

                if angle > 180:
                    return 360 - angle
                else:
                    return angle
            else:
                return -1

        def legState(angle):
            if angle < 0:
                print('angle not being picked up')
                return 0  # Joint is not being picked up
            elif angle <= self.config.min_angle: #80
                return 1  # Squat range
            elif angle < self.config.max_angle: #140
                return 2  # Transition range
            else:
                return 3  # Upright range
            
        # Init mediapipe drawing and pose
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        cap = None
        if self.config.camera:
            cap = cv2.VideoCapture(self.config.camera_id) # webcam
        else:
            cap = cv2.VideoCapture("images/test_vid.mp4") # video file

        prev_time =  time.time()
        s_time = prev_time
        prev_s = prev_time
        
        while cap.read()[1] is None:
            new_time  = time.time()
            if ((new_time-s_time)>2):
                print('\n2s passed and no camera feedback\n')
                self.warning('Camera Not Working!', 'c')
                break
            print("Waiting for Video")

        # Main Detection Loop
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

            # Initialize Reps and Body State
            repCount = 0
            lastState = 9

            while cap.isOpened():

                if repCount >= squat_n:
                    if repCount <= 9:
                        self.label_3.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths[self.nwords(repCount)])))
                    else:
                        self.label_4.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths[self.nwords(str(repCount)[0])])))
                        self.label_5.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths[self.nwords(str(repCount)[1])])))
                    time.sleep(2)
                    print('Congratulations!! {} squats done'.format(repCount))
                    success = True
                    break
                
                ret, frame = cap.read()

                new_time  = time.time()
                if ((new_time-s_time)>15):
                    if (new_time - prev_s) > self.config.squat_timeout:
                        print('\n{}s passed and no new squat\n'.format(self.config.squat_timeout))
                        break

                if frame is None:
                    print('Error: Image not found or could not be loaded.')
                    # cv2.destroyAllWindows()
                    sys.exit()
                else:
                    frame = cv2.resize(frame, (1280, 720), fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

                if ret == True:
                    try:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame.flags.writeable = False

                        lm = pose.process(frame).pose_landmarks
                        lm_arr = lm.landmark
                    except:
                        print("Please Step Into Frame")

                        continue

                    # Allow write, convert back to BGR
                    frame.flags.writeable = True
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                    rAngle = findAngle(lm_arr[24], lm_arr[26], lm_arr[28])
                    lAngle = findAngle(lm_arr[23], lm_arr[25], lm_arr[27])
                    
                    # Calculate state
                    rState = legState(rAngle)
                    lState = legState(lAngle)
                    state = rState * lState

                    if state == 1 or state == 9:
                        if state == 9:
                            self.mode = 'prepared'
                        if lastState != state:
                            lastState = state
                            if lastState == 1:
                                print("\nGOOD! Another Squat\n")
                                repCount = repCount + 1
                                print("Squats done: " + (str)(repCount))
                                prev_s = time.time()
                                # self.label_2.hide()
                                # self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(),self.config.blank_screen)))
                                self.label_3.show()
                                # nwords = num2words(repCount)
                                if repCount <=9:
                                    self.label_3.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths[self.nwords(str(repCount))])))
                                else:
                                    self.dualN = True
                                    self.label_3.hide()
                                    print('here', str(repCount))
                                    self.label_4.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths[self.nwords(str(repCount)[0])])))
                                    self.label_4.show()
                                    self.label_5.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), self.config.paths[self.nwords(str(repCount)[1])])))
                                    self.label_5.show()
        return success
    
    
    def nwords(self, n):
        return num2words(n)
    
    def warning(self, s, dev):
        button = QMessageBox.warning(
            self.centralwidget,
            "Error!",
            s,
            buttons=(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Retry),
            defaultButton=QMessageBox.StandardButton.Ok
        )
        if button == QMessageBox.StandardButton.Ok:
            self.go_back()
        else:
            if dev == 'd':
                print("trying dispenser again!")
                self.connect_dispenser()
            if dev == 'c':
                self.testCamera(self.config.camera_id)


class ConfigData:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
def load_config(file_path):
    with open(file_path) as config_file:
        config_data = yaml.safe_load(config_file)
        return ConfigData(**config_data)

def main():

    config = load_config('config.yaml')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    if config.fullscreen:
        MainWindow.showFullScreen()
    else:    
        MainWindow.showNormal()
    sys.exit(app.exec())   
        
if __name__ == "__main__":
    config = load_config('config.yaml')
    main()
