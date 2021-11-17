import tkinter as tk
import threading
from tkinter.constants import W
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import os
import pandas as pd
import sys
import warnings

warnings.filterwarnings("ignore")

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('400x200')
        self.title('Plotter')
        first_label = tk.Label(self,text="CV Plotter",font=10)
        first_label.pack(pady=2,padx=2)

    def design(self):
        self.plotbtn = tk.Button(self, text="PLOT", width=25, command=self.plot)
        self.closebtn = tk.Button(self, text="SAVE AND CLOSE", width=25, command=self.close)
        self.quitbtn = tk.Button(self, text="QUIT", width=25, command=self.terminate)
        self.filetxt = tk.Text(self,height=1, width=25)
        self.filetxt.pack()
        self.plotbtn.pack()
        self.closebtn.pack()
        self.quitbtn.pack()

    def plot(self):
        print("============== PLOT OPEN ==============")
        self.plotbtn.config(bg="lawn green")
        self.closebtn.config(bg="grey")
        self.plot_thread = threading.Thread(target=self.plot_proc,args=(),daemon=True)
        self.plot_thread.start()
    
    def close(self):
        print("============== PLOT CLOSED ==============")
        self.plotbtn.config(bg="grey")
        self.closebtn.config(bg="red")
        self.close_thread = threading.Thread(target=self.close_proc,args=(),daemon=True)
        self.close_thread.start()

    def terminate(self):
        print("============== QUIT ==============")
        self.quit()
        self.destroy()
        sys.exit()
   
    def plot_proc(self):
        print("plot process")
        self.filename = str(self.filetxt.get("1.0",'end-1c'))
        path = os.path.join("./log/"+self.filename)
        df = pd.read_csv(path)

        try:
            plt.plot(df['v'],df['i'])
            plt.xlabel("Potential (in V)")
            plt.ylabel("Current (in $\mu$A)")
            plt.title(self.filename)
            plt.show()
        except Exception:
            pass

    def close_proc(self):
        print("close process")
        plt.close()

    def run(self):
        self.design()
        self.mainloop()

if __name__=="__main__":
    app = Application()
    try:
        app.run()

    except Exception as e:
        print(e)
