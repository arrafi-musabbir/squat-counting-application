# squat-detection-application

This is a desktop application that utilizes `mediapipe` library for pose estimation to detect squats. This application is being deployed in Romania to encourage people to do squats, at the end of a certain successful number of squats (e.g. 5), the vending machine will dispense a coin to the customers. 

The application is being developed by `pyqt5` library and deployed in an [Intel NUC mini pc](https://www.intel.com/content/www/us/en/products/details/nuc/mini-pcs/products.htm) which maintains serial communication with a coin-dispenser machine. The serial communication protocol can be found here: [communication-protocol](https://github.com/arrafi-musabbir/squat-detection-application/blob/main/hopper_communication.txt)

### Try the app yourself: 
* Clone the repository
  ```
  git clone https://github.com/arrafi-musabbir/squat-counting-application.git
  ```
* Go the clone directory and install the requirements
  ```
  pip install -r requirements.txt
  ```
* Run the app
  ```
  python app.py
  ```
##### or download the `app.exe` from `release-v1`
#### 

| GUI workflow             | Squat Detection in Backend              |
| ---------------------- | --------- |
| ![gui-workflow](https://github.com/arrafi-musabbir/squat-detection-application/blob/main/gui-workflow.gif) | ![squat-detection-backend](https://github.com/arrafi-musabbir/squat-detection-application/blob/main/squat_results.gif) |

### minimum system requirements

* Ubuntu LTS 22.04
* Intel-core-i3-5100u-processor-3m-cache-2.40-ghz
* Included Memory 1x4GB DDR4
* Included Storage 128GB HDD
* Python 3.10.12
