
#
# load useful libraries
#
import pyspark.sql.functions as f

#
# https://stackoverflow.com/questions/70899029/how-to-get-all-rows-with-null-value-in-any-column-in-pyspark
#
def nan_count_spark(df, column_name):
    result = df.select(
        f.count(f.when(f.isnan(column_name)==True, f.col(column_name))).alias(column_name + '_NaN_count')
    )
    return result
