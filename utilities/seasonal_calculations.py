
#
# Generates two seasonal forecasting terms that together
# produce values useful for indicating the time of day.
# Period is forced through hard-coding to equal 24 hours.
#
# Input is a list or array of Unix epoch timestamps (always
# in seconds).
#

#
# Load useful libraries
#
import numpy as np
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, FloatType

#
# (Intentionally) hard-coded values -- because
# I want to 100% ensure a 24-hour period
# when these functions are used:
#
seasonal_forecasting_period = 60. * 60. * 24.
seasonal_forecasting_frequency = (2. * np.pi) / seasonal_forecasting_period
seasonal_forecasting_amplitude = 1.

#
# Only when the mean is zero are RMS and standard deviation the same
#     - https://math.stackexchange.com/questions/1537630/what-is-the-difference-between-root-mean-square-and-standard-deviation
#
# We need this because I want to ensure all values
# sent to the neural network are scaled appropriately.
# For the case of these seasonal indicators, I probably
# do not need to do this, but I'm doing it anyway just
# for consistency:
#
seasonal_forecasting_standard_deviation = 1. / np.sqrt(2.)

#
# function to normalize by standard devation
# (since mean = zero):
#
def normalize_by_standard_deviation(unfinished_calculation):
    return unfinished_calculation / seasonal_forecasting_standard_deviation 

#
# This ensures no NumPy artifacts remain when we return the results to Spark:
#
def make_it_spark_friendly(unfinished_calculation):
    calculation = [float(q) for q in unfinished_calculation]
    return calculation

##############################################################################
#   I would rather pass the function (np.sin or np.cos) as an argument       #
#   rather than create two functions, but Spark UDFs work better this way.   #
##############################################################################

#
# Sine wave:  Input values expressed in seconds
#
def normalized_spark_friendly_sine_with_24_hour_period(timestamp_array_in_seconds):
    return make_it_spark_friendly(
        normalize_by_standard_deviation(
            seasonal_forecasting_amplitude * np.sin(seasonal_forecasting_frequency * np.array(timestamp_array_in_seconds))
        )
    )
    
#
# Cosine wave:  Input values expressed in seconds
#
def normalized_spark_friendly_cosine_with_24_hour_period(timestamp_array_in_seconds):
    return make_it_spark_friendly(
        normalize_by_standard_deviation(
            seasonal_forecasting_amplitude * np.cos(seasonal_forecasting_frequency * np.array(timestamp_array_in_seconds))
        )
    )

#
# Create Spark UDFs
#
udf_normalized_spark_friendly_sine_with_24_hour_period = udf(normalized_spark_friendly_sine_with_24_hour_period, ArrayType(FloatType()))
udf_normalized_spark_friendly_cosine_with_24_hour_period = udf(normalized_spark_friendly_cosine_with_24_hour_period, ArrayType(FloatType()))


######################
#   Informal tests   #
######################

def main():
    print('Period in seconds: ', seasonal_forecasting_period)
    print('Frequency: ', seasonal_forecasting_frequency)
    print('Amplitude: ', seasonal_forecasting_amplitude)
    print('Standard deviation: ', seasonal_forecasting_standard_deviation)

if __name__ == '__main__':
    main()


