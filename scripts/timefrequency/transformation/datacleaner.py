import pandas as pd


def drop_data_with_time_jump_back(data: pd.DataFrame, time_column: str):
    searching_for_correct_time = False
    data_rows_ranges_to_drop = []
    invalid_data_starting_row = 0

    last_correct_datetime = data[time_column].iloc[0]

    for current_row_index, current_datetime in enumerate(data[time_column]):
        time_difference = current_datetime - last_correct_datetime

        if searching_for_correct_time:
            # detect if time is progressing correctly
            if time_difference > pd.Timedelta(0):
                searching_for_correct_time = False
                # insert higher indexes 1st in order to make data dropping easy
                data_rows_ranges_to_drop.insert(
                    0, [invalid_data_starting_row, current_row_index])
                print("Time correctly progressing from row " +
                      str(current_row_index) + " (" + str(current_datetime) + ").")
                # time is OK again
                last_correct_datetime = current_datetime
        else:
            # detect if time has jumped back
            if time_difference < pd.Timedelta(0):
                searching_for_correct_time = True
                invalid_data_starting_row = current_row_index
                print("Time jump-back detected in row " + str(invalid_data_starting_row) +
                      " (" + str(last_correct_datetime) + " -> " + str(current_datetime) + ".")
            else:
                last_correct_datetime = current_datetime

    # handle case when jump-back spread to the end of the time series
    if searching_for_correct_time:
        data_rows_ranges_to_drop.insert(
            0, [invalid_data_starting_row, current_row_index])
        print("Time wasn't correctly progressing to the last row.")

    # drop invalid data
    if len(data_rows_ranges_to_drop) > 0:
        print("Droping invalid rows...")
        initial_size = len(data.index)
        for drop_range in data_rows_ranges_to_drop:
            data.drop(
                data.index[drop_range[0]:drop_range[1]], inplace=True)
        final_size = len(data.index)
        print("Time series reduced by " +
              str(initial_size - final_size) + " records.")
