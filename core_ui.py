import tkinter as tk
from tkinter import messagebox
import seabreeze
from seabreeze.spectrometers import Spectrometer
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from testing_utils import generate_dummy_spectra
import random

root = tk.Tk()
root.resizable(0, 0)
root.title("Spectrometer Tool")
matplotlib.use("TkAgg")

device_name = tk.StringVar()
device_name.set('No Device Detected')

int_time_entry = tk.StringVar()
int_time_entry.set("2")
int_time = 2  # default integration time = 2us

trigger_mode = tk.StringVar()
trigger_mode.set("0")

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

fig = plt.Figure(figsize=(5, 5), dpi=100)
spectra_plot = fig.add_subplot(111)
spectra_plot.set_ylabel('Intensity')
spectra_plot.set_xlabel('Wavelength [nm]')
spectra_plot.set_title('Observed Emission Spectra')


def update_plot():
    if not devices:
        t_data = generate_dummy_spectra(central_spectra=(random.randint(300, 500), random.randint(500, 700),
                                                         random.randint(700, 900)))
        ref = messagebox.askyesno('Error', "Error: No device detected. Use Testing Data?")
        if ref:  # refresh with sample data
            spectra_plot.clear()
            spectra_plot.set_ylabel('Intensity')
            spectra_plot.set_xlabel('Wavelength [nm]')
            spectra_plot.set_title('Observed Emission Spectra')
            spectra_plot.plot(t_data[0], t_data[1])
            canvas.draw()
    else:
        spectra_plot.clear()
        spectra_plot.set_ylabel('Intensity')
        spectra_plot.set_xlabel('Wavelength [nm]')
        spectra_plot.set_title('Observed Emission Spectra')
        spectra_plot.plot(spec.wavelengths(), spec.intensities())
        canvas.draw()


def reconnect_device():
    global spec
    if seabreeze.spectrometers.list_devices():
        spec = seabreeze.spectrometers.Spectrometer.from_first_available()
        device_name.set(spec.serial_number)
    else:
        messagebox.showerror("ERROR", "ERROR: No Device Detected")


if test_mode:
    tst_data = generate_dummy_spectra(central_spectra=(random.randint(300, 500), random.randint(500, 700),
                                                       random.randint(700, 900)))
    spectra_plot.plot(tst_data[0], tst_data[1])

elif not devices:
    spectra_plot.plot(0, 0)
else:
    spec = seabreeze.spectrometers.Spectrometer.from_first_available()
    spectra_plot.plot(spec.wavelengths(), spec.intensities())
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=20)  # plot initial data

tk.Label(root, text="Connected Device:").grid(row=0, column=0)
tk.Label(root, textvariable=device_name, bg="White", relief=tk.GROOVE).grid(row=0, column=1, sticky="NSEW")

reconnect = tk.Button(root, text="Reconnect Device", command=reconnect_device)
reconnect.grid(row=0, column=2, columnspan=2, sticky="NSEW")

tk.Label(text="Sampling Controls", relief=tk.GROOVE).grid(row=1, columnspan=2, column=2, sticky="NSEW")

refresh = tk.Button(root, text="Refresh Data", command=update_plot)
refresh.grid(row=2, column=2, columnspan=2, sticky="NSEW")

tk.Label(root, text="Integration Time [μs]", relief=tk.GROOVE).grid(row=3, column=2, sticky="NSEW")
int_entry = tk.Entry(textvariable=int_time_entry, relief=tk.FLAT, bg="white")
int_entry.grid(row=3, column=3, sticky="NSEW")

tk.Label(root, text="Trigger Mode", relief=tk.GROOVE).grid(row=4, column=2, sticky="NSEW")
trigger_mode_entry = tk.Entry(root, textvariable=trigger_mode, relief=tk.FLAT, bg="white")
trigger_mode_entry.grid(row=4, column=3, sticky="NSEW")


def update_integration_time(a, b, c):
    global int_time
    if not int_time_entry:
        int_entry.config(bg='red')
    else:
        try:
            t = float(int_time_entry.get())
            if t:
                int_time = t
                int_entry.config(bg="white")
            else:
                int_entry.config(bg="red")
        except Exception:
            int_entry.config(bg="red")


int_time_entry.trace_variable('w', update_integration_time)

root.mainloop()
