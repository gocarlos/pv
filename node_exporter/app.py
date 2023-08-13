from dataclasses import dataclass
import logging
from typing import List
from prometheus_client import Gauge, start_http_server
from flask import Flask
import time
from prometheus_client import Histogram
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@dataclass
class InverterMetrics():
    current_dc_power: int
    current_ac_power: int


@dataclass
class AhoyDTUMetrics():
    inverterMetrics: List[InverterMetrics]
    total_dc_power: float
    total_ac_power: float


total_dc_power_gauge = Gauge('total_dc_power_gauge', 'total_dc_power')
total_ac_power_gauge = Gauge('total_ac_power_gauge', 'total_ac_power')
total_dc_power_histogram = Histogram('total_dc_power_histogram', 'total_dc_power')
total_ac_power_histogram = Histogram('total_ac_power_histogram', 'total_ac_power')


def start_monitoring():
    logger.info('starting monitoring...')
    start_http_server(8000)
    while True:
        ahoy_metrics = get_ahoy_dtu_metrics()
        logger.info(ahoy_metrics)
        export_metrics(ahoy_metrics)
        time.sleep(5)


def get_ahoy_dtu_metrics() -> AhoyDTUMetrics:
    logger.info('getting ahoy dtu metrics...')
    response = requests.get('http://192.168.0.57/api/record/live')
    inverter_0 = response.json()['inverter'][0]
    inverter_1 = response.json()['inverter'][1]
    inverter_2 = response.json()['inverter'][2]

    inverter_0_metrics = InverterMetrics(
        current_dc_power=float(inverter_0[2]['val']),
        current_ac_power=float(inverter_0[8]['val'])
    )

    inverter_1_metrics = InverterMetrics(
        current_dc_power=float(inverter_1[2]['val']),
        current_ac_power=float(inverter_1[8]['val'])
    )

    inverter_2_metrics = InverterMetrics(
        current_dc_power=float(inverter_2[2]['val']),
        current_ac_power=float(inverter_2[8]['val'])
    )

    ahoyMetrics = AhoyDTUMetrics(
        inverterMetrics=[
            inverter_0_metrics,
            inverter_1_metrics,
            inverter_2_metrics,
        ],
        total_dc_power=sum([
            inverter_0_metrics.current_dc_power,
            inverter_1_metrics.current_dc_power,
            inverter_2_metrics.current_dc_power
        ]),
        total_ac_power=sum([
            inverter_0_metrics.current_ac_power,
            inverter_1_metrics.current_ac_power,
            inverter_2_metrics.current_ac_power
        ])
    )
    logger.info(ahoyMetrics)
    return ahoyMetrics


def export_metrics(metrics: AhoyDTUMetrics):
    logger.warning('exporting metrics...')

    total_dc_power_gauge.set(metrics.total_dc_power)
    total_ac_power_gauge.set(metrics.total_ac_power)

    total_dc_power_histogram.observe(metrics.total_dc_power)
    total_ac_power_histogram.observe(metrics.total_ac_power)


@app.route('/')
def main():
    return "hello world"


if __name__ == "__main__":
    logger.info('staring application')
    start_monitoring()
