#
# import system libraries
#
import pandas as pd
import argparse

#
# import local libraries
#
import boilerplate
from timeseries.models import Interval, Instrument, PriceType, Candlestick

#
# function to make dataframe
#
def make_candlestick_dataframe(price_type_name, instrument_name, interval_name):

    #
    # get instrument, price type, and interval
    #
    price_type = PriceType.objects.get(name = price_type_name)
    instrument = Instrument.objects.get(name = instrument_name)
    interval = Interval.objects.get(name = interval_name)

    #
    # get candlesticks
    #
    candlesticks = Candlestick.objects.filter(
        price_type = price_type,
        instrument = instrument,
        interval = interval
    ).select_related('timestamp').select_related('volume').order_by(
        'timestamp__timestamp'
    )

    #
    # initialize dataframe
    #
    timestamps = [x.timestamp.timestamp for x in candlesticks]
    df = pd.DataFrame(index=timestamps)

    #
    # add instrument
    #
    df['instrument'] = instrument_name

    #
    # add candlestick points
    #
    df['o'] = [x.o for x in candlesticks]
    df['l'] = [x.l for x in candlesticks]
    df['h'] = [x.h for x in candlesticks]
    df['c'] = [x.c for x in candlesticks]

    #
    # add volume
    #
    volumes = [x.volume.volume for x in candlesticks]
    df['volume'] = volumes

    return df

#
# main function
#
if __name__ == '__main__':
    
    #
    # declare command line arguments
    #
    parser = argparse.ArgumentParser(description='Make dataframe.')
    parser.add_argument('--price-type', type=str, help='e.g., "mid".', required=True)
    parser.add_argument('--instrument', type=str, help='e.g., "EUR/USD".', required=True)
    parser.add_argument('--interval-name', type=str, help='e.g. "Hour"', required=True)
    args = parser.parse_args()

    #
    # user settings
    #
    price_type_name = args.price_type
    instrument_name = args.instrument
    interval_name = args.interval_name

    #
    # get dataframe
    #
    df = make_candlestick_dataframe(price_type_name, instrument_name, interval_name)
    
    #
    # display
    #
    print(df)
