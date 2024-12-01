import numpy as np
import pyspark.sql.functions as f
from pyspark.sql.types import ArrayType, IntegerType, FloatType

#
# not sure about best practices here...
#
def difference_an_array(the_array, seconds_divisor):
    return [int((y - x) / seconds_divisor) for x, y in zip(the_array[0:-1], the_array[1:])]

udf_difference_an_array = f.udf(difference_an_array, ArrayType(IntegerType()))

def deal_with_offset(values_list, diff_timestamp_list, max_array_length):
    items = np.empty([max_array_length])
    items[:] = np.nan
    position_column = -1

    for i, diff in enumerate(diff_timestamp_list):
        position_column += diff
        items[position_column] = values_list[i]
    
    result = [float(x) for x in items]
    return result

udf_deal_with_offset = f.udf(deal_with_offset, ArrayType(FloatType()))


# https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
def nan_helper(y):
    return np.isnan(y), lambda z: z.nonzero()[0]


#
# https://stackoverflow.com/questions/70899029/how-to-get-all-rows-with-null-value-in-any-column-in-pyspark
#
def nan_count_spark(df, column_name):
    result = df.select(
        f.count(f.when(f.isnan(column_name)==True, f.col(column_name))).alias(column_name + '_NaN_count')
    )
    return result

