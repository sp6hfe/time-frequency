from .dataprovider import DataProvider


class TimeFrequency:
    def __init__(self, time_column_name, value_column_name):
        self.__dp = DataProvider(time_column_name, value_column_name)

    def load_csv_data(self, data_dir, data_filename_prefix):
        self.__dp.load_csv(data_dir, data_filename_prefix)

    def get_loaded_files_no(self):
        return self.__dp.get_loaded_files_no()

    def get_data_range_min(self):
        return self.__dp.get_data_range_min()

    def get_data_range_max(self):
        return self.__dp.get_data_range_max()

    def get_data(self):
        return self.__dp.get_data()

    def get_data_no(self):
        return self.__dp.get_data_no()

    def get_raw_data(self):
        return self.__dp.get_raw_data()

    def get_raw_data_no(self):
        return self.__dp.get_raw_data_no()
