from prometheus_client import start_http_server, Summary, Counter, Gauge
import prometheus_client as prom
import random
import time

# Create a metric to track time spent and requests made.
gVolt = Gauge('Voltage', 'tensao do sistema')
gCurrent = Gauge('current', 'corrente do sistema')

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        gVolt.set(random.random() * 15 - 5)
        gCurrent.set(random.random() * 15 - 5)
        time.sleep(1)