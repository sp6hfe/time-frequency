from ..transformation.datacleaner import drop_data_with_time_jump_back
from ..transformation.resampler import resample_1s


import pandas as pd
from pathlib import Path
from datetime import datetime


class CsvProvider:
    def __init__(self):
        self.time_column_name = "time"
        self.value_column_name = "value"
        self.__daily_file_suffix = '[0-9][0-9][0-9][0-9][0-9][0-9].csv'

        self.__source_data = pd.DataFrame(
            columns=[self.time_column_name, self.value_column_name])
        self.__data = self.__source_data.copy()
        self.__loaded_files_no = 0

        self.__data_summary = {
            "loaded_files_no": self.__loaded_files_no,
            "source_data_points_no": len(self.__source_data.index),
            "data_points_no": len(self.__data.index),
            "time_range": [0, 0],
        }

        self.__date_path = []

    def load_from_daily_files(self, dir, filename_prefix, time_value_columns):
        print("Loading data from daily CSV files...")

        self.__source_data = pd.DataFrame(
            columns=[self.time_column_name, self.value_column_name])
        self.__data = self.__source_data.copy()
        self.__loaded_files_no = 0
        self.__load_from_multiple_files(
            dir, filename_prefix + self.__daily_file_suffix, time_value_columns)

    def get_data_summary(self):
        return self.__data_summary

    def get_data(self):
        return self.__data

    # PRIVATE METHODS #

    def __load_from_multiple_files(self, data_dir, files_name_filter, time_value_columns, separator=",", comment="#"):
        # get a list of all matching files
        dataset_file_paths = sorted(Path(data_dir).glob(files_name_filter))

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
            self.__load_from_file(path, time_value_columns,
                                  None, separator, comment)

        # after data concatenation reset the index so it matches row number (0-based)
        self.__source_data.reset_index(drop=True, inplace=True)

        # update data summary
        self.__data_summary["loaded_files_no"] = self.__loaded_files_no
        self.__data_summary["source_data_points_no"] = len(
            self.__source_data.index)

        # clear time series from errors
        drop_data_with_time_jump_back(
            self.__source_data, self.time_column_name)

        # reindex source data by time
        self.__source_data.set_index(self.time_column_name, inplace=True)

        # resample dataset to get evenly spaced time series
        resampled_Data = resample_1s(self.__source_data)
        if resampled_Data is not None:
            self.__data = resampled_Data

        # update data summary
        self.__data_summary["data_points_no"] = len(self.__data.index)
        self.__data_summary["time_range"] = [
            self.__data.index.min(), self.__data.index.max()]

    def __load_from_file(self, path, time_value_columns=None, time_spec=None, separator=',', comment='#'):
        # validate columns spec to be either None or a 2 element list (time column name/index, value column name/index)
        if time_value_columns is not None and (type(time_value_columns) is not list or len(time_value_columns) != 2):
            print("Time/value columns specifier for " + str(path) +
                  " is wrong (" + str(time_value_columns) + "). No data will be loaded.")
            return

        if time_value_columns is None:
            # TODO: handle single column file
            print("TODO: implement handling of a single column values file.")
            return
        else:
            # read time/values
            new_data = pd.read_csv(path, usecols=time_value_columns, parse_dates=[
                                   time_value_columns[0]], dtype={time_value_columns[1]: float}, sep=separator, comment=comment)

            # rename columns to match internal naming standard
            new_data.rename(columns={time_value_columns[0]: self.time_column_name,
                                     time_value_columns[1]: self.value_column_name}, inplace=True)

            # concatenate read data
            self.__source_data = pd.concat(
                [self.__source_data, new_data], axis=0)

            # update stat
            self.__loaded_files_no += 1
