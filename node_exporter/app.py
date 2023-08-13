from dataclasses import dataclass
import logging
from typing import List, Tuple
from prometheus_client import Gauge, start_http_server
# from flask import Flask
import time
from prometheus_client import Histogram
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# app = Flask(__name__)


@dataclass
class InverterMetrics():
    current_dc_power: float
    current_ac_power: float
    current_dc_0: Tuple[str, float]
    current_dc_1: Tuple[str, float]


@dataclass
class AhoyDTUMetrics():
    inverterMetrics: List[InverterMetrics]
    total_dc_power: float
    total_ac_power: float


total_dc_power_gauge = Gauge('total_dc_power_gauge', 'total_dc_power')
total_ac_power_gauge = Gauge('total_ac_power_gauge', 'total_ac_power')
total_dc_power_histogram = Histogram('total_dc_power_histogram', 'total_dc_power')
total_ac_power_histogram = Histogram('total_ac_power_histogram', 'total_ac_power')


current_dc_power_histogram_west = Histogram('current_dc_power_histogram_west', 'current_dc_power_histogram_west')
current_dc_power_histogram_top = Histogram('current_dc_power_histogram_top', 'current_dc_power_histogram_top')
current_dc_power_histogram = Histogram('current_dc_power_histogram', 'current_dc_power_histogram_')
current_dc_power_histogram_aa = Histogram('current_dc_power_histogram_aa', 'current_dc_power_histogram_aa')
current_dc_power_histogram_bb = Histogram('current_dc_power_histogram_bb', 'current_dc_power_histogram_bb')


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

    inverter_0 = requests.get('http://192.168.0.57/api/inverter/id/0').json()['ch']
    inverter_1 = requests.get('http://192.168.0.57/api/inverter/id/1').json()['ch']
    inverter_2 = requests.get('http://192.168.0.57/api/inverter/id/2').json()['ch']

    inverter_0_metrics = InverterMetrics(
        current_ac_power=float(inverter_0[0][2]),
        current_dc_power=float(inverter_0[0][8]),
        current_dc_0=('west', inverter_0[1][2]),
        current_dc_1=('top', inverter_0[2][2])
    )

    inverter_1_metrics = InverterMetrics(
        current_ac_power=float(inverter_1[0][2]),
        current_dc_power=float(inverter_1[0][8]),
        current_dc_0=('', inverter_1[1][2]),
        current_dc_1=('', 0)
    )

    inverter_2_metrics = InverterMetrics(
        current_ac_power=float(inverter_2[0][2]),
        current_dc_power=float(inverter_2[0][8]),
        current_dc_0=('aa', inverter_2[1][2]),
        current_dc_1=('bb', inverter_2[2][2])
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

    current_dc_power_histogram_west.observe(metrics.inverterMetrics[0].current_dc_0[1])
    current_dc_power_histogram_top.observe(metrics.inverterMetrics[0].current_dc_1[1])
    current_dc_power_histogram.observe(metrics.inverterMetrics[1].current_dc_0[1])
    current_dc_power_histogram_aa.observe(metrics.inverterMetrics[2].current_dc_0[1])
    current_dc_power_histogram_bb.observe(metrics.inverterMetrics[2].current_dc_1[1])


# @app.route('/')
# def main():
#     return "hello world"


if __name__ == "__main__":
    logger.info('staring application')
    start_monitoring()
