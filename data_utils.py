import seabreeze
from seabreeze.spectrometers import Spectrometer
from testing_utils import generate_dummy_spectra
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import random
from tkinter import filedialog
import pickle
matplotlib.use("TkAgg")


def get_plot(device=None, test=False):
    if not device:  # no device, return empty plot
        fig = plt.Figure(figsize=(5, 5), dpi=100)
        spectra_plot = fig.add_subplot(111)
        spectra_plot.set_ylabel('Intensity')
        spectra_plot.set_xlabel('Wavelength [nm]')
        spectra_plot.set_title('Observed Emission Spectra')
        if test:
            spectra = generate_dummy_spectra(central_spectra=(random.randint(300, 800), 600, random.randint(600, 1064)))
            spectra_plot.plot(spectra[0], spectra[1])
        elif not device:
            spectra_plot.plot(0, 0)
        else:
            spectra_plot.plot(device.wavelengths(), device.intensities())
        return fig


def export_plot():
    pass


def export_csv():
    pass


def pickle_data(device):
    fp = filedialog.asksaveasfilename(initialdir="./",
                                      title="Select file",
                                      filetypes=(("pickled data", "*.p"), ("all files", "*.*")))
    f = open(fp, 'wb')
    pickle.dump(device, f)


def unpickle_data():
    name = filedialog.askopenfilename(initialdir="./",
                                      title="Select file",
                                      filetypes=(("pickled data", "*.p"), ("all files", "*.*")))
    pickle.load(open(name, 'rb'))
