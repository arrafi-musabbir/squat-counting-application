from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie 
import os
import config
import time
from test import detect_squat
import sys
import mediapipe as mp
import cv2
import numpy as np
import threading    
from num2words import num2words
# from PyQt5.QtGui import QMovie

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 1920)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 1920))
        MainWindow.setMaximumSize(QtCore.QSize(1080, 1920))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1080, 1920))
        self.label.setMinimumSize(QtCore.QSize(1080, 1920))
        self.label.setMaximumSize(QtCore.QSize(1080, 1920))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(),config.start_screen)))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 1370, 581, 161))
        self.pushButton.setText("")
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 0, 81, 81))
        self.pushButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.go_back)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(72, 72))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.hide()
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(490, 1530, 101, 111))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.zero)))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_2.hide()
        # Loading the GIF 
        self.movie = QMovie(os.path.join(os.getcwd(), config.loading_gif)) 
        self.label_2.setMovie(self.movie)
        self.startAnimation() 
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(410, 780, 340, 400))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.zero)))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_3.hide()
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(310, 780, 340, 400))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.zero)))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_4.hide()
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(490, 780, 340, 400))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.zero)))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_5.hide()
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton.clicked.connect(self.start_squat)
        self.pushButton_2.clicked.connect(self.go_back)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.stopOps = False
        self.dualN = False

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def go_back(self):
        print("go back pressed: returning to home screen")
        if self.state == 'prepare':
            self.stopOps = True
            self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(),config.start_screen)))
            self.state = 'start'
            self.pushButton_2.hide()
            self.label_2.hide()
            self.label_3.hide()
            if self.dualN:
                print("here")
                self.label_4.hide()
                self.label_5.hide()  
            self.dualN = False          
            # self.stopOps = False


    def detect_squat(self, squat_n=5):
        success = False
        def findAngle(a, b, c, minVis=0.8):
            # Finds the angle at b with endpoints a and c
            # Returns -1 if below minimum visibility threshold
            # Takes lm_arr elements

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
            # print('angle: ', angle)
            if angle < 0:
                print('angle not being picked up')
                return 0  # Joint is not being picked up
            elif angle <= 95: #105
                print('squat range')
                return 1  # Squat range
            elif angle < 140: #150
                # print('transition range')
                return 2  # Transition range
            else:
                print('upright range')
                return 3  # Upright range
            
        # Init mediapipe drawing and pose
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        cap = None
        cap = cv2.VideoCapture("/home/arrafi/squat_front/Squat_test.mp4") # vide file
        # cap = cv2.VideoCapture(0)

        while cap.read()[1] is None:
            print("Waiting for Video")

        # Main Detection Loop
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

            # Initialize Reps and Body State
            repCount = 0
            lastState = 9

            while cap.isOpened():
                if self.stopOps:
                    print('initiating stops ops')
                    self.stopOps = False
                    break
                if repCount >= squat_n:
                    if repCount <= 9:
                        self.label_3.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.nwords(repCount))))
                    else:
                        self.label_4.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.nwords(str(repCount)[0]))))
                        self.label_5.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.nwords(str(repCount)[1]))))
                    time.sleep(2)
                    print('Congratulations!! {} squats done'.format(repCount))
                    success = True
                    cv2.destroyAllWindows()
                    break
                ret, frame = cap.read()
                if frame is None:
                    print('Error: Image not found or could not be loaded.')
                    cv2.destroyAllWindows()
                    sys.exit()
                else:
                    frame = cv2.resize(frame, (1080, 800), fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
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
                                self.label_2.hide()
                                self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(),config.blank_screen)))
                                self.label_3.show()
                                # nwords = num2words(repCount)
                                if repCount <=9:
                                    self.label_3.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.nwords(repCount))))
                                else:
                                    self.dualN = True
                                    self.label_3.hide()
                                    print('here', str(repCount))
                                    self.label_4.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.nwords(str(repCount)[0]))))
                                    self.label_4.show()
                                    self.label_5.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.nwords(str(repCount)[1]))))
                                    self.label_5.show()
                                    
                    print("Squats done: " + (str)(repCount))

                    # if cv2.waitKey(1) & 0xFF == 27:
                    #     break
        return success
    # Start Animation 
    def startAnimation(self): 
        self.movie.start() 
  
    # Stop Animation(According to need) 
    def stopAnimation(self):
        self.label_2.hide() 
        self.movie.stop() 
    
    def start_squat(self):
        print('initiating start ops')
        self.stopOps = False
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.show()
        self.state = 'prepare'
        self.t1 = threading.Thread(target=self.prepare_screen)
        self.t2 = threading.Thread(target=self.getReady_screen)
        self.t1.start()
        self.t2.start()
        time.sleep(1)
        
    def prepare_screen(self):
        self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(),config.prepare_screen)))
        print('prepare_screen')

    def getReady_screen(self):
        self.label_2.show()
        time.sleep(6)
        self.label_2.hide()
        if self.stopOps == False:
            self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(),config.get_ready_screen)))
            self.label_2.show()
            print('prepare_screen done >>> now get_ready_screen')
            if self.detect_squat(config.squat_number):
                self.label_3.hide()
                self.label_4.hide()
                self.label_5.hide()
                self.label.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(),config.finish_screen)))
        else:
            self.go_back()
    
    def squat_ops(self):
        time.sleep(12)
        self.detect_squat(2)    
    
    def screen_transition(self):
        time.sleep(1)
        self.label_2.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.one)))
        time.sleep(1)
        self.label_2.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.two)))
        time.sleep(1)
        self.label_2.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.three)))
        time.sleep(1)
        self.label_2.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.four)))
        time.sleep(1)
        self.label_2.setPixmap(QtGui.QPixmap(os.path.join(os.getcwd(), config.five)))
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
