import time
import matplotlib.pyplot as plt
from lib.mission import control
import json
import pandas as pd

class CV(object):
    def __init__(self):
        self.c = control()
        self.figure,self.ax = plt.subplots(2,2,figsize=(10,6))
        self.volt = []
        self.curr = []
        self.time = []
        self.start = time.time()
        self.count = 1

    def run(self):
        self.c.tek_on()
        self.flag = 1
        while self.flag==1:
            try:
                print(self.c.cdaq_read())
                data = json.loads(self.c.cdaq_read())
                self.volt.append(data['voltage'])
                self.curr.append(data['current'])
                time.sleep(0.1)
            except KeyboardInterrupt:
                print("Interrupt!")
                break
        return

    def stop(self):
        self.flag = 0
        print("cv stopped")
        df = pd.DataFrame(list(zip(self.volt,self.curr)),columns=['v','i'])
        df.to_csv("./log/temp"+str(self.count)+'.csv') # save log
        return

    
if __name__=="__main__":
    print("+++ cv measurement started +++")
    c = CV()
    c.run()