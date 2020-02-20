import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import seabreeze
from seabreeze.spectrometers import Spectrometer
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from testing_utils import generate_dummy_spectra
import random
import data_utils
import csv

root = tk.Tk()
root.resizable(0, 0)
root.title("Spectrometer Tool")
matplotlib.use("TkAgg")

device_name = tk.StringVar()
device_name.set('No Device Detected')

int_time_entry = tk.StringVar()
int_time_entry.set("100000")
int_time = int(1E5)  # default integration time = 20us

trigger_mode_entry = tk.StringVar()
trigger_mode_entry.set('0')
trigger_mode = 0

collect_control = True  # enable collection controls
sample_control = True  # enable sampling controls
test_mode = False  # activate test mode
spec = None

spec_range = None
spec_intensity = None

max_intensity_var = tk.StringVar()
max_intensity_var.set('N/A')
integration_limits_var = tk.StringVar()
integration_limits_var.set('N/A')
pixel_var = tk.StringVar()
pixel_var.set('N/A')
sample_var = tk.StringVar()
sample_var.set('N/A')

devices = seabreeze.spectrometers.list_devices()

# while not devices:
#     collect_control = False
#     sample_control = False
#     con = messagebox.askretrycancel('ERROR: No Device Detected', 'ERROR: could not connect to spectrometer')
#     if con:
#         devices = seabreeze.spectrometers.list_devices()
#     else:
#         test_mode = messagebox.askyesno("Use Test Data", "Use Random Test Data?\nSensor can be acquired at any point")
#         break

fig = plt.Figure(figsize=(5, 5), dpi=100)
spectra_plot = fig.add_subplot(111)
spectra_plot.set_ylabel('Intensity')
spectra_plot.set_xlabel('Wavelength [nm]')
# spectra_plot.set_xlim([350, 1000])  # set bounds to relevant data
spectra_plot.set_title('Observed Emission Spectra')


def update_plot():  # take a fresh sample from source
    global spec_range
    global spec_intensity
    if not devices:
        t_data = generate_dummy_spectra(central_spectra=(random.randint(300, 500), random.randint(500, 700),
                                                         random.randint(700, 900)))
        ref = messagebox.askyesno('Error', "Error: No device detected. Use Testing Data?")
        if ref:  # refresh with sample data
            spectra_plot.clear()
            spectra_plot.set_ylabel('Intensity')
            spectra_plot.set_xlabel('Wavelength [nm]')
            # spectra_plot.set_xlim([350, 1000])  # set bounds to relevant data
            spectra_plot.set_title('Observed Emission Spectra')
            spectra_plot.plot(t_data[0], t_data[1])
            canvas.draw()
    else:
        spec_range = spec.wavelengths()
        spec_intensity = spec.intensities()
        for i in range(len(spec_range)):  # filter out data from under 200 nm
            if spec_range[i] <= 300:
                spec_range[i] = None
                spec_intensity[i] = None
        spec_range = list(filter(None, spec_range))
        spec_intensity = list(filter(None, spec_intensity))
        spec.trigger_mode(trigger_mode)  # set trigger mode
        spec.integration_time_micros(int_time)  # set integration_time

        # update plot
        spectra_plot.clear()
        spectra_plot.set_ylabel('Intensity')
        spectra_plot.set_xlabel('Wavelength [nm]')
        # spectra_plot.set_xlim([350, 1000])  # set bounds to relevant data
        spectra_plot.set_title('Observed Emission Spectra')
        spectra_plot.plot(spec_range, spec_intensity)
        # print('Min:', spec.wavelengths().min(axis=0, initial=None))
        # print('Max:', spec.wavelengths().max(axis=0, initial=None))

        canvas.draw()

        # update settings bar
        pixel_var.set(spec.pixels)
        integration_limits_var.set(spec.integration_time_micros_limits)
        max_intensity_var.set(max(spec_intensity))
        sample_var.set(len(spec_range))


def reconnect_device():
    global spec
    if seabreeze.spectrometers.list_devices():
        spec = seabreeze.spectrometers.Spectrometer.from_first_available()
        device_name.set(spec.serial_number)
    else:
        messagebox.showerror("ERROR", "ERROR: No Device Detected")


def export_plot():
    name = filedialog.asksaveasfilename(initialdir="./",
                                        title="Select file",
                                        filetypes=(("PNG", "*.png"), ("all files", "*.*")))
    if name:
        fig.savefig(name)


