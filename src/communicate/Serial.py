import serial
import threading

#读数代码本体实现
def ReadData(ser):
    global STRGLO
    # 循环接收数据，此为死循环，可用线程实现
    while ser.is_open:
        if ser.in_waiting:
            STRGLO = ser.read(ser.in_waiting).decode("gbk")
            print(STRGLO)

def serialInit(port,
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.5):
    ret=False
    try:
        # 打开串口，并得到串口对象
        ser = serial.Serial(port,
                        baudrate=115200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=0.5)
        #判断是否打开成功
        if(ser.is_open):
           ret=True
           threading.Thread(target=ReadData, args=(ser,)).start()
    except Exception as e:
        print("---异常---：", e)
    return ser,ret

#写数据
def serialSend(ser,text):
    if text is None:
        text = " "
    result = ser.write(text.encode("gbk"))  # 写数据
    return result

#读数据
def serialRead():
    global STRGLO
    str=STRGLO
    STRGLO=""#清空当次读取
    return str

