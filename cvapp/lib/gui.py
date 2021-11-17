from lib.mission import control
from lib.cv import CV
import tkinter as tk
import threading
import sys
import matplotlib.pyplot as plt


class Application(tk.Tk):
    #GUI application based on Tkinter
    def __init__(self):
        tk.Tk.__init__(self)
        self.c1 = control()
        self.cv = CV()
        self.geometry('500x500')
        self.title('Mission Control')
        first_label = tk.Label(self,text="Cyclic Voltammetry",font=10)
        first_label.pack(pady=2,padx=2)
 
    def design(self):
        on_tek = tk.Button(self, text="TEK ON", width=25, command=self.c1.tek_on)
        off_tek = tk.Button(self, text="TEK OFF", width=25, command=self.c1.tek_off)
        quitbtn = tk.Button(self, text="QUIT", width=25, command=self.gui_quit)
        sweepbtn = tk.Button(self, text="SET SWEEP", width=25, command=self.sweep)
        startbtn = tk.Button(self, text="START", width=25, command=self.start)
        stopbtn = tk.Button(self, text="STOP", width=25, command=self.stop)
        self.filetxt = tk.Text(self,height=1, width=25)
        on_tek.pack()
        off_tek.pack()
        sweepbtn.pack()
        startbtn.pack()
        self.filetxt.pack()
        stopbtn.pack()
        quitbtn.pack()

    def sweep(self):
        try:
            sr = int(input("Enter sweep rate (mV/sec):"))
            vmax = float(input("Enter vMax (V):"))
            vmin = float(input("Enter vMin (V):"))
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
        self.c1.tek_on()
        self.c1.tek_sweep(sr=sr,vmax=vmax,vmin=vmin)
        return 0

    def start(self):
        start_thread = threading.Thread(target=self.start_proc,args=())
        start_thread.start()

    def stop(self):
        stop_thread = threading.Thread(target=self.stop_proc,args=())
        stop_thread.start()
   
    def gui_quit(self):
        quit_thread = threading.Thread(target=self.quit_proc,args=())
        quit_thread.start()

    def run(self):
        self.design()
        self.mainloop()

    def start_proc(self):
        self.cv.run()
        return

    def stop_proc(self):
        self.cv.stop()
        return
    
    def quit_proc(self):
        self.c1.tek_off()
        self.cv.stop()
        self.quit()
        self.destroy()
        return
        
    