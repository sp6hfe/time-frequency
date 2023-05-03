import pandas as pd
from pathlib import Path
from datetime import datetime


class DataProvider:
    def __init__(self, time_column_name, value_column_name):
        self.__time_column_name = time_column_name
        self.__value_column_name = value_column_name

        self.__raw_data = pd.DataFrame(
            columns=[self.__time_column_name, self.__value_column_name])
        self.__resampled_data = pd.DataFrame(columns=self.__raw_data.columns)

        self.__date_path = []
        self.__loaded_files_no = 0

    def load_csv(self, data_dir, data_filename_prefix):
        data_filename_suffix = '[0-9][0-9][0-9][0-9][0-9][0-9].csv'
        self.__resampled_data = pd.DataFrame(
            columns=self.__resampled_data.columns)
        self.__loaded_files_no = 0

        # get a list of all matching files
        data_set_file_paths = sorted(Path(data_dir).glob(
            data_filename_prefix + data_filename_suffix))

        # create a tuples with measurement dates and file paths
        self.__date_path.clear()
        for path in data_set_file_paths:
            file_name = Path(path).name
            # data acquisition day is last 6 digits of the file name (format: YYMMDD)
            date_str = file_name[-10:-4]
            date = datetime.strptime(date_str, '%y%m%d')
            self.__date_path.append((date, path))

        # load data iteratively
        for _, path in self.__date_path:
            new_data = pd.read_csv(path, comment='#', usecols=[self.__time_column_name, self.__value_column_name], parse_dates=[
                self.__time_column_name], dtype={self.__value_column_name: float})
            self.__raw_data = pd.concat([self.__raw_data, new_data], axis=0)
            self.__loaded_files_no += 1

        # index this dataset by time
        self.__raw_data.set_index(self.__time_column_name, inplace=True)

        # resample dataset
        self.__resample_1s()

    def get_loaded_files_no(self):
        return self.__loaded_files_no

    def get_data_range_min(self):
        return self.__raw_data.index.min()

    def get_data_range_max(self):
        return self.__raw_data.index.max()

    def get_raw_data_no(self):
        return len(self.__raw_data.index)

    def get_raw_data(self):
        return self.__raw_data

    def get_data_no(self):
        return len(self.__resampled_data.index)

    def get_data(self):
        return self.__resampled_data

    # PRIVATE METHODS #

    def __resample_1s(self):
        if(len(self.__raw_data.index) < 2):
            # nothing to resample due to missing data
            return

        # resample to 1[s] interval by interpolation
        self.__resampled_data = self.__raw_data.resample('1S').interpolate()
        # create new timebase in the range of the raw data
        start_time = self.__raw_data.index[0]
        end_time = self.__raw_data.index[-1]
        data_points_times = pd.date_range(start_time, end_time, freq='1S')
        # and reindex in order to calculate newly added points
        self.__resampled_data = self.__resampled_data.reindex(
            data_points_times)
