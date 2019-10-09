# Delta Robot GUI
> Software for control delta robot by graphical user interface. 
> It's working on Ubuntu and Raspberry Pi 
> Embedded control Smart Servo Dynamixel AX-12A

## Table of contents
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Run](#run)
* [Status](#status)

## Screenshots
![Example screenshot](.konstrukcja.png)

## Technologies
* Python 	3.5.2
* PyQt5
* numpy  	1.17.2
* matplotlib  	1.5.1

## Setup
Install follow library:

* $ sudo apt-get install python3-pyqt5
* $ sudo apt-get install pyqt5-dev-tools
* $ sudo apt-get install qttools5-dev-tools
* $ sudo apt-get install python3-numpy
* $ sudo apt-get install python-matplotlib
* $ sudo apt-get install python3-opengl
	
and install Dynamixel library in home folder:

* $ git clone https://github.com/ROBOTIS-GIT/DynamixelSDK
* $ cd ~/DynamixelSDK/python
* $ sudo python3 setup.py install

## Run
* $ python3 delta.py
* Add data construct

## Status
Project is: _in progress_
