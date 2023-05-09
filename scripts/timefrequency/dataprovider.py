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
        self.__missing_raw_data = pd.DataFrame(columns=[self.time_column_name])

        self.__data_summary = {
            "loaded_files_no": 0,
            "raw_data_points_no": 0,
            "data_points_no": 0,
            "time_range": [0, 0],
            "missing_raw_data_points_time": [],
        }

        self.__date_path = []
        self.__daily_file_suffix = '[0-9][0-9][0-9][0-9][0-9][0-9].csv'

    def load_from_daily_csv(self, dir, filename_prefix, time_value_columns):

        print("Loading data from daily CSV files...")
        self.__load_from_csv_files(
            dir, filename_prefix + self.__daily_file_suffix, time_value_columns)

    def get_data_summary(self):
        return self.__data_summary

    def get_data(self):
        return self.__data

    def get_raw_data(self):
        return self.__raw_data

    # PRIVATE METHODS #

    def __load_from_csv_files(self, data_dir, files_name_filter, time_value_columns, separator=",", comment="#"):
        loaded_files_no = 0
        self.__data = pd.DataFrame(
            columns=[self.time_column_name, self.value_column_name])

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
            if self.__load_from_csv(path, time_value_columns, None, separator, comment):
                loaded_files_no += 1

        # clear time series from errors
        self.__remove_invalid_data()

        # index read data by time
        self.__raw_data.set_index(self.time_column_name, inplace=True)

        # update data summary
        self.__data_summary["loaded_files_no"] = loaded_files_no
        self.__data_summary["raw_data_points_no"] = len(
            self.__raw_data.index)
        self.__data_summary["time_range"] = [
            self.__raw_data.index.min(), self.__raw_data.index.max()]

        # resample dataset to get evenly spaced time series
        self.__resample_1s()

    def __load_from_csv(self, path, time_value_columns=None, time_spec=None, separator=',', comment='#'):
        # validate columns spec to be either None or a 2 element list (time column name/index, value column name/index)
        if time_value_columns is not None and (type(time_value_columns) is not list or len(time_value_columns) != 2):
            print("Time/value columns specifier for " + str(path) +
                  " is wrong (" + str(time_value_columns) + "). No data will be loaded.")
            return False

        if time_value_columns is None:
            # TODO: handle single column file
            print("TODO: implement handling of a single column values file.")
            return False
        else:
            # read time/values
            new_data = pd.read_csv(path, usecols=time_value_columns, parse_dates=[
                                   time_value_columns[0]], dtype={time_value_columns[1]: float}, sep=separator, comment=comment)

            # rename columns to match internal naming standard
            new_data.rename(columns={time_value_columns[0]: self.time_column_name,
                                     time_value_columns[1]: self.value_column_name}, inplace=True)

            # concatenate read data
            self.__raw_data = pd.concat([self.__raw_data, new_data], axis=0)

        return True

    def __remove_invalid_data(self):
        searching_for_correct_time = False
        data_index_ranges_to_drop = []

        last_correct_datetime = pd.to_datetime(
            self.__raw_data[self.time_column_name][0])

        invalid_data_starting_index = 0

        for index, date in enumerate(self.__raw_data[self.time_column_name]):
            current_datetime = pd.to_datetime(date)
            time_difference = current_datetime - last_correct_datetime

            if searching_for_correct_time:
                if time_difference > pd.Timedelta(0):
                    searching_for_correct_time = False
                    # insert higher indexes 1st in order to make data dropping easier
                    data_index_ranges_to_drop.insert(0,
                                                     [invalid_data_starting_index, index])
                    print("Data gap ends before: " + str(current_datetime))
                    last_correct_datetime = current_datetime
            else:
                # detect if time has jumped back
                if time_difference < pd.Timedelta(0):
                    searching_for_correct_time = True
                    invalid_data_starting_index = index
                    print("Data gap start after: " +
                          str(last_correct_datetime))
                else:
                    last_correct_datetime = current_datetime

        # print(data_index_ranges_to_drop)
        print(len(self.__raw_data.index))
        for drop_range in data_index_ranges_to_drop:
            print("Droping invalid rows: " + str(drop_range))
            self.__raw_data.drop(
                self.__raw_data.index[drop_range[0]:drop_range[1]], inplace=True)
        print(len(self.__raw_data.index))

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

        # analyze missing measurements in raw data (based on samples time comparison)
        self.__missing_raw_data = data_points_times.difference(
            self.__raw_data.index).to_frame(name=self.time_column_name, index=False)

        # update data summary
        self.__data_summary["data_points_no"] = len(self.__data.index)
        self.__data_summary["missing_raw_data_points_time"] = self.__missing_raw_data.to_dict(
            orient="list")[self.time_column_name]
