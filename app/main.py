from prometheus_client import start_http_server, Summary, Counter, Gauge
import prometheus_client as prom
import random
import time

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
    print("Starting server")
    while True:
        updatePrometheusData()
        time.sleep(1)