#!../../bin/linux-x86_64/pydevioc

< envPaths

# PYTHONPATH points to folders where Python modules are.
epicsEnvSet("PYTHONPATH","$(TOP)/python")
epicsEnvSet("PYTHONPATH","/home/pla/modules/pydevice/python")##Motor.py

cd ${TOP}

## Register all support components
dbLoadDatabase "${TOP}/dbd/pydevioc.dbd"
pydevioc_registerRecordDeviceDriver pdbbase

##モーター制御の初期化
pydev("from Motor2 import PhidgetServoController")
##pydev("motor_controller = PhidgetServoController()")

## ---------ここから
dbLoadRecords("${TOP}/testApp/Db/pydevtest.db","P=GID:,R=,L=0,A=0")
epicsEnvSet("STREAM_PROTOCOL_PATH","${TOP}")
drvAsynSerialPortConfigure("L0","/dev/ttyUSB0",0,1,0)
asynSetOption("L0", -1, "baud","9600")
asynSetOption("L0", -1, "bits","8")
asynSetOption("L0", -1, "parity", "none") 
asynSetOption("L0", -1, "stop","1")
##asynSetOption("L0", -1, "handshake", "xonxoff")
asynSetOption("L0", -1, "clocal","Y")
## ------------- ここまで追加

## Load record instances
dbLoadRecords("${TOP}/testApp/Db/pydevtest.db")
dbLoadRecords("${TOP}/testApp/Db/pycalcrectest.db")

cd ${TOP}/iocBoot/${IOC}

pydev("import time")
pydev("import pydevtest")
pydev("google = pydevtest.HttpClient('www.google.com', 80)")

iocInit
