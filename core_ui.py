import tkinter as tk
from tkinter import messagebox
import numpy as np
import seabreeze
from seabreeze.spectrometers import Spectrometer
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from testing_utils import generate_dummy_spectra
from data_utils import get_plot

root = tk.Tk()
root.resizable(0, 0)
matplotlib.use("TkAgg")

device_name = tk.StringVar()
device_name.set('No Device Detected')


collect_control = True  # enable collection controls
sample_control = True  # enable sampling controls
test_mode = False  # activate test mode
spec = None

devices = seabreeze.spectrometers.list_devices()

while not devices:
    collect_control = False
    sample_control = False
    con = messagebox.askretrycancel('ERROR: No Device Detected', 'ERROR: could not connect to spectrometer')
    if con:
        devices = seabreeze.spectrometers.list_devices()
    else:
        test_mode = messagebox.askyesno("Use Test Data", "Use Random Test Data?\nSensor can be acquired at any point")
        break

if test_mode:
    fig = get_plot(device=None, test=True)
elif not devices:
    fig = get_plot(device=None, test=False)
else:
    spec = seabreeze.spectrometers.Spectrometer.from_first_available()
    fig = get_plot(device=spec, test=False)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)  # plot initial data


def update_plot():
    if not devices:
        # messagebox.showerror('Error', "Error: No device detected")
        f = get_plot(test=False)
        cv = FigureCanvasTkAgg(fig, master=root)
        cv.get_tk_widget().grid(row=1, column=0, columnspan=2)  # plot initial data
    else:
        pass


tk.Label(root, text="Connected Device:").grid(row=0, column=0)
tk.Label(root, textvariable=device_name, bg="White", relief=tk.GROOVE).grid(row=0, column=1, sticky="NSEW")

refresh = tk.Button(root, text="Refresh", command=update_plot)
refresh.grid(row=1, column=2)
root.mainloop()
