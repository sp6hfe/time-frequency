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

    tf = TimeFrequency()
    tf.load_from_daily_csv(csv_files_path, csv_filename_prefix,
                           csv_time_column_name, csv_frequency_column_name)

    data_summary = tf.get_data_summary()

    print("Dataset was created out of " +
          str(data_summary["loaded_files_no"]) + " matching files.")
    print(str(data_summary["data_points_no"]) + " data points span between " +
          str(data_summary["time_range"][0]) + " and " + str(data_summary["time_range"][1]) + ".")
    print("After resampling the amount of datapoints was increased by " + str(data_summary["data_points_no"] - data_summary["raw_data_points_no"]) +
          " to get measurements evenly spaced in time.")

    tf.generate_adev_plot(result_files_path)
    tf.generate_mdev_plot(result_files_path)


if __name__ == "__main__":
    main()
