from prometheus_client import CollectorRegistry, push_to_gateway, start_http_server, Summary, Counter, Gauge
import prometheus_client as prom
import random
import time
import os
import serial

#Login: admin
#Senha: ampera2022

registry = CollectorRegistry()

debugas = False

PORT_SELECTED = 'COM5' #'/dev/tty.usbmodem2103'
BAUD_SELECTED = 115200
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()  

# Create a metric to track time spent and requests made.
gLap = Gauge('aLap', 'Volta', registry=registry)
gRpm = Gauge('aRpm', 'RPM', registry=registry)
gMotorCurrent = Gauge('aMotorCurrent', 'Corrente do Motor', registry=registry)
gMotorTemperature = Gauge('aMotorTemperature', 'Temperatura do Motor', registry=registry)
gPower = Gauge('aPower', 'Potência', registry=registry)
gVoltage = Gauge('aVoltage', 'Tensão do Acumulador', registry=registry)
gAccumulatorCurrent = Gauge('aAccumulatorCurrent', 'Corrente do Acumulador', registry=registry)
gAccumulatorTemperature = Gauge('aAccumulatorTemperature', 'Temperatura do Acumulador', registry=registry)
gStateOfCharge = Gauge('aStateOfCharge', 'State Of Charge', registry=registry)
gApps = Gauge('aApps', 'Pedal do Acelerador', registry=registry)
gBse = Gauge('aBse', 'Pedal do Freio', registry=registry)
gRoll = Gauge('aRoll', 'Ângulo de Roll', registry=registry)
gYaw = Gauge('aYaw', 'Ângulo de Yaw', registry=registry)
gPitch = Gauge('aPitch', 'Ãngulo de Pitch', registry=registry)
gLateralForce = Gauge('aLateralForce', 'Força Lateral', registry=registry)
gLongitudinalForce = Gauge('aLongitudinalForce', 'Força Longitudinal', registry=registry)
gSteeringAngle = Gauge('aSteeringAngle', 'Ângulo de Esterçamento', registry=registry)
gRearLeftSuspension = Gauge('aRearLeftSuspension', 'Suspensão Traseira Esquerda', registry=registry)
gRearRightSuspension = Gauge('aRearRightSuspension', 'Suspensão Traseira Direita', registry=registry)
gFrontLeftSuspension = Gauge('aFrontLeftSuspension', 'Suspensão Frontal Esquerda', registry=registry)
gFrontRightSuspension = Gauge('aFrontRightSuspension', 'Suspensão Frontal Direita', registry=registry)
gBrakePressure = Gauge('aBrakePressure', 'Pressão do Freio', registry=registry)
gRearLeftWheelSpeed = Gauge('aRearLeftWheelSpeed', 'Velocidade da Roda Traseira Esquerda', registry=registry)
gRearRightWheelSpeed = Gauge('aRearRightWheelSpeed', 'Velocidade da Roda Traseira Direita', registry=registry)
gFrontLeftWheelSpeed = Gauge('aFrontLeftWheelSpeed', 'Velocidade da Roda Frontal Esquerda', registry=registry)
gFrontRightWheelSpeed = Gauge('aFrontRightWheelSpeed', 'Velocidade da Roda Frontal Direita', registry=registry)
gInverterFail = Gauge('aInverterFail', 'Falha do Inversor', registry=registry)
gBmsFail = Gauge('aBmsFail', 'Falha do BMS', registry=registry)
gImdFail = Gauge('aImdFail', 'Falha do IMD', registry=registry)
gBspdFail = Gauge('aBspdFail', 'Falha da BSPD', registry=registry)
gEcuFail = Gauge('aEcuFail', 'Falha da ECU', registry=registry)
gLatitude = Gauge('aLatitude', 'Latitude', registry=registry)
gLongitude = Gauge('aLongitude', 'Longitude', registry=registry)


#Ex: yaw, roll, angle = 123.456(+-)
#Ex: latitude, longitude = 56.12345678(+-) (Multiplicar por 10^9 pra caso a lat long for > 100)

