import pandas as pd
import allantools
from pathlib import Path


class Allan:
    def __init__(self, data_set, rate=1.0, data_type="freq"):
        self.__data_set = data_set
        self.__rate = rate
        self.__data_type = data_type

        self.__allan_data = None
        self.__allan_metric = None

    def calculate_mdev(self, taus="octave"):
        self.__allan_metric = "MDEV"
        print("Calculating " + self.__allan_metric + "...")

        self.__allan_data = allantools.Dataset(
            self.__data_set, rate=self.__rate, data_type=self.__data_type, taus=taus)

        self.__allan_data.compute("mdev")

    def save(self, out_dir, file_name, plot_title):
        if self.__allan_data is None:
            print("No data to save. Calculate wanted statistic first!")
            return

        plot = allantools.Plot()
        plot.plot(self.__allan_data, errorbars=False, grid=True)

        # nicely prints on A4
        plot.fig.set_size_inches(11, 6, True)

        plot.fig.suptitle(plot_title)

        plot.ax.set_xlabel("Tau [s]")
        plot.ax.set_ylabel(self.__allan_metric)

        file_name_path = Path(out_dir) / file_name
        plot.save(file_name_path)
        print(self.__allan_metric + " saved as: " +
              str(file_name_path) + ".png")
