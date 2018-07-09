import socket
from enum import IntEnum
from MotorModule.Motor import Motor
import traceback
import threading
import time
from SteeringModule.Steering import Steering

def getLocalIp():
    '''Get the local ip'''
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip

def motorAction(motor,command):
    '''Set the action of motor according to the command'''
    if command=='DirForward':
        motor.ahead()
    elif command=='DirBack':
        motor.rear()
    elif command=='DirLeft':
        motor.left()
    elif command=='DirRight':
        motor.right()
    elif command=='DirStop':
        motor.stop()

def setCameraAction(command):
    if command=='CamUp' or command=='CamDown' or command=='CamLeft' or command=='CamRight':
        return command

def cameraActionThread():
    '''This is a child thread to control the action of camera'''
    #Init the steering module
    steer=Steering(14,0,180,15,90,180,36,160)
    steer.setup()
    while stopCameraThread is False:
        time.sleep(0.001) #It look like that a delay must be set, otherwise the progam runs 'blocking'
        if cameraAction=='CamUp':
            steer.Up()
            continue
        elif cameraAction=='CamDown':
            steer.Down()
            continue
        elif cameraAction=='CamLeft':
            steer.Left()
            continue
        elif cameraAction=='CamRight':
            steer.Right()
            continue
        else:
            pass
    steer.cleanup()

def main():
    '''The main thread, control the motor'''
    host=getLocalIp()
    print('localhost ip :'+host)
    port=5050

    #Init the tcp socket
    tcpServer=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcpServer.bind((host,port))
    tcpServer.setblocking(0) #Set unblock mode
    tcpServer.listen(5)

    #Init motor module
    motor=Motor(5,21,22,23,24,13)
    motor.setup()

    #Set a state variable for steering module
    global cameraAction
    cameraAction='CamStop'
    global stopCameraThread
    stopCameraThread=False

    while True:
        try:
            (client,addr)=tcpServer.accept()
            print('accept the client!')
            stopCameraThread=False
            camera_action_thread=threading.Thread(target=cameraActionThread,args=())
            camera_action_thread.start()
            while True:
                try:
                    data=client.recv(1024)
                    data=bytes.decode(data)
                    if(len(data)==0):
                        print('client is closed')
                        break
                    motorAction(motor,data)
                    cameraAction=setCameraAction(data)
                except socket.error:
                    pass
                except Exception:
                    raise Exception
            stopCameraThread=True #Notice the camera action thread to stop
            time.sleep(1)
        except socket.error:
            pass
        except Exception,e1:
            traceback.print_exc()
            stopCameraThread=True
            motor.clear()
            tcpServer.close()
    stopCameraThread=True
    motor.clear()
    tcpServer.close()

main()
