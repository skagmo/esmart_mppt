#!/usr/bin/python3
# -*- coding: utf-8 -*-

import esmart
import time

def handle_data(d):
	# Correct error in readings
	d['bat_volt'] *= 1.107
	d['load_volt'] *= 1.09
	# Only correct if reading is not zero
	if d['chg_cur']:
		d['chg_cur'] += 1.5

	# chg_power uses uncorrected voltage/current, so recalculate
	actual_power = d['bat_volt']*d['chg_cur']

	print("PV %.1f V, battery %.1f V" % (d['pv_volt'], d['bat_volt']))
	print("Charging %s, %.1f A, %.1f W" % (esmart.DEVICE_MODE[d['chg_mode']], d['chg_cur'], actual_power))
	print("Discharging %.1f V, %.1f A, %.1f W" % (d['load_volt'], d['load_cur'], d['load_power']))

e = esmart.esmart()
e.open("/dev/ttyUSB0")
e.set_callback(handle_data)

while 1:
	e.tick()
	time.sleep(0.001)