def export_csv():
    try:
        name = filedialog.asksaveasfilename(initialdir="./",
                                            title="Select file",
                                            filetypes=(("CSV data", "*.csv"), ("all files", "*.*")))
        with open(name, 'w', newline='') as f:
            data_writer = csv.writer(f, delimiter=',', quotechar="|", quoting=csv.QUOTE_MINIMAL)
            data_writer.writerow(['Wavelength [nm]', 'Intensity'])
            for i in range(len(spec_range)):
                data_writer.writerow([spec_range[i], spec_intensity[i]])
    except ValueError:
        pass


if test_mode:
    tst_data = generate_dummy_spectra(central_spectra=(random.randint(300, 500), random.randint(500, 700),
                                                       random.randint(700, 900)))
    spectra_plot.plot(tst_data[0], tst_data[1])

elif not devices:
    spectra_plot.plot(0, 0)
else:
    spec = seabreeze.spectrometers.Spectrometer.from_first_available()
    spectra_plot.plot(spec.wavelengths(), spec.intensities())
    device_name.set(spec.serial_number)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, rowspan=20)  # plot initial data

tk.Label(root, text="Connected Device:").grid(row=0, column=0)
tk.Label(root, textvariable=device_name, bg="White", relief=tk.GROOVE).grid(row=0, column=1, sticky="NSEW")

reconnect = tk.Button(root, text="Reconnect Device", command=reconnect_device)
reconnect.grid(row=0, column=2, columnspan=2, sticky="NSEW")
reconnect.config(state=tk.DISABLED)

tk.Label(text="Sampling Controls", relief=tk.GROOVE).grid(row=1, columnspan=2, column=2, sticky="NSEW")

refresh = tk.Button(root, text="Refresh Data", command=update_plot)
refresh.grid(row=4, column=2, columnspan=2, sticky="NSEW")

tk.Label(root, text="Integration Time [μs]", relief=tk.GROOVE).grid(row=2, column=2, sticky="NSEW")
int_entry = tk.Entry(textvariable=int_time_entry, relief=tk.FLAT, bg="white")
int_entry.grid(row=2, column=3, sticky="NSEW")

tk.Label(root, text="Trigger Mode", relief=tk.GROOVE).grid(row=3, column=2, sticky="NSEW")
trigger_entry = tk.Entry(root, textvariable=trigger_mode_entry, relief=tk.FLAT, bg="white")
trigger_entry.grid(row=3, column=3, sticky="NSEW")

tk.Label(root, text="Current Settings", relief=tk.GROOVE).grid(row=5, column=2, columnspan=2, sticky="NSEW")
tk.Label(root, text="Max Intensity", relief=tk.GROOVE).grid(row=6, column=2, sticky="NSEW")
tk.Label(root, textvariable=max_intensity_var, bg='gray', relief=tk.FLAT).grid(row=6, column=3, sticky="NSEW")
tk.Label(root, text="Integration Bounds", relief=tk.GROOVE).grid(row=7, column=2, sticky="NSEW")
tk.Label(root, textvariable=integration_limits_var, bg='gray', relief=tk.FLAT).grid(row=7, column=3, sticky="NSEW")
tk.Label(root, text="Pixel Count", relief=tk.GROOVE).grid(row=8, column=2, sticky="NSEW")
tk.Label(root, textvariable=pixel_var, bg='gray', relief=tk.FLAT).grid(row=8, column=3, sticky="NSEW")
tk.Label(root, text="Sample Count", relief=tk.GROOVE).grid(row=9, column=2, sticky="NSEW")
tk.Label(root, textvariable=sample_var, bg='gray', relief=tk.FLAT).grid(row=9, column=3, sticky="NSEW")

img_button = tk.Button(root, text='Export Image', command=export_plot)
img_button.grid(row=10, column=2, columnspan=2, sticky="NSEW")

csv_button = tk.Button(root, text='Export CSV', command=export_csv)
csv_button.grid(row=11, column=2, columnspan=2, sticky="NSEW")


def update_integration_time(a, b, c):
    global int_time
    if not int_time_entry:
        int_entry.config(bg='red')
    else:
        try:
            t = int(int_time_entry.get())
            if t:
                int_time = t
                int_entry.config(bg="white")
            else:
                int_entry.config(bg="red")
        except ValueError:
            int_entry.config(bg="red")


def update_trigger_mode(a, b, c):
    global trigger_mode
    if not trigger_mode_entry:
        trigger_entry.config(bg='red')
    else:
        try:
            t = int(trigger_mode_entry.get())
            if t in range(0, 4):
                trigger_mode = t
                trigger_entry.config(bg='white')
            else:
                trigger_entry.config(bg='red')
        except ValueError:
            trigger_entry.config(bg='red')


trigger_mode_entry.trace_variable('w', update_trigger_mode)
int_time_entry.trace_variable('w', update_integration_time)
update_plot()

root.mainloop()
