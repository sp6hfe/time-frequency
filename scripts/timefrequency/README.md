# _timefrequency_ - time and frequency data analysis package

This Python package allows for analysis of time and frequency measurements.

It was created for the purpose of using it on an edge device (like Raspberry PI) in order to prepare input data for a central node (gathering information from spreaded measurement devices), although it may be used wherever needed as the code isn't coupled anyhow to PI's HW/SW specifics.  
While allowing for calculations of useful metrics it is also usable for source data analysis in order to find issues with measuring system itself.

## Features
* source data loading from files (CSV)
* analysis of the input data (missing datapoints)
* input data resampling to create timely uniform dataset
* calculation of the Allan deviation (ADEV, MDEV) and `png` image creation

## Source data requirements

### general
* time is expressed in `UTC` (to rule out potential issues with time zones and daylight saving time changes)
* source data should be organized in files dedicated to a distinct measurement day
* source data file names should follow a pattern: `name_prefix` + `measurement_day` + file extension (i.e. `analysis230517.csv`)

### data files
* data should be gathered evenly in time with resolution down to 1[s] (resampling usually degrade signal's information)
* files should at least consist of `time` and `value` records
* earliest data point should be taken on `00:00:00 UTC`
* latest data point should be taken on `23:59:59 UTC`
* comment lines start with a `#` sign,

### CSV specifics
* data should be `comma separated`
* file should include a header row containing column names (i.e. `time,value`)
* column with measurement timestamp should be in a datetime UTC format (i.e. `2023-05-17T01:15:27Z`)
* column with measurement value should be a float number (i.e. `224999.865`)
