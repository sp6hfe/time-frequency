import pandas as pd
from pathlib import Path
from datetime import datetime


class DataProvider:
    def __init__(self):
        self.time_column_name = "time"
        self.value_column_name = "value"

        self.__raw_data = pd.DataFrame(
            columns=[self.time_column_name, self.value_column_name])
        self.__data = pd.DataFrame(columns=self.__raw_data.columns)

        self.__date_path = []
        self.__loaded_files_no = 0

    def load_from_daily_csv(self, dir, filename_prefix, time_column_name, value_column_name):
        daily_suffix = '[0-9][0-9][0-9][0-9][0-9][0-9].csv'

        print("Loading data from daily CSV files...")
        self.__load_from_csv_files(
            dir, filename_prefix, daily_suffix, time_column_name, value_column_name)

    def get_data_range_min(self):
        return self.__raw_data.index.min()

    def get_data_range_max(self):
        return self.__raw_data.index.max()

    def get_data(self):
        return self.__data

    # PRIVATE METHODS #

    def __load_from_csv_files(self, data_dir, filename_prefix, filename_suffix, time_column_name, value_column_name):
        self.__loaded_files_no = 0
        self.__data = pd.DataFrame(
            columns=[self.time_column_name, self.value_column_name])

        # get a list of all matching files
        dataset_file_paths = sorted(Path(data_dir).glob(
            filename_prefix + filename_suffix))

        # create a tuples with measurement dates and file paths
        self.__date_path.clear()
        for path in dataset_file_paths:
            file_name = Path(path).name
            # data acquisition day is last 6 digits of the file name (format: YYMMDD)
            date_str = file_name[-10:-4]
            date = datetime.strptime(date_str, '%y%m%d')
            self.__date_path.append((date, path))

        # load data iteratively
        for _, path in self.__date_path:
            # parse file using provided column names
            new_data = pd.read_csv(path, comment='#', usecols=[time_column_name, value_column_name], parse_dates=[
                                   time_column_name], dtype={value_column_name: float})
            # rename columns to match internal naming standard
            new_data.rename(columns={time_column_name: self.time_column_name,
                            value_column_name: self.value_column_name}, inplace=True)
            # concatenate read data
            self.__raw_data = pd.concat([self.__raw_data, new_data], axis=0)

            self.__loaded_files_no += 1
        # index read data by time
        self.__raw_data.set_index(self.time_column_name, inplace=True)

        print("Dataset was created out of " +
              str(self.__loaded_files_no) + " matching files.")
        print(str(len(self.__raw_data.index)) + " raw measurements span between " +
              str(self.get_data_range_min()) + " and " + str(self.get_data_range_max()) + ".")

        # resample dataset to get evenly spaced time series
        self.__resample_1s()

    def __resample_1s(self):
        if (len(self.__raw_data.index) < 2):
            # nothing to resample due to missing data
            print(
                "Can't resample source data as there is not much data for the operation.")
            return

        print("Data resampling...")

        # resample to 1[s] interval by interpolation
        self.__data = self.__raw_data.resample('1S').interpolate()
        # create new timebase in the range of the raw data
        start_time = self.__raw_data.index[0]
        end_time = self.__raw_data.index[-1]
        data_points_times = pd.date_range(start_time, end_time, freq='1S')
        # and reindex in order to calculate newly added points
        self.__data = self.__data.reindex(
            data_points_times)

        print("The amount of datapoints was increased by " + str(len(self.__data.index) - len(self.__raw_data.index)) +
              " to get " + str(len(self.__data.index)) + " measurements evenly spaced in time.")
