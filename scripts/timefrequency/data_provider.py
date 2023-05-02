import pandas as pd
from pathlib import Path
from datetime import datetime


class CsvDataProvider:
    def __init__(self, time_column_name, value_column_name):
        self.time_column_name = time_column_name
        self.value_column_name = value_column_name

        self.raw_data = pd.DataFrame(
            columns=[self.time_column_name, self.value_column_name])

        self.data_filename_suffix = '[0-9][0-9][0-9][0-9][0-9][0-9].csv'
        self.date_path = []
        self.loaded_files_no = 0

    def load(self, data_dir, data_filename_prefix):
        self.loaded_files_no = 0

        # get a list of all matching files
        data_set_file_paths = sorted(Path(data_dir).glob(
            data_filename_prefix + self.data_filename_suffix))

        # create a tuples with measurement dates and file paths
        self.date_path.clear()
        for path in data_set_file_paths:
            file_name = Path(path).name
            # data acquisition day is last 6 digits of the file name (format: YYMMDD)
            date_str = file_name[-10:-4]
            date = datetime.strptime(date_str, '%y%m%d')
            self.date_path.append((date, path))

        # load data iteratively
        for _, path in self.date_path:
            new_data = pd.read_csv(path, comment='#', usecols=[self.time_column_name, self.value_column_name], parse_dates=[
                self.time_column_name], dtype={self.value_column_name: float})
            self.raw_data = pd.concat([self.raw_data, new_data], axis=0)
            self.loaded_files_no += 1

        # index this dataset by the time
        self.raw_data.set_index(self.time_column_name, inplace=True)

    def get_loaded_files_no(self):
        return self.loaded_files_no

    def get_data_range_min(self):
        return self.raw_data.index.min()

    def get_data_range_max(self):
        return self.raw_data.index.max()

    def get_raw_data_no(self):
        return len(self.raw_data.index)
