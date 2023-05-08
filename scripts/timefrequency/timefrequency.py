from .dataprovider import DataProvider
from .allan import Allan


class TimeFrequency:
    def __init__(self):
        self.__dp = DataProvider()
        self.__filename_prefix = "None"

    def load_from_daily_csv(self, dir, filename_prefix, time_value_columns):
        self.__filename_prefix = filename_prefix
        self.__dp.load_from_daily_csv(
            dir, self.__filename_prefix, time_value_columns)

    def get_data_summary(self):
        return self.__dp.get_data_summary()

    def generate_adev_plot(self, dir):
        if (len(self.__dp.get_data().index) < 2):
            print("Can't generate ADEV plot as there is not much data for the operation.")
            return

        # calculate Allan deviation assuming data spaced with 1[s] rate
        allan = Allan(self.__dp.get_data()[self.__dp.value_column_name])
        allan.calculate_adev()

        # configure the plot
        data_summary = self.__dp.get_data_summary()
        time_min = data_summary["time_range"][0]
        time_max = data_summary["time_range"][1]
        plot_title = "Allan deviation for \"" + self.__filename_prefix + \
            "\" dataset (" + str(time_min) + " - " + str(time_max) + ")"

        file_name = self.__filename_prefix + "_" + time_min.strftime('%Y%m%d') + \
            "-" + time_max.strftime('%Y%m%d') + "_ADEV"

        # save calculation result as image
        allan.save(dir, file_name, plot_title)

    def generate_mdev_plot(self, dir):
        if (len(self.__dp.get_data().index) < 2):
            print("Can't generate MDEV plot as there is not much data for the operation.")
            return

        # calculate Allan deviation assuming data spaced with 1[s] rate
        allan = Allan(self.__dp.get_data()[self.__dp.value_column_name])
        allan.calculate_mdev()

        # configure the plot
        data_summary = self.__dp.get_data_summary()
        time_min = data_summary["time_range"][0]
        time_max = data_summary["time_range"][1]
        plot_title = "Modified Allan deviation for \"" + self.__filename_prefix + \
            "\" dataset (" + str(time_min) + " - " + str(time_max) + ")"

        file_name = self.__filename_prefix + "_" + time_min.strftime('%Y%m%d') + \
            "-" + time_max.strftime('%Y%m%d') + "_MDEV"

        # save calculation result as image
        allan.save(dir, file_name, plot_title)
