from prometheus_client import start_http_server, Summary, Counter, Gauge
import prometheus_client as prom
import random
import time
import os
import serial

PORT_SELECTED = '/dev/tty.usbmodem103'
BAUD_SELECTED = 115200
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

# Create a metric to track time spent and requests made.
gVolt = Gauge('aVoltage', 'Tensao do sistema')
gCurrent = Gauge('aCurrent', 'Corrente do sistema')
gPower = Gauge('aPower', 'Potencia do sistema')
gTemperaturePlanetary = Gauge('aTemperaturePlanetary', 'Temperatura da planetaria')
gTemperatureMotor = Gauge('aTemperatureMotor', 'Temperatura do Motor')
gTemperatureInverter = Gauge('aTemperatureInverter', 'Temperatura do Inversor')
gTemperatureAcumulatorPeak = Gauge('aTemperatureAcumulatorPeak', 'Temperatura do Acumulador pico')
gTemperatureAcumulatorAvg = Gauge('aTemperatureAcumulatorAvg', 'Temperatura do Acumulador (media)')
gRPM = Gauge('aRPM', 'RPM do motor')
gWheelSpeed = Gauge('aWheelSpeed', 'Velocidade da roda')
gECUFail = Gauge('aECUFail', 'Falha ECU')
gBMSFail = Gauge('aBMSFail', 'Falha BMS')
gIMDFail = Gauge('aIMDFail', 'Falha IMD')
gBSPDFail = Gauge('aBSPDFail', 'Falha BSPD')
gDCL = Gauge('aDCL', 'DCL')
gBSE = Gauge('aBSE', 'BSE')
gAPPS = Gauge('aAPPS', 'APPS')
gBrakePressure = Gauge('aBrakePressure', 'Pressao dos freios')
gSoC = Gauge('aSoC', 'SoC')

#bse_percent = 0, apps_percent = 0, bms_fail = 0, rightInversor_fail = 0, leftInversor_fail = 0, speed = 0, minimal_voltage = 0, maximum_voltage = 0, minimal_temperature = 0, maximum_temperature = 0, minimal_resistance = 0, maximum_resistance = 0, SOC = 0, SOH = 0, bms_ccl = 0, accumulator_voltage = 0, accumulator_current = 0, accumulator_capacity = 0, bms_dcl = 0, rightInversor_temperatureRaw = 0, rightMotor_temperatureRaw = 0, rightMotor_currentRaw = 0, rightMotor_rpm = 0, leftInversor_temperatureRaw = 0, leftMotor_temperatureRaw = 0, leftMotor_currentRaw = 0, leftMotor_rpm = 0, steering_angle = 0, backLeft_suspensionRaw = 0, frontLeft_suspensionRaw = 0, frontRight_suspensionRaw = 0, backRight_suspensionRaw = 0, leftPlanetary_temperatureRaw = 0, rightPlanetary_temperatureRaw = 0, brake_pressureRaw = 0, frontRightBrake_temperatureRaw = 0, ecu_fail = 0



def getSerialData(data):
    bse_percent, apps_percent, bms_fail, rightInversor_fail, leftInversor_fail, speed, minimal_voltage, maximum_voltage, minimal_temperature, maximum_temperature, minimal_resistance, maximum_resistance, SOC, SOH, bms_ccl, accumulator_voltage, accumulator_current, accumulator_capacity, bms_dcl, rightInversor_temperatureRaw, rightMotor_temperatureRaw, rightMotor_currentRaw, rightMotor_rpm, leftInversor_temperatureRaw, leftMotor_temperatureRaw, leftMotor_currentRaw, leftMotor_rpm, steering_angle, backLeft_suspensionRaw, frontLeft_suspensionRaw, frontRight_suspensionRaw, backRight_suspensionRaw, leftPlanetary_temperatureRaw, rightPlanetary_temperatureRaw, brake_pressureRaw, frontRightBrake_temperatureRaw, ecu_fail = data.split(",")
    print(bse_percent, apps_percent, bms_fail, rightInversor_fail, leftInversor_fail, speed, minimal_voltage, maximum_voltage, minimal_temperature, maximum_temperature, minimal_resistance, maximum_resistance, SOC, SOH, bms_ccl, accumulator_voltage, accumulator_current, accumulator_capacity, bms_dcl, rightInversor_temperatureRaw, rightMotor_temperatureRaw, rightMotor_currentRaw, rightMotor_rpm, leftInversor_temperatureRaw, leftMotor_temperatureRaw, leftMotor_currentRaw, leftMotor_rpm, steering_angle, backLeft_suspensionRaw, frontLeft_suspensionRaw, frontRight_suspensionRaw, backRight_suspensionRaw, leftPlanetary_temperatureRaw, rightPlanetary_temperatureRaw, brake_pressureRaw, frontRightBrake_temperatureRaw, ecu_fail)


def updatePrometheusData():
    gVolt.set(random.uniform(130, 150))
    gCurrent.set(random.uniform(0, 500))
    gPower.set(random.uniform(0, 56000))
    gTemperaturePlanetary.set(random.uniform(1, 100))
    gTemperatureMotor.set(random.uniform(1, 100))
    gTemperatureInverter.set(random.uniform(1, 150))
    gTemperatureAcumulatorPeak.set(random.uniform(1, 100))
    gTemperatureAcumulatorAvg.set(random.uniform(1, 130))
    gRPM.set(random.uniform(0, 3000))
    gWheelSpeed.set(random.uniform(0, 100))
    gDCL.set(random.random() * 15 )
    gBSE.set(random.random() * 15 )
    gAPPS.set(random.random() * 15 )
    gBrakePressure.set(random.random() )

    gECUFail.set(1)
    gBMSFail.set(0)
    gIMDFail.set(1)
    gBSPDFail.set(0)

    gSoC.set(random.uniform(1, 100))

 
if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    print("AMP Telemetry Server - DaV2") 
    print("Starting server")
    time.sleep(1)
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
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
        updatePrometheusData()
        time.sleep(1)