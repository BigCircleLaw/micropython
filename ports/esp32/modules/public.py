_Addr_Master = 0x00
_Addr_Broadcast = 0x01
# Addr_PC = 0x02
_Addr_Error = 0x03
_Addr_Init = 0x04

_TYPE_INIT = 0x00
_TYPE_RESPONSE = 0x01
_TYPE_INTERRUPT = 0x02
_TYPE_REQUEST = 0x03
_TYPE_REPORT = 0x04

_TYPE_TEST = 0x05
_TYPE_GETTYPE = 0x06
_TYPE_RETYPE = 0x07
_TYPE_INSERT = 0x08
_TYPE_PULL = 0x09

DEVICE_TYPE = {}
DEVICE_TYPE['control'] = 0x00
DEVICE_TYPE['signal'] = 0x01
DEVICE_TYPE['driver'] = 0x02
DEVICE_TYPE['display'] = 0x03
DEVICE_TYPE['observer'] = 0x04
# DEVICE_TYPE['power'] = 0x05
# DEVICE_TYPE['motion'] = 0x06
DEVICE_TYPE['distance'] = 0x07
# DEVICE_TYPE['communication'] = 0x08
# DEVICE_TYPE['servo'] = 0x09
DEVICE_TYPE['voice'] = 0x0A
# DEVICE_TYPE['wifi'] = 0x0B
DEVICE_TYPE['led'] = 0x0C
# DEVICE_TYPE['button'] = 0x0D
# DEVICE_TYPE['servo'] = 0x0E
# DEVICE_TYPE['buzzer'] = 0x0F
# DEVICE_TYPE['volume'] = 0x10
# DEVICE_TYPE['touch'] = 0x11
DEVICE_TYPE['rfCommunication'] = 0x12
DEVICE_TYPE['hall'] = 0x13
DEVICE_TYPE['acceleration'] = 0x14
DEVICE_TYPE['pulse'] = 0x15
DEVICE_TYPE['rfTelecontroller'] = 0x16
# DEVICE_TYPE['spO2'] = 0x17
# DEVICE_TYPE['color'] = 0x18
# DEVICE_TYPE['thermistor'] = 0x19
# DEVICE_TYPE['bluetooth'] = 0x1A
# DEVICE_TYPE['relay'] = 0x1B
# DEVICE_TYPE['switch'] = 0x1C
# DEVICE_TYPE['stepperMotor'] = 0x1D
# DEVICE_TYPE['subMaster'] = 0x1E
DEVICE_TYPE['ultrasonic'] = 0x1F
# DEVICE_TYPE['dcSpeedMotor'] = 0x20
# DEVICE_TYPE['lineTracer'] = 0x21
DEVICE_TYPE['makeyMakey'] = 0x22
# DEVICE_TYPE['lineTracerPro'] = 0x23
DEVICE_TYPE['ioExtension'] = 0x24
# DEVICE_TYPE['laser'] = 0x25
# DEVICE_TYPE['soilMoisture'] = 0x26
DEVICE_TYPE['pressure'] = 0x27
# DEVICE_TYPE['cameraSwitching'] = 0x28
DEVICE_TYPE['lightBelt'] = 0x29
# DEVICE_TYPE['ps2Receiver'] = 0x2A
# DEVICE_TYPE['carButtom'] = 0x2B
# DEVICE_TYPE['voiceBroadcast'] = 0x2C
DEVICE_TYPE['rtc'] = 0x2D
# DEVICE_TYPE['smallStepperMotor'] = 0x2E
DEVICE_TYPE['nfc'] = 0x2F
DEVICE_TYPE['nebulier'] = 0x30
DEVICE_TYPE['buggy'] = 0x31
DEVICE_TYPE['slider'] = 0x32
DEVICE_TYPE['displaymini'] = 0x33
DEVICE_TYPE['climate'] = 0x34
DEVICE_TYPE['light'] = 0x35
DEVICE_TYPE['transmitter'] = 0x36
DEVICE_TYPE['audioPlayer'] = 0x37
DEVICE_TYPE['fingerprint'] = 0x38
DEVICE_TYPE['ledMatrix'] = 0x39

_CMD_LED = 0x00
_CMD_ASK_UID = 0x01
_CMD_GET_VERSION = 0x02

_CMD_LED_RGB = 0x08  # LED2模拟输出颜色
_CMD_BUZZER_OFF = 0x09
_CMD_BUZZER_FRE = 0x0A  # 设置无源蜂鸣器频率
_CMD_VIBRATIONMOTOR_SET = 0x0B  # 设置振动马达震动强度
_CMD_BUZZER_SET = 0x0C  # 设置无源蜂鸣器频率，占空比
_CMD_SignalRGB_Fade = 0x0D  # 设置RGB渐变
_CMD_PlayANode = 0x0E  # 播放一个声音

_CMD_Motor_DC_SET = 0x07  # ����ֱ�������ķ������ٶ�
_CMD_Motor_DC_STOP = 0x08  # ֱֹͣ����������
_CMD_Motor_DC_BRAKE = 0x09  # ֱ������ɲ��

_CMD_IR_CAPTURE_FIAT = 0x08  # IR 获取命令
_CMD_IR_SEND_FIAT = 0x09  # IR 发送命令
_CMD_IR_SEND_DATA = 0x0A  # IR 发送数据
_CMD_IR_ABANDON_FIAT = 0x0B  # IR 获取命令

_CMD_GetHumidity = 0x08  # OLED 读取湿度
_CMD_GetTemp = 0x09  # OLED 读取温度

_CMD_POWER_LIGHTSON = 0x08  # 电源指示灯开
_CMD_POWER_LIGHTSOFF = 0x09  # 电源指示灯关
_CMD_POWER_READ = 0x0E  # 读取电量
_CMD_POWER_OFF = 0x0F  # 关闭电源

_CMD_MPU6050_GET = 0x08  # 读取所有轴所有数据
_CMD_MPU6050_BRATEGA = 0x09  # 校准加速度，角速度
_CMD_MPU6050_BRATEM = 0x0A  # 校准磁力计

_CMD_VOICERC_SET = 0x08  # 声音设置��������
_CMD_VOICERC_START = 0x25

# _CMD_DC_BRAKE = 0x09    #直流电机刹车

_CMD_Servo_SET = 0x08  # 设置舵机角度

#_CMD_Servo_SET = 0x08

_CMD_Wireless_SetMode = 0x08
_CMD_Wireless_SetID = 0x09
_CMD_Wireless_Send = 0x0A
_CMD_Wireless_SendID = 0x0B
_CMD_Wireless_SetChannel = 0x0C
_CMD_Wireless_Password = 0x0E
_CMD_Wireless_Send2 = 0x0F
_CMD_Wirless_Mate = 0x10

_CMD_BluetoothSetName = 0x08

_CMD_StepperMotor_Run = 0x08
_CMD_StepperMotor_Seg = 0x09
_CMD_StepperMotor_Ref = 0x0A

_CMD_RELAY_ON = 0x08
_CMD_RELAY_OFF = 0x09

RGB_R = 1
RGB_G = 2
RGB_B = 3
RGB_LB = 4
RGB_Y = 5
RGB_P = 6
RGB_W = 7
RGB_OFF = 8

# Master = 0x01
# Slave = 0x02
