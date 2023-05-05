from .dataprovider import DataProvider
from .allan import Allan


class TimeFrequency:
    def __init__(self):
        self.__dp = DataProvider()
        self.__filename_prefix = "None"

    def load_from_daily_csv(self, dir, filename_prefix, time_column_name, value_column_name):
        self.__filename_prefix = filename_prefix
        self.__dp.load_from_daily_csv(
            dir, self.__filename_prefix, time_column_name, value_column_name)

    def generate_mdev_plot(self, dir):
        if (len(self.__dp.get_data().index) < 2):
            print("Can't generate MDEV plot as there is not much data for the operation.")
            return

        # calculate Allan deviation assuming data spaced with 1[s] rate
        allan = Allan(self.__dp.get_data()[self.__dp.value_column_name])
        allan.calculate_mdev()

        # configure the plot
        plot_title = "Modified Allan deviation for \"" + self.__filename_prefix + \
            "\" dataset (" + str(self.__dp.get_data_range_min()) + \
            " - " + str(self.__dp.get_data_range_max()) + ")"

        file_name = self.__filename_prefix + "_" + self.__dp.get_data_range_min().strftime('%Y%m%d') + \
            "-" + self.__dp.get_data_range_max().strftime('%Y%m%d')

        # save calculation result as image
        allan.save(dir, file_name, plot_title)