def updatePrometheusData(dataS):
    gLap.set(float(dataS[0])*1)
    gRpm.set(float(dataS[1])*1)
    gMotorCurrent.set(float(dataS[2])*1)
    gMotorTemperature.set(float(dataS[3])*1)
    gPower.set(float(dataS[4])*1)
    gVoltage.set(float(dataS[5])*1)
    gAccumulatorCurrent.set(float(dataS[6])*1)
    gAccumulatorTemperature.set(float(dataS[7])*1)
    gStateOfCharge.set(float(dataS[8])*1)
    gApps.set(float(dataS[9])*1)
    gBse.set(float(dataS[10])*1)
    gRoll.set(float(dataS[11])*0.001)
    gYaw.set(float(dataS[12])*0.001)
    gPitch.set(float(dataS[13])*0.001)
    gLateralForce.set(float(dataS[14])*1)
    gLongitudinalForce.set(float(dataS[15])*1)
    gSteeringAngle.set(float(dataS[16])*1)
    gRearLeftSuspension.set(float(dataS[17])*1)
    gRearRightSuspension.set(float(dataS[18])*1)
    gFrontLeftSuspension.set(float(dataS[19])*1)
    gFrontRightSuspension.set(float(dataS[20])*1)
    gBrakePressure.set(float(dataS[21])*1)
    gRearLeftWheelSpeed.set(float(dataS[22])*0.26)
    gRearRightWheelSpeed.set(float(dataS[23])*0.26)
    gFrontLeftWheelSpeed.set(float(dataS[24])*0.26)
    gFrontRightWheelSpeed.set(float(dataS[25])*0.26)
    gInverterFail.set(float(dataS[26])*1)
    gBmsFail.set(float(dataS[27])*1)
    gImdFail.set(float(dataS[28])*1)
    gBspdFail.set(float(dataS[29])*1)
    gEcuFail.set(float(dataS[30])*1)
    gLatitude.set(float(dataS[31])*0.000000001)
    gLongitude.set(float(dataS[32])*0.000000001)


 
if __name__ == '__main__':
    # Start up the server to expose the metrics.
    # Generate some requests.
    print("AMP Telemetry Server - DaV2") 
    print("Starting server")
    time.sleep(1)
    prometheus_host = "http://localhost"
    prometheus_port = 9091
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

    while debugas:
        
        gLap.set(random.randint(0, 5))
        gRpm.set(random.randint(0, 5000))
        gMotorCurrent.set(random.randint(0, 200))
        gMotorTemperature.set(random.randint(0, 80))
        gPower.set(random.randint(0, 28000))
        gVoltage.set(random.randint(0, 164))
        gAccumulatorCurrent.set(random.randint(0, 200))
        gAccumulatorTemperature.set(random.randint(0, 50))
        gStateOfCharge.set(random.randint(0, 100))
        gApps.set(random.randint(0, 100))
        gBse.set(random.randint(0, 100))
        gRoll.set(random.randint(-180, 180))
        gYaw.set(random.randint(-180, 180))
        gPitch.set(random.randint(-180, 180))
        gLateralForce.set(random.randint(-2, 2))
        gLongitudinalForce.set(random.randint(-2, 2))
        gSteeringAngle.set(random.randint(-40, 40))
        gRearLeftSuspension.set(random.randint(0, 30))
        gRearRightSuspension.set(random.randint(0, 30))
        gFrontLeftSuspension.set(random.randint(0, 30))
        gFrontRightSuspension.set(random.randint(0, 30))
        gBrakePressure.set(random.randint(0, 100))
        gRearLeftWheelSpeed.set(random.randint(0, 100))
        gRearRightWheelSpeed.set(random.randint(0, 100))
        gFrontLeftWheelSpeed.set(random.randint(0, 100))
        gFrontRightWheelSpeed.set(random.randint(0, 100))
        gInverterFail.set(random.randint(0, 1))
        gBmsFail.set(random.randint(0, 1))
        gImdFail.set(random.randint(0, 1))
        gBspdFail.set(random.randint(0, 1))
        gEcuFail.set(random.randint(0, 1))
        gLatitude.set(random.randint(0, 100))
        gLongitude.set(random.randint(0, 100))


        push_to_gateway(f"{prometheus_host}:{prometheus_port}",job="DaVDataServer",registry=registry)

    while True:
        try:
            ser = serial.Serial(PORT_SELECTED, BAUD_SELECTED)
            ser.flushInput()
            time.sleep(0.5)
            print("Sistema iniciado, conectando a Telemetria")
            time.sleep(0.5)
            break
        except:
            print("Não foi possível conectar a serial, verifique a Porta e o Baud")
            time.sleep(2)
    while True:
        try:
            data = ser.readline().decode('ascii')
            dataS = data.split(",")
            if len(dataS) != 33:
                continue
            print(data)
            updatePrometheusData(dataS)
            push_to_gateway(f"{prometheus_host}:{prometheus_port}",job="DaVDataServer",registry=registry)
        except:
            print("Erro de Leitura, prosseguindo")