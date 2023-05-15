import pandas as pd
import allantools
from pathlib import Path


class Allan:
    def __init__(self, data_set, rate=1.0, data_type="freq"):
        self.__data_set = data_set
        self.__rate = rate
        self.__data_type = data_type

        self.__allan_data = None
        self.__allan_result = {"taus": None,
                               "stat": None,
                               "stat_err": None,
                               "stat_n": None,
                               "stat_id": None}

    def calculate_adev(self, taus="octave"):
        if not self.__source_data_available():
            print("Can't calculate ADEV due to missing source data!")
            return

        print("Calculating ADEV...")

        self.__allan_data = allantools.Dataset(
            self.__data_set, rate=self.__rate, data_type=self.__data_type, taus=taus)

        self.__allan_data.compute("adev")
        self.__copy_computation_result()

    def calculate_mdev(self, taus="octave"):
        if not self.__source_data_available():
            print("Can't calculate MDEV due to missing source data!")
            return

        print("Calculating MDEV...")

        self.__allan_data = allantools.Dataset(
            self.__data_set, rate=self.__rate, data_type=self.__data_type, taus=taus)

        self.__allan_data.compute("mdev")
        self.__copy_computation_result()

    def save(self, out_dir, file_name, plot_title):
        if not self.__computation_result_available():
            print("No data to save. Calculate wanted statistic first!")
            return

        plot = allantools.Plot()
        plot.plot(self.__allan_data, errorbars=False, grid=True)

        # nicely prints on A4
        plot.fig.set_size_inches(11, 6, True)

        plot.fig.suptitle(plot_title)

        plot.ax.set_xlabel("Tau [s]")
        plot.ax.set_ylabel(str(self.__allan_result["stat_id"]).upper())

        file_name_path = Path(out_dir) / file_name
        plot.save(file_name_path)
        print(str(self.__allan_result["stat_id"]).upper() + " saved as: " +
              str(file_name_path) + ".png")

    # PRIVATE METHODS #

    def __source_data_available(self):
        return len(self.__data_set) >= 3

    def __computation_result_available(self):
        return self.__allan_result is not None

    def __copy_computation_result(self):
        # selective copy of the computation result
        for key in self.__allan_result.keys():
            if (key in self.__allan_data.out.keys()):
                self.__allan_result[key] = self.__allan_data.out[key]
