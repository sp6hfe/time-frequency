import pandas as pd


def resample_1s(source_data: pd.DataFrame):
    if (len(source_data) < 2):
        # nothing to resample due to missing data
        print(
            "Can't resample source data as there is not much data for the operation.")
        return None

    print("Data resampling...")

    # resample to 1[s] interval by interpolation
    resampled_data = source_data.resample('1S').interpolate()
    # create new timebase in the range of the raw data
    start_time = source_data.index[0]
    end_time = source_data.index[-1]
    resampled_data_points_time = pd.date_range(
        start_time, end_time, freq='1S')

    # and reindex in order to calculate newly added points
    resampled_data = resampled_data.reindex(
        resampled_data_points_time)

    return resampled_data
