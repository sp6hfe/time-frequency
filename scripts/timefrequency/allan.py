import pandas as pd
import allantools
from pathlib import Path


class Allan:
    def __init__(self, data_set, data_set_name, rate=1.0, data_type="freq"):
        self.__data_set = data_set
        self.__data_set_name = data_set_name
        self.__rate = rate
        self.__data_type = data_type

        self.__allan_data = None
        self.__allan_metric = "Nothing"

    def calculate_mdev(self, taus="octave"):
        self.__allan_data = allantools.Dataset(
            self.__data_set, rate=self.__rate, data_type=self.__data_type, taus=taus)

        self.__allan_data.compute("mdev")
        self.__allan_metric = "MDEV"

    def save(self, out_directory, file_name):
        if self.__allan_data is None:
            return

        plot = allantools.Plot()
        plot.plot(self.__allan_data, errorbars=False, grid=True)

        plot.fig.set_size_inches(11, 6, True)
        plot.fig.suptitle("Frequency stability for " + self.__data_set_name)

        plot.ax.set_xlabel("Tau [s]")
        plot.ax.set_ylabel(self.__allan_metric)

        result_path = Path(out_directory) / file_name
        plot.save(result_path)
