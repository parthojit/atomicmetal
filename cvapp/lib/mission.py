#separately install NI-VISA and NI-DAQmx driver from National Instruments for operation
import nidaqmx
import time
import pyvisa
import tkinter as tk
import matplotlib.pyplot as plt
import time
import json
import numpy as np
import matplotlib.animation as animation
import serial
import pandas as pd
import threading
from datetime import date

today = date.today()

class control(object):
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.fg = rm.open_resource('USB0::0x0699::0x0353::1738559::INSTR')

    def cdaq_read(self):
        #reads ADC CDAQ-9171
        with nidaqmx.Task() as task:
            try:
                task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0:1")
                data = task.read(number_of_samples_per_channel=1)
                print(data)
                snd = {
                    "voltage": data[0][0], #corrected for WE-CE potential (WE is ground)
                    "current": data[1][0]*10 #corrected current
                    }
                return json.dumps(snd)
            except Exception as e:
                print(e)

    def tek_on(self):
        #switches function generator ON
        try:
            print(self.fg.query('OUTPut1:STATe ON'))
            print('+++ function generator is ON +++')
        except Exception as e:
            print(e)

    def tek_off(self):
        #switches function generator OFF
        try:
            print(self.fg.query('OUTPut1:STATe OFF'))
            print('+++ function generator is OFF +++')
        except Exception as e:
            print(e)
    
    def tek_sweep(self,sr=100,vmax=0.5,vmin=-0.5):
        #generates sweep signal using function generator
        try:
            freq = sr/((vmax-vmin)*2000)
            print('+++ sweep between %s V and %s V at %s mV/s +++' % (str(vmin),str(vmax),str(sr)))    
            self.fg.query('SOUR1:FUNC:SHAP USER0')
            self.fg.query('SOUR1:FREQ %s' % str(freq))
            self.fg.query('SOUR1:VOLT:LEV:IMM:OFFS %s Vpp' % str(((vmax+vmin)/2)))
            self.fg.query('SOUR1:VOLT:LEV:IMM:AMPL %s Vpp' % str(vmax-vmin))
            return 0
        except Exception as e:
            print(e)

    def plotter(self, tmax):
        V = []
        I = []
        T = []

        start = time.time()
        while True:
            try:
                res = json.loads(self.cdaq_read())
                print(res)
                V.append(res['voltage'])
                I.append(res['current'])
                end = time.time()
                T.append(end-start)
            
            except Exception as e:
                print(e)

            if (end-start) > tmax:
                print("--------------------------")
                return T,V,I


if __name__=="__main__":
    print('+++ measurement started +++')
    c1 = control()
    c1.tek_on()
    c1.tek_sweep(sr=100,vmax=0.8,vmin=-0.2)
    while True:
        print(c1.cdaq_read())
        time.sleep(1)
