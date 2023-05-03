from .dataprovider import DataProvider
from .allan import Allan


class TimeFrequency:
    def __init__(self, time_column_name, value_column_name):
        self.__time_column_name = time_column_name
        self.__value_column_name = value_column_name
        self.__dp = DataProvider(
            self.__time_column_name, self.__value_column_name)
        self.__data_filename_prefix = "None"

    def load_csv_data(self, data_dir, data_filename_prefix):
        self.__data_filename_prefix = data_filename_prefix
        self.__dp.load_csv(data_dir, self.__data_filename_prefix)

    def generate_mdev_plot(self, out_dir):
        allan = Allan(self.__dp.get_data()[self.__value_column_name])
        allan.calculate_mdev()

        plot_title = "Modified Allan deviation for \"" + self.__data_filename_prefix + \
            "\" dataset (" + str(self.__dp.get_data_range_min()) + \
            " - " + str(self.__dp.get_data_range_max()) + ")"

        file_name = self.__data_filename_prefix + "_" + self.__dp.get_data_range_min().strftime('%Y%m%d') + \
            "-" + self.__dp.get_data_range_max().strftime('%Y%m%d')

        allan.save(out_dir, file_name, plot_title)
