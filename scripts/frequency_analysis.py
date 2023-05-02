from pathlib import Path
from timefrequency import data_provider


def main():
    csv_time_column_name = 'UTC'
    csv_frequency_column_name = 'Freq'
    csv_filename_prefix = 'analysis'
    csv_files_subfolder = 'data'

    # data folder is one level up relatively to scripts location
    csv_files_path = Path(__file__).resolve(
    ).parent.parent / csv_files_subfolder

    data = data_provider.CsvDataProvider(
        csv_time_column_name, csv_frequency_column_name)
    data.load(csv_files_path, csv_filename_prefix)

    print("Data set was loaded from " +
          str(data.get_loaded_files_no()) + " matching files.")
    print(str(data.get_raw_data_no()) + " raw measurements span from " +
          str(data.get_data_range_min()) + " to " + str(data.get_data_range_max()) + ".")
    print("After resampling the amount of datapoints was increased by " + str(data.get_data_no() - data.get_raw_data_no()) +
          " to get " + str(data.get_data_no()) + " measurements evenly spaced in time.")


if __name__ == "__main__":
    main()
