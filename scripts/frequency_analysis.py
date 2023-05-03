from pathlib import Path
from timefrequency.timefrequency import TimeFrequency


def main():
    csv_time_column_name = 'UTC'
    csv_frequency_column_name = 'Freq'
    csv_filename_prefix = 'analysis'
    csv_files_subfolder = 'data'
    results_files_subfolder = 'output'

    # data and results folders is one level up relatively to scripts location
    csv_files_path = Path(__file__).resolve(
    ).parent.parent / csv_files_subfolder
    result_files_path = Path(__file__).resolve(
    ).parent.parent / results_files_subfolder

    tf = TimeFrequency(csv_time_column_name, csv_frequency_column_name)
    tf.load_csv_data(csv_files_path, csv_filename_prefix)

    print("Data set was loaded from " +
          str(tf.get_loaded_files_no()) + " matching files.")
    print(str(tf.get_raw_data_no()) + " raw measurements span from " +
          str(tf.get_data_range_min()) + " to " + str(tf.get_data_range_max()) + ".")
    print("After resampling the amount of datapoints was increased by " + str(tf.get_data_no() - tf.get_raw_data_no()) +
          " to get " + str(tf.get_data_no()) + " measurements evenly spaced in time.")

    tf.generate_mdev(result_files_path, csv_filename_prefix)


if __name__ == "__main__":
    main()
