from prometheus_client import CollectorRegistry, push_to_gateway, start_http_server, Summary, Counter, Gauge
import prometheus_client as prom
import random
import time
import os
import serial

registry = CollectorRegistry()

debugas = True

PORT_SELECTED = '/dev/tty.usbmodem2103'
BAUD_SELECTED = 115200
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

# Create a metric to track time spent and requests made.
gVolt = Gauge('aVoltage', 'Tensao do sistema', registry=registry)
gCurrent = Gauge('aCurrent', 'Corrente do sistema', registry=registry)
gPower = Gauge('aPower', 'Potencia do sistema', registry=registry)
gTemperaturePlanetary = Gauge('aTemperaturePlanetary', 'Temperatura da planetaria', registry=registry)
gTemperatureMotor = Gauge('aTemperatureMotor', 'Temperatura do Motor', registry=registry)
gTemperatureInverter = Gauge('aTemperatureInverter', 'Temperatura do Inversor', registry=registry)
gTemperatureAcumulatorPeak = Gauge('aTemperatureAcumulatorPeak', 'Temperatura do Acumulador pico', registry=registry)
gTemperatureAcumulatorAvg = Gauge('aTemperatureAcumulatorAvg', 'Temperatura do Acumulador (media)', registry=registry)
gRPM = Gauge('aRPM', 'RPM do motor', registry=registry)
gWheelSpeed = Gauge('aWheelSpeed', 'Velocidade da roda', registry=registry)
gECUFail = Gauge('aECUFail', 'Falha ECU', registry=registry)
gBMSFail = Gauge('aBMSFail', 'Falha BMS', registry=registry)
gINVFail = Gauge('aIMDFail', 'Falha IMD', registry=registry)
gBSE = Gauge('aBSE', 'BSE', registry=registry)
gAPPS = Gauge('aAPPS', 'APPS', registry=registry)
gDCL = Gauge('aDCL', 'DCL', registry=registry)
gBrakePressure = Gauge('aBrakePressure', 'Pressao dos freios', registry=registry)
gSoC = Gauge('aSoC', 'SoC', registry=registry)
gBackLeftSuspension = Gauge('aBackLeftSuspension', 'Suspensao Traseira Esquerda', registry=registry)
gFrontLeftSuspension = Gauge('aFrontLeftSuspension', 'Suspensao Dianteira Esquerda', registry=registry)
gFrontRightSuspension = Gauge('aFrontRightSuspension', 'Suspensao Dianteira Direita', registry=registry)
gBackRightSuspension = Gauge('aBackRightSuspension', 'Suspensao Traseira Direita', registry=registry)
gSteeringAngle = Gauge('aSteeringAngle', 'Angulo de esterçamento', registry=registry)



def updatePrometheusData(dataS):
    gVolt.set(float(dataS[0])*0.1)
    gCurrent.set(float(dataS[1])*0.1)
    gPower.set(float(dataS[2])*0.1)
    gTemperaturePlanetary.set(float(dataS[3])*0.1)
    gTemperatureMotor.set(float(dataS[4])*0.1)
    gTemperatureInverter.set(float(dataS[5])*0.1)
    gTemperatureAcumulatorPeak.set(float(dataS[6])*0.1)
    gTemperatureAcumulatorAvg.set(float(dataS[7])*0.1)
    gRPM.set(float(dataS[8])*0.1)
    gWheelSpeed.set(float(dataS[9])*0.1)
    gECUFail.set(float(dataS[10])*1)
    gBMSFail.set(float(dataS[11])*1)
    gINVFail.set(float(dataS[12])*1)
    gBSE.set(float(dataS[13])*1)
    gAPPS.set(float(dataS[14])*1)
    gDCL.set(float(dataS[15])*0.1)
    gBrakePressure.set(float(dataS[16])*0.1)
    gSoC.set(float(dataS[17])*0.1)
    gBackLeftSuspension.set(float(dataS[18])*0.1)
    gFrontLeftSuspension.set(float(dataS[19])*0.1)
    gFrontRightSuspension.set(float(dataS[20])*0.1)
    gBackRightSuspension.set(float(dataS[21])*0.1)
    gSteeringAngle.set(float(dataS[22])*0.1)


 
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
        gVolt.set(random.randint(0, 140))
        gCurrent.set(random.randint(0, 500))
        gPower.set(random.randint(0, 50000))
        gTemperaturePlanetary.set(random.randint(0, 150))
        gTemperatureMotor.set(random.randint(0, 150))
        gTemperatureInverter.set(random.randint(0, 150))
        gTemperatureAcumulatorPeak.set(random.randint(0, 150))
        gTemperatureAcumulatorAvg.set(random.randint(0, 150))
        gRPM.set(random.randint(0, 3000))
        gWheelSpeed.set(random.randint(0, 100))
        gECUFail.set(random.randint(0, 1))
        gBMSFail.set(random.randint(0, 1))
        gINVFail.set(random.randint(0, 1))
        gBSE.set(random.randint(0, 100))
        gAPPS.set(random.randint(0, 100))
        gDCL.set(random.randint(0, 200))
        gBrakePressure.set(random.randint(0, 100))
        gSoC.set(random.randint(0, 100))
        gBackLeftSuspension.set(random.randint(0, 100))
        gFrontLeftSuspension.set(random.randint(0, 100))
        gFrontRightSuspension.set(random.randint(0, 100))
        gBackRightSuspension.set(random.randint(0, 100))
        gSteeringAngle.set(random.randint(0, 100))



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
            if len(dataS) != 23:
                continue
            print(data)
            updatePrometheusData(dataS)
            push_to_gateway(f"{prometheus_host}:{prometheus_port}",job="DaVDataServer",registry=registry)
        except:
            print("Erro de Leitura, prosseguindo")