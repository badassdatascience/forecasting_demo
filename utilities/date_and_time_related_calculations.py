import datetime

def compute_datetime_information(df, tz):
    df_to_return = df.copy()
    df_to_return['datetime_tz'] = [datetime.datetime.fromtimestamp(x, tz) for x in df_to_return.index]
    df_to_return['weekday_tz'] = [datetime.datetime.weekday(x) for x in df_to_return['datetime_tz']]
    df_to_return['hour_tz'] = [x.hour for x in df_to_return['datetime_tz']]
    return df_to_return